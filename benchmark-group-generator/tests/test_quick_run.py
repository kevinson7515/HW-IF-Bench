import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import quick_run as q


class QuickRun(unittest.TestCase):
    def test_embedded_groups_are_sanitized_and_matched_by_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            query={'id':2,'user_query':'检查文件','attached_files':['a.py']}
            group={'task_id':2,'group_id':'G-2','user_query':'检查文件',
                   'attached_files':['a.py'],'system_prompt':'执行任务','tools':['file_read'],
                   'env':{'snapshot':'synthetic'},'baseline_fingerprint':{'tool_seq':['file_read']},
                   'variants':[{'instruction':'旧变体不应成为输入'}]}
            (root/'user_query_2.jsonl').write_text(json.dumps(query,ensure_ascii=False),encoding='utf-8')
            (root/'benchmark_groups_2.json').write_text(json.dumps([group],ensure_ascii=False),encoding='utf-8')
            rows,files,tag=q.prepare(root)
            self.assertEqual(tag,'embedded')
            self.assertEqual(len(files),2)
            self.assertEqual(rows[0]['fingerprint'],group['baseline_fingerprint'])
            self.assertNotIn('variants',rows[0])
            group['user_query']='不一致'
            (root/'benchmark_groups_2.json').write_text(json.dumps([group],ensure_ascii=False),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'不一致'):
                q.prepare(root)

    def test_multiple_fingerprints_are_chosen_not_hardcoded(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            query={'id':1,'user_query':'查询'}
            (root/'user_query.jsonl').write_text(json.dumps(query,ensure_ascii=False),encoding='utf-8')
            for model in ('deepseek','pangu'):
                fp={'task_id':1,'user_query':'查询','system_prompt':'执行任务',
                    'tools':['web_search'],'env':{'snapshot':'synthetic'},
                    'baseline_fingerprint':{'reply_len':10 if model=='deepseek' else 20}}
                (root/f'baseline_fingerprint_{model}.jsonl').write_text(json.dumps(fp,ensure_ascii=False),encoding='utf-8')
            with patch('quick_run.choose',side_effect=lambda items,label: items[0] if len(items)==1 else next(p for p in items if 'pangu' in p.name)):
                rows,files,tag=q.prepare(root)
            self.assertEqual(tag,'pangu')
            self.assertEqual(rows[0]['fingerprint']['reply_len'],20)
            self.assertEqual(len(files),2)

    def test_flat_config_requires_no_yaml_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'config.yaml'
            path.write_text('deepseek_api_key: "example-key"\nprofile: "workflow"\nmax_combination: 6\ncount: 5\n',encoding='utf-8')
            values=q.config(path)
            self.assertEqual(values['deepseek_api_key'],'example-key')
            self.assertEqual(values['profile'],'workflow')


if __name__=='__main__':
    unittest.main()
