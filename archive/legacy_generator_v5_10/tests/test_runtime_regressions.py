import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import generator as g
from policies import assemble_matrix, tool_name_map

ROOT = Path(__file__).resolve().parents[1]


def approve(plan):
    return {'approved':True,'tc_grounded':True,'combinations_compatible':True,'issues':[], 'pending_checks':[],
            'candidate_reviews':[{'id':c['id'],'anti_default':True,'task_preserving':True,'reason':'模拟审查依据'} for c in plan['candidates'] if c['id'] in {cid for v in plan['variants'] for cid in v['candidate_ids']}]}


class RuntimeRegressions(unittest.TestCase):
    def setUp(self):
        self.task = g.normalize(g.read_json(ROOT/'examples/demo_task.json'))[0]
        self.plan = g.read_json(ROOT/'examples/demo_plan.json')

    def test_truncation_retries_same_request_with_larger_budget(self):
        first = {'choices':[{'finish_reason':'length','message':{'content':''}}], 'usage':{'completion_tokens':32768}}
        second = {'choices':[{'finish_reason':'stop','message':{'content':'{"approved":true}'}}]}
        with patch.dict('os.environ',{'DEEPSEEK_API_KEY':'test'}), patch('generator.request.urlopen',side_effect=[io.BytesIO(json.dumps(first).encode()),io.BytesIO(json.dumps(second).encode())]) as fetch:
            messages = [{'role':'user','content':'json review'}]
            result = g.DeepSeek('test','https://api.deepseek.com').complete(messages)
            self.assertEqual(result, {'approved':True})
            bodies = [json.loads(call.args[0].data) for call in fetch.call_args_list]
            self.assertEqual([b['max_tokens'] for b in bodies], [32768,65536])
            self.assertEqual(bodies[0]['messages'], bodies[1]['messages'])
            self.assertEqual(bodies[0]['reasoning_effort'], 'low')
            self.assertNotIn('temperature', bodies[0])

    def test_truncation_at_cap_is_infrastructure_failure(self):
        response = {'choices':[{'finish_reason':'length','message':{'content':''}}]}
        with patch.dict('os.environ',{'DEEPSEEK_API_KEY':'test'}), patch('generator.request.urlopen',return_value=io.BytesIO(json.dumps(response).encode())):
            with self.assertRaises(g.RequestFailed):
                g.DeepSeek('test','https://api.deepseek.com',max_tokens=65536).complete([])

    def test_review_checkpoint_resumes_without_regenerating_candidates(self):
        parent = self
        class Client:
            model = 'mock'
            generations = 0
            reviews = 0
            def complete(self, messages):
                if messages[0]['content'] == g.REVIEW_PROMPT:
                    self.reviews += 1
                    if self.reviews == 1:
                        raise g.RequestFailed('模拟审查请求截断')
                    return approve(json.loads(messages[1]['content'])['plan'])
                self.generations += 1
                return copy.deepcopy(parent.plan)
        client = Client()
        with tempfile.TemporaryDirectory() as temp:
            checkpoint = Path(temp)/'candidate.json'
            with self.assertRaises(g.RequestFailed):
                g.generate(self.task,client,6,checkpoint=checkpoint)
            self.assertEqual(g.read_json(checkpoint)['state'],'awaiting_review')
            group = g.generate(self.task,client,6,checkpoint=checkpoint)
            self.assertEqual(len(group['variants']),6)
            self.assertEqual(client.generations,1)
            self.assertEqual(client.reviews,2)

    def test_bad_model_matrix_is_replaced_with_valid_local_references(self):
        self.plan['variants'] = [{'tier':'B','candidate_ids':['nonexistent']}]
        assemble_matrix(self.plan,6)
        g.check_plan(self.plan,self.task,6)
        singles = {v['candidate_ids'][0] for v in self.plan['variants'] if v['tier']=='A'}
        self.assertGreaterEqual(len({cid for v in self.plan['variants'] for cid in v['candidate_ids']}),4)
        used={cid for v in self.plan['variants'] for cid in v['candidate_ids']}
        chosen = {f for c in self.plan['candidates'] if c['id'] in used for f in c['instr_types']}
        self.assertGreaterEqual(len(chosen),2)

    def test_compact_review_excludes_assertion_code_and_adds_checked_aliases(self):
        self.task['tools'] = ['file_read']
        self.task['fingerprint']['tool_seq'] = ['file_read']
        self.task['baseline_observation'] = {'raw_tool_calls':[{'name':'read','args':'huge-content-not-needed'}], 'final_answer':'实际回复'}
        captured = []
        parent = self
        class Client:
            def complete(self, messages):
                captured.extend(messages)
                return approve(json.loads(messages[1]['content'])['plan'])
        g.semantic_review(self.plan,self.task,Client())
        payload = json.loads(captured[1]['content'])
        self.assertEqual(payload['task']['baseline_observation']['tool_name_map'],{'read':'file_read'})
        self.assertNotIn('checks',payload['plan']['candidates'][0])
        self.assertNotIn('huge-content-not-needed',captured[1]['content'])

    def test_alias_mapping_does_not_guess_unknown_tools(self):
        self.assertEqual(tool_name_map(['mcp__e2b__execute_python'],['python_exec']),{'mcp__e2b__execute_python':'python_exec'})
        with self.assertRaises(ValueError):
            tool_name_map(['unknown_python'],['python_exec'])


if __name__ == '__main__':
    unittest.main()
