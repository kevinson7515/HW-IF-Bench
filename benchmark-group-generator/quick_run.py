"""One-command runner for supplied query + fingerprint datasets.

Only reads supplied JSON/JSONL. Never extracts a baseline from dsh-runs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import generator as g

ROOT = Path(__file__).resolve().parent
ALLOWED_CONFIG = {'deepseek_api_key', 'deepseek_model', 'profile', 'count', 'max_combination'}


def config(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f'缺少配置文件：{path}')
    values = {}
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        text = line.strip()
        if not text or text.startswith('#'):
            continue
        if ':' not in text:
            raise ValueError(f'config.yaml 第{number}行需要 key: value')
        key, raw = (part.strip() for part in text.split(':', 1))
        if key not in ALLOWED_CONFIG or key in values:
            raise ValueError(f'config.yaml 第{number}行字段未知或重复：{key}')
        if raw.startswith('"'):
            values[key] = json.loads(raw)
        elif raw.startswith("'") and raw.endswith("'"):
            values[key] = raw[1:-1]
        else:
            values[key] = raw.split(' #', 1)[0].strip()
    if values.get('profile', 'balanced') not in {'balanced', 'coverage', 'stress', 'workflow'}:
        raise ValueError('profile必须是balanced、coverage、stress或workflow')
    maximum = int(values.get('max_combination', '6'))
    if not 2 <= maximum <= 6:
        raise ValueError('max_combination必须是2–6')
    values['max_combination'] = maximum
    count = values.get('count', '5')
    if not (str(count).isdigit() and 4 <= int(count) <= 6):
        raise ValueError('快捷入口每个query生成4–6个变体，请在config.yaml中设置count: 4、5或6')
    return values


def choose(items: list[Path], label: str) -> Path:
    if not items:
        raise ValueError(f'没有找到{label}')
    if len(items) == 1:
        return items[0]
    if not sys.stdin.isatty():
        raise ValueError(f'找到多份{label}，请在交互终端选择：' + '、'.join(p.name for p in items))
    print(f'请选择{label}：')
    for number, item in enumerate(items, 1):
        print(f'  {number}. {item.name}')
    while True:
        answer = input('输入序号：').strip()
        if answer.isdigit() and 1 <= int(answer) <= len(items):
            return items[int(answer)-1]
        print('请输入列表中的序号。')


def key(row: dict) -> str:
    value = row.get('task_id', row.get('id'))
    if value is None:
        raise ValueError('任务缺少task_id/id')
    return str(value)


def index(rows: list[dict], label: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(label + '必须是对象数组')
        task_id = key(row)
        if task_id in result:
            raise ValueError(f'{label}存在重复task_id={task_id}')
        result[task_id] = row
    return result


def source_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode('utf-8'))
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()[:10]


def prepare(directory: Path) -> tuple[list[dict], list[Path], str]:
    queries = sorted(directory.glob('user_query*.jsonl'))
    query_file = choose(queries, 'user_query文件') if queries else None
    fingerprint_files = sorted(directory.glob('baseline_fingerprint*.jsonl'))
    groups_files = sorted(directory.glob('benchmark_groups*.json'))
    if fingerprint_files:
        fp_file = choose(fingerprint_files, 'fingerprint文件')
        if not query_file:
            raise ValueError('单独提供fingerprint时，目录中还需要user_query*.jsonl')
        rows = g.load_tasks(query_file, fp_file)
        return rows, [query_file, fp_file], fp_file.stem.removeprefix('baseline_fingerprint').strip('_') or 'provided'
    groups_file = choose(groups_files, '含fingerprint的benchmark_groups文件')
    groups = g.records(g.read_json(groups_file))
    by_group = index(groups, 'benchmark_groups')
    by_query = index(g.read_json(query_file), 'user_query') if query_file else {}
    if query_file and set(by_group) != set(by_query):
        raise ValueError('benchmark_groups与user_query的任务ID集合不一致')
    fields = ('task_id', 'group_id', 'task_type', 'system_prompt', 'user_query', 'tools',
              'env', 'env_snapshot', 'attached_files', 'benchmark', 'baseline_fingerprint',
              'capabilities', 'evidence_contract', 'task_contract', 'execution_status')
    cleaned = []
    for task_id, group in by_group.items():
        row = {name: group[name] for name in fields if name in group}
        row['task_id'] = group.get('task_id', group.get('id'))
        if not isinstance(row.get('baseline_fingerprint'), dict) or not row['baseline_fingerprint']:
            raise ValueError(f'task_id={task_id}缺少非空baseline_fingerprint')
        if query_file:
            query = by_query[task_id]
            if row.get('user_query') != query.get('user_query'):
                raise ValueError(f'task_id={task_id}的user_query文本不一致')
            if 'attached_files' in query and row.get('attached_files', []) != query['attached_files']:
                raise ValueError(f'task_id={task_id}的attached_files不一致')
        row['baseline_fingerprint_ref'] = str(groups_file.resolve()) + '#task_id=' + task_id
        cleaned.append(row)
    return g.normalize(cleaned), [groups_file] + ([query_file] if query_file else []), 'embedded'


def main() -> int:
    parser = argparse.ArgumentParser(description='选择data目录，直接生成benchmark_groups；不读取dsh-runs')
    parser.add_argument('data_dir', nargs='?', help='数据目录；不填时从data子目录中选择')
    parser.add_argument('--check', action='store_true', help='只匹配并校验输入，不调用DeepSeek')
    parser.add_argument('--task-ids', help='只生成指定任务ID，多个ID用逗号分隔')
    parser.add_argument('--new-run', action='store_true', help='同一数据集重新开始一次新生成；默认继续最近一次运行')
    args = parser.parse_args()
    settings = config(ROOT / 'config.yaml')
    data_root = ROOT / 'data'
    directory = Path(args.data_dir) if args.data_dir else choose(sorted(p for p in data_root.iterdir() if p.is_dir()), '数据目录')
    if not directory.is_absolute():
        directory = (ROOT / directory).resolve()
    if not directory.is_dir():
        raise ValueError(f'数据目录不存在：{directory}')
    rows, sources, tag = prepare(directory)
    fingerprint = source_hash(sources)
    name = re.sub(r'[^A-Za-z0-9_-]+', '_', directory.name).strip('_') or 'dataset'
    work_dir = ROOT / 'generated'
    output_dir = ROOT / 'output'
    work_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    prepared = work_dir / f'{name}_{tag}_input.json'
    g.write_json(prepared, rows)
    if args.check:
        print(f'输入校验通过：{len(rows)}个任务；来源：' + '、'.join(p.name for p in sources), flush=True)
        return 0
    profile = settings.get('profile', 'balanced')
    if profile == 'workflow':
        missing = [str(r['task_id']) for r in rows if not r.get('evidence_contract', {}).get('trace.events', {}).get('implemented')]
        if missing:
            raise ValueError('workflow模式需要实际运行事件适配器；这些任务未声明：' + '、'.join(missing[:8]) + '。当前数据可先使用profile: balanced生成常规变体。')
    api_key = settings.get('deepseek_api_key', '')
    if not api_key or api_key.startswith('请填入'):
        raise ValueError('请先在config.yaml的deepseek_api_key中填写DeepSeek API Key；--check无需密钥')
    selected = ('_task_' + re.sub(r'[^A-Za-z0-9_-]+', '_', args.task_ids)) if args.task_ids else ''
    source_label='' if tag=='embedded' else '_'+re.sub(r'[^A-Za-z0-9_-]+','_',tag)
    prefix = f'benchmark_{name}{source_label}{selected}_'
    existing = sorted((p for p in output_dir.glob(prefix + '*.json')
                       if re.fullmatch(re.escape(prefix)+r'\d{8}_\d{6}(?:_\d+)?\.json',p.name)), key=lambda p:p.name)
    compatible=[]
    for path in existing:
        meta=g.run_files(path)['metadata']
        if meta.exists():
            try:
                info=g.read_json(meta)
                if (info.get('generator_revision')=='5.8' and info.get('source_hash')==fingerprint
                    and info.get('model')==settings.get('deepseek_model','deepseek-flash')
                    and info.get('count')==int(settings['count']) and info.get('profile')==profile):
                    compatible.append(path)
            except (ValueError,OSError):
                continue
    started_at = datetime.now(timezone(timedelta(hours=8)))
    output = compatible[-1] if compatible and not args.new_run else output_dir / (prefix + started_at.strftime('%Y%m%d_%H%M%S') + '.json')
    if output.exists() and (args.new_run or not compatible):
        suffix=2
        while output.exists():
            output=output_dir / (prefix + started_at.strftime('%Y%m%d_%H%M%S') + f'_{suffix}.json')
            suffix+=1
    cmd = [sys.executable, str(ROOT / 'generator.py'), 'generate', '--input', str(prepared),
           '--output', str(output), '--model', settings.get('deepseek_model', 'deepseek-flash'),
           '--profile', profile, '--count', settings.get('count', '5'),
           '--max-combination', str(settings['max_combination']), '--source-hash', fingerprint, '--resume']
    if args.task_ids:
        cmd += ['--task-ids', args.task_ids]
    env = os.environ.copy()
    env['DEEPSEEK_API_KEY'] = api_key
    return subprocess.call(cmd, cwd=ROOT, env=env)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, g.Invalid, json.JSONDecodeError) as exc:
        print('错误：' + str(exc), file=sys.stderr)
        raise SystemExit(2)
