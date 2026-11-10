import copy
import io
from http.client import IncompleteRead
import json
from pathlib import Path
import unittest
import tempfile
import threading
from contextlib import redirect_stderr
from unittest.mock import patch
from urllib.error import HTTPError

import generator as g

ROOT = Path(__file__).resolve().parents[1]


def approved_review(plan):
    return {'approved': True, 'tc_grounded': True, 'combinations_compatible': True, 'issues': [], 'pending_checks': [],
            'candidate_reviews': [{'id': c['id'], 'anti_default': True, 'task_preserving': True, 'reason': '测试用模拟审查'} for c in plan['candidates'] if c['id'] in {cid for v in plan['variants'] for cid in v['candidate_ids']}]}


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.task = g.normalize(g.read_json(ROOT / 'examples/demo_task.json'))[0]
        self.plan = g.read_json(ROOT / 'examples/demo_plan.json')

    def test_demo_end_to_end_and_prompt_hashes(self):
        g.check_plan(self.plan, self.task, 6)
        group = g.assemble(self.task, self.plan, 'mock')
        self.assertEqual(group['user_query'], self.task['user_query'])
        self.assertEqual(group['baseline']['effective_system_prompt'], self.task['system_prompt'])
        for v in group['variants']:
            self.assertEqual(v['system_prompt_sha256'], g.digest(v['effective_system_prompt']))
            self.assertAlmostEqual(sum(r['weight'] for r in v['rubric'] if r['weight'] > 0), 1)
            self.assertNotIn(v['variant_id'], v['source_variant_ids'])
        scored = g.score(group['variants'][0], {'final_answer': '固定数据输入使重复运行更容易比较。'},
                         {'S1-TC-1': 'FULL', 'S1-SE-1': 'NO'})
        self.assertTrue(scored['joint_success'])
        self.assertAlmostEqual(scored['weighted_score'], 1)

    def test_multiple_benchmark_domains_normalize(self):
        tasks = g.normalize([dict(self.task, task_id=i, group_id=f'G-demo-{i}',
                                  task_type=kind) for i, kind in enumerate(
                                      ('code_change', 'financial_analysis', 'customer_service'), 1)])
        self.assertEqual(len(tasks), 3)
        self.assertEqual(len({t['group_id'] for t in tasks}), 3)

    def test_id_join_ignores_order(self):
        tasks = [dict(self.task, task_id=1, group_id='G-1'), dict(self.task, task_id=2, group_id='G-2')]
        for task in tasks:task.pop('fingerprint',None)
        fps = [{'task_id': 2, 'fingerprint': {'n': 20}}, {'task_id': 1, 'fingerprint': {'n': 10}}]
        out = g.normalize(tasks, fps)
        self.assertEqual([t['fingerprint']['n'] for t in out], [10, 20])
        with self.assertRaises(g.Invalid):
            g.normalize(tasks, fps[:1])
        with self.assertRaises(g.Invalid):
            g.normalize(tasks, [fps[0], fps[0]])
        with self.assertRaisesRegex(g.Invalid,'fingerprint不一致'):
            g.normalize([dict(tasks[0],fingerprint={'n':99}),tasks[1]],fps)

    def test_duplicate_group_ids_rejected(self):
        with self.assertRaisesRegex(g.Invalid, 'group_id'):
            g.normalize([dict(self.task, task_id=1), dict(self.task, task_id=2)])

    def test_query_is_preserved_exactly(self):
        self.task['user_query'] = '  输入\n含换行\t  '
        self.assertEqual(g.normalize(self.task)[0]['user_query'], self.task['user_query'])

    def test_false_fingerprint_and_unknown_field_rejected(self):
        for field, value in [('reply_len', 123), ('nonexistent', 500)]:
            plan = copy.deepcopy(self.plan)
            plan['candidates'][0]['basis'][0].update(field=field, baseline_value=value)
            with self.assertRaises(g.Invalid):
                g.check_plan(plan, self.task, 6)

    def test_default_compliant_candidate_rejected(self):
        self.task['baseline_evidence'] = {'final_answer': '很短'}
        with self.assertRaisesRegex(g.Invalid, '基线已满足'):
            g.check_plan(self.plan, self.task, 6)

    def test_unknown_metric_rejected(self):
        self.plan['candidates'][0]['checks'][0]['rule'] = {'path': 'metrics.imaginary', 'op': 'eq', 'value': True}
        with self.assertRaisesRegex(g.Invalid, '未实现证据适配器'):
            g.check_plan(self.plan, self.task, 6)

    def test_nonexistent_tool_rejected(self):
        self.plan['candidates'][0]['checks'][0]['rule'] = {'path': 'trace.calls.*.name', 'op': 'count_le', 'match': 'fake_tool', 'value': 2}
        with self.assertRaisesRegex(g.Invalid, '不存在的工具'):
            g.check_plan(self.plan, self.task, 6)

    def test_conflict_and_combination_rules(self):
        self.plan['variants'][-1]['expected_behavior'] = None
        with self.assertRaisesRegex(g.Invalid, 'expected_behavior'):
            g.check_plan(self.plan, self.task, 6)
        self.setUp()
        self.plan['variants'][3]['candidate_ids'] = ['c1', 'c8']
        with self.assertRaisesRegex(g.Invalid, '独立A'):
            g.check_plan(self.plan, self.task, 6)

    def test_missing_negative_evidence_never_passes(self):
        rule = {'path': 'metrics.forbidden_count', 'op': 'eq', 'value': 0}
        with self.assertRaises(g.Invalid):
            g.evaluate_rule(rule, {})
        rule = {'any': [{'path': 'final_answer', 'op': 'eq', 'value': 'ok'}, rule]}
        with self.assertRaises(g.Invalid):
            g.evaluate_rule(rule, {'final_answer': 'ok'})

    def test_empty_artifacts_and_traversal_rejected(self):
        rule = {'path': 'artifacts.*.path', 'op': 'all_prefix', 'value': 'output/'}
        self.assertTrue(g.evaluate_rule(rule, {'artifacts': [{'path': 'output/chart.svg'}]}))
        with self.assertRaises(g.Invalid):
            g.evaluate_rule(rule, {'artifacts': []})
        self.assertFalse(g.evaluate_rule(rule, {'artifacts': [{'path': 'output/../secret.svg'}]}))

    def test_code_and_table_count_toward_length(self):
        rule = {'path': 'final_answer', 'op': 'length_le', 'value': 20}
        self.assertFalse(g.evaluate_rule(rule, {'final_answer': '简短\n```\n' + 'x' * 100 + '\n```'}))

    def test_tool_count_and_projection(self):
        rule = {'path': 'trace.calls.*.name', 'op': 'count_le', 'match': 'search', 'value': 1}
        self.assertFalse(g.evaluate_rule(rule, {'trace': {'calls': [{'name': 'search'}, {'name': 'search'}]}}))
        self.assertTrue(g.evaluate_rule(rule, {'trace': {'calls': []}}))

    def test_missing_se_or_if_means_ungradable(self):
        v = g.assemble(self.task, self.plan, 'mock')['variants'][0]
        result = g.score(v, {'final_answer': '答案'}, {'S1-TC-1': 'FULL'})
        self.assertEqual(result['status'], 'ungradable')
        self.assertIsNone(result['weighted_score'])
        result = g.score(v, {}, {'S1-TC-1': 'FULL', 'S1-SE-1': 'NO'})
        self.assertIsNone(result['IF'])

    def test_partial_tc_and_side_effect_penalty(self):
        v = g.assemble(self.task, self.plan, 'mock')['variants'][0]
        result = g.score(v, {'final_answer': '答案'}, {'S1-TC-1': 'PARTIAL', 'S1-SE-1': 'YES'})
        self.assertFalse(result['joint_success'])
        self.assertAlmostEqual(result['weighted_score'], .6)
        se = copy.deepcopy(v['rubric'][-1])
        for i in range(4):
            se = dict(se, id='extra' + str(i))
            v['rubric'].append(se)
        judges = {r['id']: ('FULL' if r['layer'] == 'TC' else 'YES') for r in v['rubric'] if r['method'] == 'llm_judge'}
        self.assertAlmostEqual(g.score(v, {'final_answer': '答案'}, judges)['weighted_score'], .5)

    def test_model_repair_after_invalid_json(self):
        class MockClient:
            model = 'mock'
            n = 0
            def complete(client, messages):
                if messages[0]['content'] == g.REVIEW_PROMPT:
                    return approved_review(json.loads(messages[1]['content'])['plan'])
                client.n += 1
                if client.n == 1:
                    return {'candidates': []}
                return self.plan
        client = MockClient()
        self.assertEqual(len(g.generate(self.task, client, 6)['variants']), 6)
        self.assertEqual(client.n, 2)

    def test_http_payload_and_json_parsing(self):
        response = {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(self.plan)}}]}
        with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'test-only'}), patch('generator.request.urlopen', return_value=io.BytesIO(json.dumps(response).encode())) as urlopen:
            client = g.DeepSeek('test-model', 'https://api.deepseek.com')
            out = client.complete([{'role': 'user', 'content': 'json'}])
            payload = json.loads(urlopen.call_args.args[0].data)
            self.assertEqual(payload['response_format'], {'type': 'json_object'})
            self.assertEqual(payload['model'], 'test-model')
            self.assertEqual(out['task_type'], self.plan['task_type'])

    def test_http_401_is_not_retried_or_leaked(self):
        with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'test-only'}), patch('generator.request.urlopen', side_effect=HTTPError('url', 401, 'private response', {}, None)) as urlopen:
            with self.assertRaisesRegex(g.Invalid, 'HTTP 401') as caught:
                g.DeepSeek('test', 'https://api.deepseek.com').complete([])
            self.assertNotIn('private response', str(caught.exception))
            self.assertEqual(urlopen.call_count, 1)

    def test_http_429_retry(self):
        response = {'choices': [{'finish_reason': 'stop', 'message': {'content': '{}'}}]}
        with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'test-only'}), patch('generator.time.sleep'), patch('generator.request.urlopen', side_effect=[HTTPError('url', 429, 'rate limited', {}, None), io.BytesIO(json.dumps(response).encode())]) as urlopen:
            self.assertEqual(g.DeepSeek('test', 'https://api.deepseek.com').complete([]), {})
            self.assertEqual(urlopen.call_count, 2)

    def test_multiline_concatenated_jsonl(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fingerprints.jsonl'
            path.write_text('\ufeff{\n "task_id": 1\n}\n{\n "task_id": 2\n}\n', encoding='utf-8')
            self.assertEqual(g.read_json(path), [{'task_id': 1}, {'task_id': 2}])
            path.write_text('{"task_id":1}\nBROKEN', encoding='utf-8')
            with self.assertRaises(json.JSONDecodeError):
                g.read_json(path)

    def test_actual_file_shape_merge(self):
        query = {'id': 1, 'user_query': self.task['user_query'], 'attached_files': ['attached_files/parser.py']}
        fp = {'task_id': 1, 'user_query': self.task['user_query'], 'system_prompt': 'baseline',
              'env_snapshot': 'model=x; sandbox=workspace-write', 'tools': ['file_read'],
              'baseline_fingerprint': {'tool_seq': ['file_read']}, 'execution_status': 'succeeded'}
        task = g.normalize([query], [fp])[0]
        self.assertEqual(task['task_id'], 1)
        self.assertEqual(task['env'], {'snapshot': fp['env_snapshot']})
        self.assertEqual(task['fingerprint'], fp['baseline_fingerprint'])
        self.assertEqual(task['tools'], ['file_read'])
        self.assertEqual(task['attached_files'], query['attached_files'])

    def test_id_alias_conflict_rejected(self):
        with self.assertRaisesRegex(g.Invalid, 'id与task_id'):
            g.normalize(dict(self.task, id='different'))

    def test_hash_mismatch_preserved_as_warning(self):
        task = g.normalize(dict(self.task, system_prompt_sha256='old-hash'))[0]
        self.assertEqual(task['source_system_prompt_sha256'], 'old-hash')
        self.assertEqual(task['system_prompt_sha256'], g.digest(task['system_prompt']))
        self.assertTrue(task['import_metadata']['warnings'])
        group = g.assemble(task, self.plan, 'mock')
        self.assertEqual(group['construction_metadata']['baseline_import']['source_system_prompt_sha256'], 'old-hash')

    def test_failed_baseline_rejected(self):
        with self.assertRaisesRegex(g.Invalid, '基线运行未成功'):
            g.normalize(dict(self.task, execution_status='failed'))

    def test_directory_import_uses_provided_fingerprint_without_run_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            q = {'id': 1, 'user_query': self.task['user_query'], 'attached_files': []}
            fp = dict(self.task, task_id=1, tools=['file_read'])
            (root/'user_query.jsonl').write_text(json.dumps(q), encoding='utf-8')
            (root/'baseline_fingerprint.jsonl').write_text(json.dumps(fp, indent=2), encoding='utf-8')
            run = root/'dsh-runs'/'000001-1'
            run.mkdir(parents=True)
            g.write_json(run/'task.json', q)
            g.write_json(run/'trace.json', {'lossless':False, 'trace':[
                {'role':'system','content':''},
                {'role':'assistant','reasoning_content':'must not import', 'tool_calls':[
                    {'id':'call1','function':{'name':'read','arguments':'{}'}}]}]})
            (run/'final.txt').write_text('真实回复', encoding='utf-8')
            tasks = g.load_tasks(root)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]['tools'], ['file_read'])
            self.assertNotIn('must not import', g.canonical(tasks))
            self.assertNotIn('baseline_evidence', tasks[0])
            self.assertNotIn('baseline_observation', tasks[0])
            self.assertEqual(tasks[0]['import_metadata']['fingerprint_provenance'],
                             'provided_by_user_not_independently_verified')
            self.assertEqual(set(tasks[0]['import_metadata']['files_sha256']),
                             {'user_query.jsonl','baseline_fingerprint.jsonl'})
            fp['user_query'] = 'different'
            g.write_json(root/'baseline_fingerprint.jsonl', fp)
            with self.assertRaisesRegex(g.Invalid, '文本不一致'):
                g.load_tasks(root)

    def test_progress_flushes_to_console_and_log(self):
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp)/'progress.log'
            console = io.StringIO()
            with redirect_stderr(console):
                progress = g.Progress(log_file=log)
                progress('开始 task_id=1')
                progress('已保存6个变体')
            self.assertIn('[------------------------]', console.getvalue())
            self.assertIn('已保存6个变体', log.read_text(encoding='utf-8'))
            with redirect_stderr(console):
                g.Progress(quiet=True, log_file=log)('仅日志')
            self.assertNotIn('仅日志', console.getvalue())
            self.assertIn('仅日志', log.read_text(encoding='utf-8'))

    def test_waiting_notifies_and_stops_even_on_exception(self):
        seen, event = [], threading.Event()
        def notify(message):
            seen.append(message)
            event.set()
        waiting = g.Waiting(notify, interval=.01)
        with self.assertRaisesRegex(RuntimeError, 'test'):
            with waiting:
                self.assertTrue(event.wait(1))
                raise RuntimeError('test')
        self.assertFalse(waiting.thread.is_alive())
        self.assertIn('仍在等待响应', seen[0])

    def test_repair_progress_explains_validation_failure(self):
        class MockClient:
            model = 'mock'
            n = 0
            def complete(client, messages):
                if messages[0]['content'] == g.REVIEW_PROMPT:
                    return approved_review(json.loads(messages[1]['content'])['plan'])
                client.n += 1
                return {} if client.n == 1 else self.plan
        events = []
        g.generate(self.task, MockClient(), 6, progress=events.append)
        self.assertTrue(any('本轮未通过' in event for event in events))
        self.assertTrue(any('校验通过：8 条候选' in event for event in events))

    def test_request_retry_progress_does_not_leak_credentials(self):
        events = []
        response = {'choices': [{'finish_reason': 'stop', 'message': {'content': '{}'}}]}
        with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'secret-test-key'}), patch('generator.time.sleep'), patch('generator.request.urlopen', side_effect=[HTTPError('url', 429, 'private-body', {}, None), io.BytesIO(json.dumps(response).encode())]):
            g.DeepSeek('test', 'https://api.deepseek.com', progress=events.append).complete([])
        text = '\n'.join(events)
        self.assertIn('HTTP 429', text)
        self.assertIn('后重试', text)
        self.assertIn('已收到 DeepSeek 响应', text)
        self.assertNotIn('secret-test-key', text)
        self.assertNotIn('private-body', text)

    def test_incomplete_response_retries_same_deepseek_request(self):
        response={'choices':[{'finish_reason':'stop','message':{'content':'{"ok":true}'}}]}
        events=[]
        with patch.dict('os.environ',{'DEEPSEEK_API_KEY':'test-key'}), patch('generator.time.sleep'), \
             patch('generator.request.urlopen',side_effect=[IncompleteRead(b'{',12),io.BytesIO(json.dumps(response).encode())]) as api:
            result=g.DeepSeek('test','https://api.deepseek.com',progress=events.append).complete([])
        self.assertEqual(result,{'ok':True})
        self.assertEqual(api.call_count,2)
        self.assertTrue(any('响应传输中断' in event for event in events))

    def test_batch_progress_and_resume_without_network(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'groups.json'
            console = io.StringIO()
            argv = ['generator.py', 'generate', '--input', str(ROOT/'examples/demo_task.json'), '--output', str(output)]
            with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'test-key'}), patch('generator.DeepSeek.complete', side_effect=lambda messages: approved_review(json.loads(messages[1]['content'])['plan']) if messages[0]['content'] == g.REVIEW_PROMPT else copy.deepcopy(self.plan)), patch('sys.argv', argv), redirect_stderr(console):
                g.main()
            self.assertIn('[########################] 1/1', console.getvalue())
            self.assertIn('Summary: generated=1', console.getvalue())
            self.assertTrue(g.run_files(output)['log'].exists())
            self.assertTrue(g.run_files(output)['metadata'].exists())
            self.assertNotIn('construction_metadata',g.read_json(output)[0])
            with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'test-key'}), patch('generator.DeepSeek.complete') as api, patch('sys.argv', argv+['--resume']), redirect_stderr(console):
                g.main()
                api.assert_not_called()
            self.assertIn('skipped=1', console.getvalue())

    def test_named_fingerprints_selected_without_run_scan(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for model in ('deepseek', 'pangu'):
                task = dict(self.task, task_id=1, run_group=model)
                g.write_json(root/f'baseline_fingerprint_{model}.jsonl', task)
                run = root/'dsh-runs'/model/'000001-1'
                g.write_json(run/'task.json', {'id':1,'user_query':task['user_query']})
                (run/'final.txt').write_text(model, encoding='utf-8')
            with self.assertRaisesRegex(g.Invalid, '--fingerprints'):
                g.load_tasks(root)
            for model in ('deepseek', 'pangu'):
                task = g.load_tasks(root, f'baseline_fingerprint_{model}.jsonl')[0]
                self.assertNotIn('baseline_observation',task)
                self.assertTrue(task['baseline_fingerprint_ref'].startswith(f'baseline_fingerprint_{model}.jsonl'))

    def test_unique_named_fingerprint_auto_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            g.write_json(root/'baseline_fingerprint_custom.jsonl', self.task)
            self.assertEqual(g.load_tasks(root)[0]['task_id'], self.task['task_id'])

    def test_run_group_is_metadata_and_does_not_open_run_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            g.write_json(root/'baseline_fingerprint.jsonl', dict(self.task, run_group='../other'))
            self.assertEqual(g.load_tasks(root)[0]['run_group'],'../other')


if __name__ == '__main__':
    unittest.main()
