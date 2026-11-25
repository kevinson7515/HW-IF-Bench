import copy
from pathlib import Path
import unittest
from unittest.mock import patch

import generator as g
import policies as p


ROOT = Path(__file__).resolve().parents[1]


class MultistepWorkflow(unittest.TestCase):
    def setUp(self):
        self.task = g.normalize(g.read_json(ROOT / 'examples/demo_task.json'))[0]
        self.task['tools'] = ['file_glob', 'file_read', 'python_exec', 'cwd_inspect',
                              'web_search', 'web_fetch', 'task_planning']
        self.task['fingerprint']['tool_seq'] = ['file_read', 'python_exec']

    def test_routes_have_ordered_pass_and_fail_evidence(self):
        policies = [
            {'kind': 'workflow_locate_read', 'locate_tool': 'file_glob'},
            {'kind': 'workflow_workspace_read', 'workspace_tool': 'cwd_inspect'},
            {'kind': 'workflow_search_fetch'},
            {'kind': 'workflow_locate_read_run', 'locate_tool': 'file_glob', 'run_tool': 'python_exec'},
            {'kind': 'workflow_workspace_locate_read', 'workspace_tool': 'cwd_inspect', 'locate_tool': 'file_glob'},
            {'kind': 'workflow_plan_locate_read', 'locate_tool': 'file_glob'},
        ]
        for policy in policies:
            with self.subTest(policy=policy['kind']):
                compiled = p.compile_policy(policy, self.task)
                self.assertTrue(compiled['instr_types'][0].startswith('process-'))
                self.assertEqual(compiled['checks'][0]['rule']['path'], 'trace.calls')
                self.assertEqual(p.self_test_policy(policy, compiled, g.evaluate_rule)['status'], 'passed')
                self.assertFalse(p.observed_baseline_compliance(policy, self.task['fingerprint']))

        rule = p.compile_policy(policies[3], self.task)['checks'][0]['rule']
        calls = lambda names: {'trace': {'calls': [{'name': name} for name in names]}}
        self.assertTrue(g.evaluate_rule(rule, calls(['file_glob', 'file_read', 'file_read', 'python_exec'])))
        self.assertFalse(g.evaluate_rule(rule, calls(['file_glob', 'python_exec', 'file_read'])))
        self.assertFalse(g.evaluate_rule(rule, calls(['file_read', 'file_glob', 'python_exec'])))
        with self.assertRaisesRegex(ValueError, '无关字段'):
            p.compile_policy({'kind': 'workflow_search_fetch', 'workspace_tool': 'cwd_inspect'}, self.task)
        code_route = p.compile_policy(policies[4], self.task)
        legal_task = copy.deepcopy(self.task)
        legal_task['task_type'] = 'legal_matter'
        legal_route = p.compile_policy(policies[4], legal_task)
        self.assertNotEqual(code_route['instruction'], legal_route['instruction'])
        self.assertEqual(code_route['checks'], legal_route['checks'])

    def test_supplied_artifact_list_excludes_baseline_compliant_candidates(self):
        fingerprint = {'output_artifacts': [{'path': 'fixed/query.py'},
                                            {'path': 'tests/test_query.py'},
                                            {'path': 'patch.diff'}]}
        self.assertTrue(p.observed_baseline_compliance(
            {'kind': 'artifact_count', 'min': 2, 'max': 4}, fingerprint))
        self.assertTrue(p.observed_baseline_compliance(
            {'kind': 'artifact_extensions', 'extensions': ['.py', '.diff']}, fingerprint))
        self.assertFalse(p.observed_baseline_compliance(
            {'kind': 'artifact_count', 'min': 4, 'max': 6}, fingerprint))

    def test_compact_selection_prioritizes_supported_multistep_routes(self):
        plan = copy.deepcopy(g.read_json(ROOT / 'examples/demo_plan.json'))
        for i, policy in enumerate([
            {'kind': 'workflow_locate_read', 'locate_tool': 'file_glob'},
            {'kind': 'workflow_workspace_read', 'workspace_tool': 'cwd_inspect'},
            {'kind': 'workflow_search_fetch'},
        ], 100):
            plan['candidates'].append({'id': f'route_{i}', 'policy': policy,
                'basis': [{'field': 'tool_seq.0', 'baseline_value': 'file_read',
                           'target': 'file_glob', 'reason': '合成基线首个工具不同'}],
                'feasibility_reason': '合成任务提供所有阶段工具'})
        p.prepare_plan(plan, self.task)
        p.screen_baseline(plan, self.task, g.evaluate_rule)
        p.assemble_matrix(plan, 5, {'profile': 'balanced', 'max_combination': 6})
        selected = {cid for variant in plan['variants'] for cid in variant['candidate_ids']}
        selected_process = [c for c in plan['candidates'] if c['id'] in selected
                            and c['policy']['kind'] in p.workflow.CALL_ROUTE_KINDS]
        self.assertGreaterEqual(len(selected_process), 2)
        self.assertTrue(all(len(v['candidate_ids']) == 1 for v in plan['variants']))

    def test_generator_adds_routes_from_supplied_fingerprint(self):
        self.task['generation_options'] = {'profile': 'balanced', 'max_combination': 6,
            'candidate_count': 24, 'min_families': 1, 'strict_coverage': False}
        raw_plan = g.read_json(ROOT / 'examples/demo_plan.json')
        class OfflineClient:
            model = 'offline'
            def complete(self, messages):
                return copy.deepcopy(raw_plan)
        with patch('generator.semantic_review', return_value={'tc_grounded': True,
                'combinations_compatible': True, 'candidate_reviews': [],
                'issues': [], 'pending_checks': []}):
            group = g.generate(self.task, OfflineClient(), 5, repair=0)
        selected = {cid for v in group['variants'] for cid in v['candidate_ids']}
        self.assertTrue(any(cid.startswith('workflow_') for cid in selected))
        self.assertEqual(len(group['variants']), 5)


if __name__ == '__main__':
    unittest.main()
