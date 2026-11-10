import copy
import json
from pathlib import Path
import unittest

import generator as g
import policies as p


ROOT = Path(__file__).resolve().parents[1]


class WorkflowPrototype(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = g.normalize(g.read_json(ROOT / 'examples/workflow_demo_task.json'))[0]
        cls.plan = g.read_json(ROOT / 'examples/workflow_demo_plan.json')

    def test_each_workflow_policy_has_actual_pass_and_fail_evidence(self):
        candidates = [c for c in self.plan['candidates'] if c['policy']['kind'] in p.workflow.KINDS]
        self.assertEqual(len(candidates), 4)
        for candidate in candidates:
            with self.subTest(kind=candidate['policy']['kind']):
                compiled = p.compile_policy(candidate['policy'], self.task)
                self.assertGreaterEqual(len(compiled['instruction']), 100)
                self.assertNotIn('trace', compiled['instruction'])
                self.assertEqual(p.self_test_policy(candidate['policy'], compiled, g.evaluate_rule)['status'], 'passed')

    def test_capabilities_and_runtime_adapter_are_required(self):
        for candidate in self.plan['candidates'][:4]:
            task = copy.deepcopy(self.task)
            task['evidence_contract'] = {}
            with self.assertRaisesRegex(ValueError, '适配器'):
                p.compile_policy(candidate['policy'], task)
        task = copy.deepcopy(self.task)
        task['capabilities']['interactive_confirmation'] = False
        with self.assertRaisesRegex(ValueError, 'interactive_confirmation'):
            p.compile_policy({'kind': 'workflow_approval_gate'}, task)

    def test_progress_needs_visible_message_after_each_three_calls(self):
        rule = p.compile_policy({'kind': 'workflow_plan_progress'}, self.task)['checks'][0]['rule']
        events = [{'kind': 'assistant_message', 'content': '- [ ] 探查\n- [ ] 修改'}]
        events += [{'kind': 'tool_call', 'name': 'file_read', 'status': 'completed'} for _ in range(3)]
        self.assertFalse(g.evaluate_rule(rule, {'trace': {'events': events}}))
        events.append({'kind': 'assistant_message', 'content': '[进度]\n- [x] 探查\n关键信息：已查看文件'})
        self.assertTrue(g.evaluate_rule(rule, {'trace': {'events': events}}))

    def test_confirmation_requires_matching_real_user_event(self):
        rule = p.compile_policy({'kind': 'workflow_approval_gate'}, self.task)['checks'][0]['rule']
        request = {'kind': 'approval_request', 'id': 'r1', 'paths': ['a.py']}
        write = {'kind': 'tool_call', 'name': 'file_edit', 'effect': 'write',
                 'status': 'completed', 'target_paths': ['a.py']}
        self.assertFalse(g.evaluate_rule(rule, {'trace': {'events': [request, write]}}))
        self.assertTrue(g.evaluate_rule(rule, {'trace': {'events': [request]}}))
        approved = {'kind': 'user_confirmation', 'request_id': 'r1', 'approved': True}
        self.assertTrue(g.evaluate_rule(rule, {'trace': {'events': [request, approved, write]}}))
        other = copy.deepcopy(write); other['target_paths'] = ['b.py']
        self.assertFalse(g.evaluate_rule(rule, {'trace': {'events': [request, approved, other]}}))

    def test_workflow_matrix_uses_long_a_and_four_to_six_for_bcd(self):
        plan = copy.deepcopy(self.plan)
        p.assemble_matrix(plan, 'auto', self.task['generation_options'])
        g.check_plan(plan, self.task, 'auto')
        group = g.assemble(self.task, plan, 'offline')
        self.assertEqual(len(group['variants']), 20)
        self.assertEqual({v['tier'] for v in group['variants']}, {'A', 'B', 'C', 'D'})
        for variant in group['variants']:
            self.assertGreaterEqual(len(variant['instruction']), 100)
            if variant['tier'] != 'A':
                self.assertTrue(4 <= variant['complexity']['constraint_count'] <= 6)
                if variant['tier'] == 'D':
                    self.assertNotIn('c4', variant['candidate_ids'])

    def test_workflow_rule_flows_through_full_score(self):
        plan=copy.deepcopy(self.plan)
        p.assemble_matrix(plan, 'auto', self.task['generation_options'])
        group=g.assemble(self.task, plan, 'offline')
        variant=next(v for v in group['variants'] if v['tier']=='A' and v['candidate_ids']==['c1'])
        events=[{'kind':'assistant_message','content':'- [ ] 检查\n- [ ] 修改'}]
        events += [{'kind':'tool_call','name':'file_read','status':'completed'} for _ in range(3)]
        events.append({'kind':'assistant_message','content':'[进度]\n- [x] 检查\n关键信息：已检查输入'})
        evidence={'trace':{'events':events},'final_answer':'已完成修改',
                  'workspace_diff':{'modified':['parser.py']},'code':'def parse(x): return x',
                  'validation_trace':'synthetic validation only'}
        judgments={variant['variant_id']+'-TC-1':'FULL',variant['variant_id']+'-SE-1':'NO'}
        result=g.score(variant,evidence,judgments)
        self.assertEqual(result['status'],'graded')
        self.assertTrue(result['joint_success'])


if __name__ == '__main__':
    unittest.main()
