import copy
import json
from pathlib import Path
import unittest

import generator as g
import policies as p

ROOT=Path(__file__).resolve().parents[1]


class RequestedChanges(unittest.TestCase):
    def setUp(self):
        self.task=g.normalize(g.read_json(ROOT/'examples/demo_task.json'))[0]
        self.plan=g.read_json(ROOT/'examples/demo_plan.json')

    def test_five_variants_and_readable_weights(self):
        plan=copy.deepcopy(self.plan)
        p.assemble_matrix(plan,5)
        g.ground_task_completion(plan,self.task)
        g.check_plan(plan,self.task,5)
        group=g.assemble(self.task,plan,'offline')
        self.assertEqual(len(group['variants']),5)
        self.assertGreaterEqual(len({cid for v in group['variants'] for cid in v['candidate_ids']}),4)
        self.assertEqual(len({tuple(sorted(v['candidate_ids'])) for v in group['variants']}),5)
        self.assertTrue(all(len(v['candidate_ids'])==1 for v in group['variants']))
        self.assertEqual({v['tier'] for v in group['variants']},{'A','C','D'})
        by_id={c['id']:c for c in plan['candidates']}
        self.assertTrue(all(v['instruction']==by_id[v['candidate_ids'][0]]['instruction'] for v in group['variants']))
        for variant in group['variants']:
            weights=[r['weight'] for r in variant['rubric'] if r['layer']=='IF']
            self.assertAlmostEqual(sum(weights),.6)
            self.assertTrue(all(abs(w-round(w,3))<1e-12 for w in weights))
            self.assertFalse(any(str(w).startswith('0.199999') for w in weights))

    def test_no_fingerprint_basis_means_no_negative_penalty(self):
        plan=copy.deepcopy(self.plan)
        plan['side_effect'].pop('basis')
        p.prepare_plan(plan,self.task)
        p.assemble_matrix(plan,5)
        g.ground_task_completion(plan,self.task)
        g.check_plan(plan,self.task,5)
        group=g.assemble(self.task,plan,'offline')
        self.assertEqual(group['construction_metadata']['side_effect_policy'],'omitted_no_fingerprint_basis')
        self.assertTrue(all(not any(r['layer']=='SE' for r in v['rubric']) for v in group['variants']))

    def test_catalog_process_is_grounded_in_available_tool(self):
        task=copy.deepcopy(self.task)
        task['tools'].append('mcp_resource_list')
        task['fingerprint']['tool_seq']=['file_read','mcp_resource_list']
        compiled=p.compile_policy({'kind':'workflow_catalog_first','catalog_tool':'mcp_resource_list'},task)
        self.assertGreater(len(compiled['instruction']),100)
        self.assertEqual(compiled['checks'][0]['rule'],
                         {'path':'trace.calls.0.name','op':'eq','value':'mcp_resource_list'})
        self.assertEqual(p.self_test_policy({'kind':'workflow_catalog_first','catalog_tool':'mcp_resource_list'},compiled,g.evaluate_rule)['status'],'passed')

    def test_catalog_alias_and_duplicate_first_call_are_repaired_locally(self):
        task=copy.deepcopy(self.task)
        task['tools'].append('mcp_resource_list')
        plan={'candidates':[
            {'id':'c1','policy':{'kind':'first_tool','tools':['mcp_resource_list']}},
            {'id':'c2','policy':{'kind':'workflow_catalog_first','tool':'mcp_resource_list'}},
            {'id':'c3','policy':{'kind':'workflow_catalog_first','tools':['not_available']}}]}
        p.prepare_plan(plan,task)
        self.assertEqual([c['id'] for c in plan['candidates']],['c2'])
        self.assertEqual(plan['candidates'][0]['policy']['catalog_tool'],'mcp_resource_list')
        self.assertEqual(len(plan['discarded_candidates']),2)

    def test_known_compliant_baseline_is_excluded_before_model_review(self):
        task=copy.deepcopy(self.task)
        task['fingerprint']['tool_seq']=['file_read','file_edit']
        plan={'candidates':[
            {'id':'order','policy':{'kind':'tool_order','before':'file_read','after':'file_edit'}},
            {'id':'repeat','policy':{'kind':'tool_repeat_limit','tool':'file_edit','max':1}},
            {'id':'changed','policy':{'kind':'first_tool','tools':['file_edit']}}]}
        p.screen_baseline(plan,task,g.evaluate_rule)
        self.assertEqual(set(plan['local_excluded_candidate_ids']),{'order','repeat'})
        self.assertEqual(plan['candidates'][2]['baseline_check']['status'],'observed_violation')

    def test_long_plan_first_policy_requires_real_tool(self):
        task=copy.deepcopy(self.task)
        task['tools'].append('task_planning')
        compiled=p.compile_policy({'kind':'workflow_plan_first'},task)
        self.assertGreater(len(compiled['instruction']),100)
        self.assertEqual(compiled['checks'][0]['rule']['value'],'task_planning')
        self.assertEqual(p.self_test_policy({'kind':'workflow_plan_first'},compiled,g.evaluate_rule)['status'],'passed')
        legal=copy.deepcopy(task)
        legal['task_type']='legal_matter+evidence_reconciliation'
        alternative=p.compile_policy({'kind':'workflow_plan_first'},legal)
        self.assertNotEqual(compiled['instruction'],alternative['instruction'])
        self.assertEqual(compiled['checks'][0]['rule'],alternative['checks'][0]['rule'])

    def test_literature_about_code_repair_is_not_a_code_edit_task(self):
        task=copy.deepcopy(self.task)
        task['task_type']='literature_comparison'
        task['user_query']='比较三篇关于实现代码修复的论文，并说明成功率口径。'
        plan=copy.deepcopy(self.plan)
        g.ground_task_completion(plan,task)
        self.assertEqual(plan['tc_origin'],'model_proposed_requires_independent_review')
        self.assertNotIn('workspace_diff',plan['task_completion']['required_evidence'])


if __name__=='__main__':unittest.main()
