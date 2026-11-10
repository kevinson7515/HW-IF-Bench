import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import generator as g
import policies as p

ROOT=Path(__file__).resolve().parents[1]


def approve(plan):
    return {'candidate_reviews':[{'id':c['id'],'anti_default':True,'task_preserving':True,'reason':'离线模拟依据，非真实审查'} for c in plan['candidates']],
            'tc_grounded':True,'combinations_compatible':True,'issues':[],'pending_checks':[]}


class NewRules(unittest.TestCase):
    def setUp(self):self.task={'tools':['file_read','file_edit','web_search','web_fetch'],
        'capabilities':{'model_visible_tool_call_ids':True},
        'evidence_contract':{'trace.calls.id':{'implemented':True,'extractor':'runtime_call_id','source':'tool_events'}}}
    def compiled(self,policy):return p.compile_policy(policy,self.task)
    def check(self,policy,evidence):return all(g.evaluate_rule(c['rule'],evidence) for c in self.compiled(policy)['checks'])
    def test_every_new_policy_has_passing_and_failing_fixtures(self):
        samples=[{'kind':'json_schema','schema':{'type':'object','properties':{'result':{'type':'string','minLength':1}},'required':['result']}},
            {'kind':'paragraph_range','min':2,'max':4},{'kind':'opening_line','text':'结论'}, {'kind':'no_code_fences'},
            {'kind':'tool_total_budget','limit':3},{'kind':'unique_tool_budget','limit':2},
            {'kind':'tool_repeat_limit','tool':'file_read','max':2},{'kind':'tool_order','before':'file_read','after':'file_edit'},
            {'kind':'conditional_section','on_error':'问题','on_success':'验证'}, {'kind':'evidence_refs','min':2},
            {'kind':'artifact_extensions','extensions':['.svg','.png']},{'kind':'artifact_count','min':1,'max':3},
            {'kind':'section_limits','sections':{'结论':80,'依据':120}},{'kind':'citation_range','min':1,'max':3}]
        self.assertEqual({x['kind'] for x in samples},set(p.EXTRA_KINDS)-set(p.workflow.KINDS))
        covered=set()
        for policy in samples:
            with self.subTest(kind=policy['kind']):
                compiled=self.compiled(policy)
                covered.update(compiled['instr_types'])
                for c in compiled['checks']:g.validate_rule(c['rule'])
                self.assertEqual(p.self_test_policy(policy,compiled,g.evaluate_rule)['status'],'passed')
        self.assertEqual(covered,p.EXTRA_FAMILIES-{family for family,_ in p.workflow.KINDS.values()})
    def test_json_types_duplicates_and_extra_keys(self):
        policy={'kind':'json_schema','schema':{'type':'object','properties':{'n':{'type':'integer'}},'required':['n']}}
        self.assertTrue(self.check(policy,{'final_answer':'{"n":2}'}))
        for text in ['{"n":true}','{"n":1,"n":2}','{"n":1,"extra":1}','```json\n{"n":2}\n```','{"n":NaN}']:
            self.assertFalse(self.check(policy,{'final_answer':text}),text)
    def test_nested_schema_and_bounds(self):
        schema={'type':'array','items':{'type':'string','minLength':2},'minItems':1,'maxItems':2}
        policy={'kind':'json_schema','schema':schema}
        self.assertTrue(self.check(policy,{'final_answer':'["内容"]'}))
        for text in ['[]','["短"]','["内容", "内容", "内容"]']:self.assertFalse(self.check(policy,{'final_answer':text}))
    def test_unsupported_schema_is_rejected(self):
        with self.assertRaises(ValueError):self.compiled({'kind':'json_schema','schema':{'type':'object','$ref':'https://example.com'}})
    def test_condition_missing_status_is_ungradable_not_success(self):
        policy={'kind':'conditional_section','on_error':'问题','on_success':'验证'}
        with self.assertRaises(ValueError):self.check(policy,{'trace':{'calls':[{'name':'file_read'}]},'final_answer':'## 验证\n通过'})
        with self.assertRaises(g.Invalid):self.check(policy,{'trace':{'calls':[]}})
    def test_condition_both_runtime_branches(self):
        policy={'kind':'conditional_section','on_error':'问题','on_success':'验证'}
        self.assertTrue(self.check(policy,{'trace':{'calls':[{'name':'file_read','status':'error'}]},'final_answer':'## 问题\n失败说明'}))
        self.assertTrue(self.check(policy,{'trace':{'calls':[]},'final_answer':'## 验证\n没有工具调用'}))
    def test_evidence_refs_cannot_reference_failure_unknown_or_duplicate_ids(self):
        policy={'kind':'evidence_refs','min':1}
        evidence={'trace':{'calls':[{'name':'file_read','id':'a','status':'completed'},{'name':'file_read','id':'b','status':'error'}]},'final_answer':'内容[证据:a]'}
        self.assertTrue(self.check(policy,evidence))
        for text in ['[证据:b]','[证据:a] [证据:unknown]']:
            evidence['final_answer']=text;self.assertFalse(self.check(policy,evidence))
        evidence['trace']['calls'][1]['id']='a'
        with self.assertRaises(ValueError):self.check(policy,evidence)
    def test_instructions_do_not_expose_internal_trace_and_ids_need_runtime_visibility(self):
        samples=[{'kind':'tool_repeat_limit','tool':'file_read','max':2},
                 {'kind':'tool_order','before':'file_read','after':'file_edit'},
                 {'kind':'conditional_section','on_error':'问题','on_success':'验证'},
                 {'kind':'evidence_refs','min':1}]
        for policy in samples:
            instruction=self.compiled(policy)['instruction']
            for internal in ('trace','评分','不可评分','记录顺序'):
                self.assertNotIn(internal,instruction)
        without_visibility=copy.deepcopy(self.task)
        del without_visibility['capabilities']['model_visible_tool_call_ids']
        with self.assertRaises(ValueError):p.compile_policy({'kind':'evidence_refs','min':1},without_visibility)
        without_adapter=copy.deepcopy(self.task)
        del without_adapter['evidence_contract']['trace.calls.id']
        with self.assertRaises(ValueError):p.compile_policy({'kind':'evidence_refs','min':1},without_adapter)
    def test_order_requires_actual_tools_and_nonvacuity(self):
        policy={'kind':'tool_order','before':'file_read','after':'file_edit'}
        self.assertFalse(self.check(policy,{'trace':{'calls':[]}}))
        with self.assertRaises(ValueError):self.compiled({'kind':'tool_order','before':'invented','after':'file_edit'})
    def test_section_counts_fenced_content_but_not_fenced_headers(self):
        policy={'kind':'section_limits','sections':{'结论':40}}
        self.assertTrue(self.check(policy,{'final_answer':'## 结论\n内容\n```\n## 伪标题\n```'}))
        self.assertFalse(self.check(policy,{'final_answer':'## 结论\n正文\n## 结论\n重复'}))
    def test_duplicate_artifact_paths_not_counted_as_distinct(self):
        with self.assertRaises(ValueError):self.check({'kind':'artifact_count','min':1,'max':2},{'artifacts':[{'path':'a.txt'},{'path':'a.txt'}]})
    def test_baseline_compliant_policies_excluded_with_real_projection(self):
        plan={'candidates':[dict(id='a',policy={'kind':'no_code_fences'}),dict(id='b',policy={'kind':'opening_line','text':'新首行'})]}
        p.prepare_plan(plan,self.task)
        task=dict(self.task,baseline_observation={'evaluation_projection':{'final_answer':'原首行','trace':{'calls':[]},'artifacts':[]}})
        p.screen_baseline(plan,task,g.evaluate_rule)
        self.assertEqual(plan['local_excluded_candidate_ids'],['a'])
        self.assertEqual(plan['candidates'][1]['baseline_check']['status'],'observed_violation')
    def test_unavailable_baseline_status_is_recorded_not_fabricated(self):
        plan={'candidates':[dict(id='c',policy={'kind':'conditional_section','on_error':'问题','on_success':'验证'})]}
        p.prepare_plan(plan,self.task)
        task=dict(self.task,baseline_observation={'evaluation_projection':{'final_answer':'说明','trace':{'calls':[{'name':'file_read'}]}}})
        p.screen_baseline(plan,task,g.evaluate_rule)
        self.assertEqual(plan['candidates'][0]['baseline_check']['status'],'unavailable')
        self.assertEqual(plan['local_excluded_candidate_ids'],[])
    def test_json_and_markdown_incompatible(self):
        cs=[{'policy':{'kind':'json_schema'}},{'policy':{'kind':'headings','headings':['结论']}}]
        with self.assertRaises(ValueError):p.validate_combination(cs)
    def test_order_budget_incompatible(self):
        cs=[{'policy':{'kind':'tool_order','before':'file_read','after':'file_edit'}},{'policy':{'kind':'unique_tool_budget','limit':1}}]
        with self.assertRaises(ValueError):p.validate_combination(cs)

    def test_provided_query_and_fingerprint_are_matched_without_reading_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            query={'task_id':7,'group_id':'G-7','user_query':'检查附件','attached_files':['a.txt']}
            fp={'task_id':7,'user_query':'检查附件','system_prompt':'执行原任务',
                'tools':['file_read'],'env':{'snapshot':'provided'},
                'baseline_fingerprint':{'tool_seq':['file_read'],'reply_len':17}}
            (root/'user_query_all.jsonl').write_text(json.dumps(query,ensure_ascii=False),encoding='utf-8')
            (root/'baseline_fingerprint.jsonl').write_text(json.dumps(fp,ensure_ascii=False),encoding='utf-8')
            run=root/'dsh-runs'/'G-7';run.mkdir(parents=True)
            (run/'final.txt').write_text('do not import this',encoding='utf-8')
            task=g.load_tasks(root)[0]
            self.assertEqual(task['fingerprint'],fp['baseline_fingerprint'])
            self.assertNotIn('do not import this',g.canonical(task))
            self.assertEqual(task['import_metadata']['fingerprint_provenance'],
                             'provided_by_user_not_independently_verified')
            self.assertEqual(len(task['import_metadata']['files_sha256']),2)
            self.assertEqual(g.load_tasks(root/'user_query_all.jsonl',root/'baseline_fingerprint.jsonl')[0]['fingerprint'],
                             fp['baseline_fingerprint'])
            fp['task_id']=8
            (root/'baseline_fingerprint.jsonl').write_text(json.dumps(fp,ensure_ascii=False),encoding='utf-8')
            with self.assertRaisesRegex(g.Invalid,'任务ID集合不一致'):
                g.load_tasks(root)

    def test_score_cli_accepts_current_generated_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'score.json'
            evidence=Path(temp)/'evidence.json'
            judgments=Path(temp)/'judgments.json'
            evidence.write_text('{}',encoding='utf-8')
            judgments.write_text('{}',encoding='utf-8')
            task=g.normalize(g.read_json(ROOT/'examples/demo_task.json'))[0]
            plan=g.read_json(ROOT/'examples/demo_plan.json')
            group=g.assemble(task,plan,'offline')
            groups=Path(temp)/'groups.json'
            g.write_json(groups,[g.public_group(group)])
            argv=['generator.py','score','--groups',str(groups),
                  '--group-id',group['group_id'],'--variant-id',group['variants'][0]['variant_id'],
                  '--evidence',str(evidence),'--judgments',str(judgments),'--output',str(output)]
            with patch('sys.argv',argv):g.main()
            self.assertEqual(g.read_json(output)['status'],'ungradable')


class Planner(unittest.TestCase):
    def setUp(self):
        self.task=g.normalize(g.read_json(ROOT/'examples/demo_task.json'))[0]
        self.plan=g.read_json(ROOT/'examples/demo_plan.json')
    def build(self,count='auto',profile='balanced'):
        plan=copy.deepcopy(self.plan);plan['generation_options']={'profile':profile,'max_combination':5}
        p.assemble_matrix(plan,count);g.ground_task_completion(plan,self.task);g.check_plan(plan,self.task,count)
        return plan
    def test_variable_counts_and_auto(self):
        for count in [4,5,6,12,24,48,'auto']:
            plan=self.build(count)
            self.assertEqual(len(plan['variants']),count if count!='auto' else 18)
            self.assertEqual({v['tier'] for v in plan['variants']},
                             {'A','C','D'} if count in (4,5,6) else {'A','B','C','D'})
            singles={v['candidate_ids'][0] for v in plan['variants'] if v['tier']=='A'}
            if count not in (4,5,6):
                for v in plan['variants']:self.assertLessEqual(set(v['candidate_ids']),singles)
            else:
                self.assertGreaterEqual(len({x for v in plan['variants'] for x in v['candidate_ids']}),4)
                self.assertTrue(all(len(v['candidate_ids'])==1 for v in plan['variants']))
    def test_stress_has_larger_combinations_and_multiple_conflicts(self):
        plan=self.build(24,'stress');coverage=p.coverage_summary(plan)
        self.assertGreaterEqual(max(len(v['candidate_ids']) for v in plan['variants']),4)
        self.assertGreaterEqual(len(coverage['conflict_styles']),2)
        self.assertTrue(any(v['tier']=='C' and len(v['candidate_ids'])>1 for v in plan['variants']))
        self.assertTrue(any(v['tier']=='D' and len(v['candidate_ids'])>1 for v in plan['variants']))
    def test_matrix_signatures_are_unique(self):
        plan=self.build(48,'stress')
        signatures={(v['tier'],tuple(sorted(v['candidate_ids'])),v['position'],v.get('context_records'),v.get('conflict_style')) for v in plan['variants']}
        self.assertEqual(len(signatures),48)
    def test_excluded_combo_does_not_remove_independent_singles(self):
        original=self.build(12);pair=next(v['candidate_ids'][:2] for v in original['variants'] if v['tier']=='B')
        self.plan['rejected_combinations']=[pair];plan=self.build(12)
        singles={v['candidate_ids'][0] for v in plan['variants'] if v['tier']=='A'}
        self.assertLessEqual(set(pair),singles)
        for v in plan['variants']:
            if v['tier']!='A':self.assertFalse(set(pair)<=set(v['candidate_ids']))
    def test_json_and_heading_can_be_independent_a_not_combined(self):
        pool=[{'id':'j','policy':{'kind':'json_schema'},'instr_types':['structured-output']},
              {'id':'h','policy':{'kind':'headings','headings':['结论']},'instr_types':['artifact-form']},
              {'id':'l','policy':{'kind':'answer_length','limit':800},'instr_types':['artifact-form']},
              {'id':'n','policy':{'kind':'no_lists'},'instr_types':['artifact-form']}]
        plan={'candidates':pool};p.assemble_matrix(plan,12,{'profile':'coverage'})
        singles={v['candidate_ids'][0] for v in plan['variants'] if v['tier']=='A'}
        self.assertTrue({'j','h'}<=singles)
        for v in plan['variants']:
            if len(v['candidate_ids'])>1:self.assertFalse({'j','h'}<=set(v['candidate_ids']))
    def test_weights_are_clean_and_positive_sum_one(self):
        plan=self.build(12);group=g.assemble(self.task,plan,'offline')
        for v in group['variants']:
            self.assertAlmostEqual(sum(r['weight'] for r in v['rubric'] if r['weight']>0),1)
            for r in v['rubric']:
                if r['layer']=='IF':self.assertEqual(r['weight'],round(r['weight'],6))
    def test_context_records_changes_hash_without_claiming_token_count(self):
        a=g.insert_prompt('基线','约束','middle',True,150)
        b=g.insert_prompt('基线','约束','middle',True,500)
        self.assertNotEqual(g.digest(a),g.digest(b));self.assertLess(len(a),len(b))
    def test_auto_generate_mock_review_and_checkpoint_resume(self):
        parent=self
        class Client:
            model='mock'
            generations=0
            def complete(self,messages):
                if messages[0]['content']==g.REVIEW_PROMPT:return approve(json.loads(messages[1]['content'])['plan'])
                self.generations+=1;return copy.deepcopy(parent.plan)
        client=Client();group=g.generate(self.task,client,'auto')
        self.assertEqual(len(group['variants']),18)
        self.assertEqual(group['construction_metadata']['generator_revision'],'5.8')
        self.assertEqual(group['baseline_fingerprint'],self.task['fingerprint'])
    def test_strict_coverage_rejects_not_fabricates(self):
        self.task['generation_options']={'strict_coverage':True,'min_families':10}
        with self.assertRaisesRegex(g.Invalid,'严格覆盖'):
            self.build(12)


if __name__=='__main__':unittest.main()
