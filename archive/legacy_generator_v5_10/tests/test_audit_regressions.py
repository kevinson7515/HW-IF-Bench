"""Regression cases from the user's actual generated benchmark audit."""
import copy
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stderr

import generator as g
from policies import compile_policy, prepare_plan, validate_combination

ROOT = Path(__file__).resolve().parents[1]


class AuditRegressions(unittest.TestCase):
    def setUp(self):
        self.task = g.normalize(g.read_json(ROOT/'examples/demo_task.json'))[0]
        self.task['tools'] = ['web_search', 'web_fetch', 'file_edit', 'python_exec']

    def result(self, policy, evidence):
        compiled = compile_policy(policy, self.task)
        return all(g.evaluate_rule(c['rule'], evidence) for c in compiled['checks'])

    def test_object_count_legacy_rule_is_rejected_not_silently_zero(self):
        bad = {'path':'trace.calls','op':'count_eq','match':{'name':'web_search'},'value':0}
        with self.assertRaisesRegex(g.Invalid, '标量'):
            g.evaluate_rule(bad, {'trace':{'calls':[{'name':'web_search','args':{}}]}})

    def test_budget_counts_complete_call_records(self):
        policy = {'kind':'tool_budget','tools':['web_search'],'limit':4}
        calls = [{'name':'web_search','args':{'query':'q'},'result':'data','round':0,'status':'ok'}]*5
        self.assertFalse(self.result(policy, {'trace':{'calls':calls}}))
        self.assertTrue(self.result(policy, {'trace':{'calls':calls[:4]}}))

    def test_forbidden_tool_with_extra_fields_fails(self):
        self.assertFalse(self.result({'kind':'tool_forbidden','tools':['web_search']},
            {'trace':{'calls':[{'name':'web_search','args':{},'result':'data'}]}}))

    def test_no_raw_source_regex_for_chart(self):
        with self.assertRaisesRegex(g.Invalid, '源码正则'):
            g.evaluate_rule({'path':'code','op':'regex','value':'up.*green'}, {'code':'# up = green'})
        with self.assertRaisesRegex(ValueError, '适配器'):
            compile_policy({'kind':'chart_colors'}, self.task)

    def test_verified_chart_metric_not_comment_or_exact_hex(self):
        self.task['capabilities'] = {'rendered_chart':True}
        self.task['evidence_contract'] = {'metrics.chart_candle_colors':{'implemented':True,'extractor':'my_actual_renderer','source':'OHLC-linked rendered candle nodes'}}
        policy = {'kind':'chart_colors'}
        with self.assertRaises(g.Invalid):
            self.result(policy, {'code':'# up=green, down=red'})
        self.assertTrue(self.result(policy, {'metrics':{'chart_candle_colors':{'up':'green','down':'red','rendered':True}}}))
        self.assertFalse(self.result(policy, {'metrics':{'chart_candle_colors':{'up':'red','down':'green','rendered':True}}}))

    def test_source_fetch_and_final_citation_both_checked(self):
        policy = {'kind':'source_blacklist','domains':['zhihu.com','xiaohongshu.com','xhslink.com'],'keywords':['知乎','小红书']}
        for call in [
            {'name':'web_fetch','args':{'url':'https://zhuanlan.zhihu.com/p/1'}},
            {'name':'web_search','args':{'query':'知乎 用户体验'}},
            {'name':'web_fetch','args':{'url':'https://xhslink.com/a'}}]:
            self.assertFalse(self.result(policy, {'final_answer':'没有域名','trace':{'calls':[call]}}))
        self.assertFalse(self.result(policy, {'final_answer':'https://www.xiaohongshu.com/a','trace':{'calls':[]}}))
        self.assertTrue(self.result(policy, {'final_answer':'已排除知乎，以下使用其他来源。','trace':{'calls':[
            {'name':'web_search','args':{'query':'review -site:zhihu.com'}}]}}))
        self.assertTrue(self.result(policy, {'final_answer':'https://zhihu.com.example.org/a','trace':{'calls':[]}}))
        with self.assertRaises(ValueError):
            self.result(policy, {'final_answer':'内容','trace':{'calls':[{'name':'web_fetch'}]}})

    def test_no_markdown_table_accepts_paragraph_rejects_both_forms(self):
        policy = {'kind':'no_markdown_table'}
        self.assertTrue(self.result(policy, {'final_answer':'空输入验证通过。'}))
        for text in ['输入 | 结果\n--- | ---\n空输入 | 通过', '| 输入 | 结果 |\n| :--- | ---: |\n| 空 | 通过 |']:
            self.assertFalse(self.result(policy, {'final_answer':text}))

    def test_readonly_and_python_write_need_real_capabilities(self):
        for kind in ('first_round_readonly','modify_via_python'):
            with self.assertRaisesRegex(ValueError, '适配器'):
                compile_policy({'kind':kind}, self.task)
        self.task['fingerprint']['modified_path'] = 'parser.py'
        with self.assertRaisesRegex(ValueError, '本地修改路径'):
            compile_policy({'kind':'tool_forbidden','tools':['file_edit']}, self.task)

    def test_combination_cannot_ban_required_tool(self):
        with self.assertRaisesRegex(ValueError, '同时禁止与要求'):
            validate_combination([{'policy':{'kind':'tool_forbidden','tools':['web_search']}},
                                  {'policy':{'kind':'first_tool','tools':['web_search']}}])

    def test_model_cannot_add_unchecked_instruction(self):
        plan = g.read_json(ROOT/'examples/demo_plan.json')
        plan['candidates'][0]['instruction'] += ' 并只引用官方来源。'
        with self.assertRaisesRegex(g.Invalid, '偏离本地policy模板'):
            g.check_plan(plan, self.task, 6)
        prepare_plan(plan, self.task)
        self.assertNotIn('官方', plan['candidates'][0]['instruction'])

    def test_semantic_review_cannot_be_skipped_or_partial(self):
        plan = g.read_json(ROOT/'examples/demo_plan.json')
        class Client:
            def complete(self, messages):
                return {'approved':True,'candidate_reviews':[]}
        with self.assertRaisesRegex(g.Invalid, '未覆盖全部'):
            g.semantic_review(plan, self.task, Client())

    def test_review_ignores_conflict_between_independent_variants(self):
        plan = {'variants': [{'candidate_ids': ['c15']}, {'candidate_ids': ['c17']}],
                'task_completion': {'assert': '完成任务'}}
        verdict = {'candidate_reviews': [
            {'id': cid, 'anti_default': True, 'task_preserving': True, 'reason': '可行'}
            for cid in ('c15', 'c17')],
            'tc_grounded': True, 'combinations_compatible': False,
            'issues': [{'scope': 'combination', 'candidate_ids': ['c15', 'c17'],
                        'reason': 'JSON与Markdown标题不能同时满足'}], 'pending_checks': []}
        rejected, combinations = g.validate_review(verdict, plan, {'c15', 'c17'})
        self.assertEqual((rejected, combinations), ([], []))
        self.assertTrue(verdict['combinations_compatible'])
        self.assertEqual(verdict['issues'], [])
        self.assertEqual(len(verdict['ignored_cross_variant_issues']), 1)

        combined = copy.deepcopy(plan)
        combined['variants'] = [{'candidate_ids': ['c15', 'c17']}]
        actual = copy.deepcopy(verdict)
        actual.pop('ignored_cross_variant_issues')
        actual['issues'] = [{'scope': 'combination', 'candidate_ids': ['c15', 'c17'],
                             'reason': 'JSON与Markdown标题不能同时满足'}]
        actual['combinations_compatible'] = False
        self.assertEqual(g.validate_review(actual, combined, {'c15', 'c17'})[1], [['c15', 'c17']])

    def test_chart_tc_does_not_copy_baseline_filename_or_metric_count(self):
        plan = g.read_json(ROOT/'examples/demo_plan.json')
        self.task['task_type'] = 'analysis+chart_generation'
        self.task['fingerprint']['chart_outputs'] = ['fixed_baseline_name.svg']
        g.ground_task_completion(plan, self.task)
        self.assertNotIn('fixed_baseline_name', g.canonical(plan['task_completion']))
        self.assertIn('rendered_artifacts', plan['task_completion']['required_evidence'])

    def test_code_tc_requires_actual_file_validation_without_none_contract(self):
        plan = g.read_json(ROOT/'examples/demo_plan.json')
        self.task['task_type'] = 'bug_fix'
        g.ground_task_completion(plan, self.task)
        self.assertIn('validation_trace', plan['task_completion']['required_evidence'])
        self.assertNotIn('None', plan['task_completion']['assert'])
        variant = g.assemble(self.task, plan, 'mock')['variants'][0]
        scored = g.score(variant, {'final_answer':'修好了'}, {'S1-TC-1':'FULL','S1-SE-1':'NO'})
        self.assertEqual(scored['status'], 'ungradable')
        self.assertIsNone(scored['weighted_score'])

    def test_old_outputs_cannot_resume_past_new_validation(self):
        task = g.normalize(g.read_json(ROOT/'examples/demo_task.json'))[0]
        plan = g.read_json(ROOT/'examples/demo_plan.json')
        group = g.assemble(task, plan, 'deepseek-flash')
        group['construction_metadata']['pipeline_schema_version'] = '3.0'
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'old.json'
            g.write_json(output, [group])
            argv = ['generator.py','generate','--input',str(ROOT/'examples/demo_task.json'),'--output',str(output),'--resume']
            with patch.dict('os.environ',{'DEEPSEEK_API_KEY':'test-only'}), patch('sys.argv',argv), redirect_stderr(io.StringIO()):
                with self.assertRaisesRegex(g.Invalid, '缺少对应'):
                    g.main()

    def test_all_twelve_families_have_tested_template_support(self):
        self.task['capabilities'] = {'rendered_chart':True,'round_effects':True,'multi_round_scheduling':True,'local_python_write_bridge':True}
        self.task['evidence_contract'] = {p:{'implemented':True,'extractor':'test_adapter','source':'external artifacts'} for p in
            ['metrics.chart_grid_visible','metrics.chart_candle_colors','metrics.first_round_readonly','metrics.modified_via_python']}
        policies = [{'kind':'tool_budget','tools':['web_search'],'limit':4},
            {'kind':'answer_length','limit':200}, {'kind':'no_exclamation'}, {'kind':'forbidden_words','words':['套话']},
            {'kind':'source_blacklist','domains':['zhihu.com'],'keywords':['知乎']},
            {'kind':'chart_colors'}, {'kind':'first_round_readonly'}, {'kind':'modify_via_python'},
            {'kind':'python_imports_exclude','modules':['pandas']}, {'kind':'artifact_directory','directory':'output'},
            {'kind':'required_section','heading':'数据口径说明'}, {'kind':'forbidden_read_paths','tools':['web_fetch'],'patterns':['.env','*.key']},
            {'kind':'chart_no_grid'}]
        families = set()
        for policy in policies:
            compiled = compile_policy(policy, self.task)
            families.update(compiled['instr_types'])
            self.assertEqual(g.self_test_policy(policy, compiled, g.evaluate_rule)['status'], 'passed')
        self.assertEqual(families, g.FAMILIES - g.EXTRA_FAMILIES)

    def test_ast_ignores_comment_but_rejects_actual_import(self):
        policy = {'kind':'python_imports_exclude','modules':['pandas']}
        self.assertTrue(self.result(policy, {'code':'# import pandas\nx = 1'}))
        self.assertFalse(self.result(policy, {'code':'from pandas.core import frame'}))
        with self.assertRaises(g.Invalid):
            self.result(policy, {'code':'bad Python !'})

    def test_required_section_with_blank_lines_and_real_body(self):
        policy = {'kind':'required_section','heading':'数据口径说明'}
        self.assertTrue(self.result(policy, {'final_answer':'## 数据口径说明\n\n实际说明。'}))
        self.assertFalse(self.result(policy, {'final_answer':'## 数据口径说明\n\n## 其他\n其他内容'}))
        self.assertFalse(self.result(policy, {'final_answer':'```text\n## 数据口径说明\n伪造章节\n```'}))

    def test_headings_inside_code_do_not_count_as_document_structure(self):
        policy = {'kind':'headings','headings':['结论','证据']}
        self.assertFalse(self.result(policy, {'final_answer':'```\n## 结论\n文字\n## 证据\n文字\n```'}))


if __name__ == '__main__':
    unittest.main()
