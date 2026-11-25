"""Reviewed constraint templates. Models select parameters; local code owns instructions and rules."""
import fnmatch
from itertools import combinations
import re
from urllib.parse import urlsplit, unquote


def need(ok, message):
    if not ok:
        raise ValueError(message)


def markdown_lines(text):
    """Ignore fenced code when interpreting rendered Markdown structure."""
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match.group(1)[0]
            fence = None if fence == marker else marker
            lines.append('')
        else:
            lines.append(line if fence is None else '')
    return lines


def markdown_table(text):
    # CommonMark/GFM tables allow omitted outer pipes.
    lines = markdown_lines(text)
    for i in range(1, len(lines)):
        cells = [s.strip() for s in lines[i].strip().strip('|').split('|')]
        if '|' in lines[i - 1] and len(cells) >= 2 and all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
            return True
    return False


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


TOOL_ALIASES = {'read':'file_read', 'edit':'file_edit', 'write':'file_write', 'grep':'file_search',
                'glob':'file_glob', 'working_directory':'cwd_inspect', 'todo_write':'task_planning',
                'list_mcp_resources':'mcp_resource_list', 'list_mcp_resource_templates':'mcp_template_list',
                'mcp__e2b__execute_python':'python_exec', 'mcp__serper__google_search':'web_search'}


def tool_name_map(raw_names, available_tools):
    result = {}
    for name in raw_names:
        target = name if name in available_tools else TOOL_ALIASES.get(name)
        need(target in available_tools, '没有已知工具名称映射：' + str(name))
        result[name] = target
    return result


def domain_used(text, domains, keywords=(), search=False):
    text = unquote(text).lower()
    # A search exclusion is not a request to use the excluded site.
    if search:
        text = re.sub(r'-site:[\w.-]+', '', text)
    for url in re.findall(r'https?://[^\s<>"\]\)]+', text):
        try:
            host = (urlsplit(url).hostname or '').rstrip('.').lower()
        except ValueError:
            continue
        if any(host == d or host.endswith('.' + d) for d in domains):
            return True
    if search:
        return any(k.lower() in text for k in keywords) or any(
            re.search(r'(?<![\w.-])(?:[\w-]+\.)*' + re.escape(d) + r'(?![\w.-])', text) for d in domains)
    return False


def sources_allowed(evidence, domains, keywords):
    need(isinstance(evidence, dict) and isinstance(evidence.get('final_answer'), str), '缺少final_answer')
    calls = evidence.get('trace', {}).get('calls')
    need(isinstance(calls, list), '缺少完整trace.calls')
    for call in calls:
        need(isinstance(call, dict) and 'name' in call and 'args' in call, '调用记录缺少name/args')
        search = 'search' in call['name'].lower()
        for text in strings(call['args']):
            if domain_used(text, domains, keywords, search=search):
                return False
    return not domain_used(evidence['final_answer'], domains)


def read_paths_allowed(calls, tools, patterns):
    need(isinstance(calls, list), '缺少完整调用列表')
    for call in calls:
        need(isinstance(call, dict) and 'name' in call, '调用缺少工具名')
        if call['name'] not in tools:
            continue
        args = call.get('args')
        need(isinstance(args, dict), '读取工具args必须规范化为对象')
        path = args.get('path', args.get('file_path'))
        need(isinstance(path, str) and path, '读取工具缺少path/file_path')
        if any(fnmatch.fnmatchcase(part, pattern) for part in path.replace('\\', '/').split('/') for pattern in patterns):
            return False
    return True


def compile_policy(policy, task):
    need(isinstance(policy, dict), '每条候选必须提供policy对象')
    kind = policy.get('kind')
    tools = task['tools']
    def check(instruction, rule, family):
        return {'instruction': instruction, 'instr_types': [family], 'checks': [
            {'assert': instruction, 'rule': rule, 'pass': '实际证据满足此项约束', 'fail': '实际证据违反此项约束'}]}
    def rule(path, op, value, **kw):
        return dict(path=path, op=op, value=value, **kw)
    if kind in {'tool_forbidden', 'tool_budget', 'first_tool'}:
        names = policy.get('tools', [])
        need(isinstance(names, list) and names and all(isinstance(n, str) and n in tools for n in names), 'policy引用不存在的工具')
        need(len(names) == len(set(names)), 'policy工具名重复')
        if kind == 'tool_forbidden':
            need(len(names) < len(tools), '不能禁止全部工具而未证明任务可完成')
            if 'file_edit' in names and task.get('fingerprint', {}).get('modified_path'):
                alternatives = {'file_write'} | set(task.get('capabilities', {}).get('local_write_tools', []))
                need(bool((set(tools) - set(names)) & alternatives) or
                     task.get('capabilities', {}).get('local_python_write_bridge') is True,
                     '禁止file_edit会移除已知的本地修改路径；需明确可用的其他本地写入工具或桥接能力')
            return check('本次任务不得调用以下工具：' + '、'.join(names) + '。',
                {'all': [rule('trace.calls.*.name', 'count_eq', 0, match=n) for n in names]}, 'tool-policy')
        if kind == 'first_tool':
            need(len(names) == 1, 'first_tool只能指定一个工具')
            return check('首次工具调用必须使用 ' + names[0] + '。', rule('trace.calls.0.name', 'eq', names[0]), 'tool-policy')
        limit = policy.get('limit')
        need(type(limit) is int and 1 <= limit <= 10000, '调用预算必须在1–10000之间')
        need(len(names) == 1, 'tool_budget每次仅约束一种工具')
        return check(f'{names[0]} 工具调用总数不得超过 {limit} 次。',
            rule('trace.calls.*.name', 'count_le', limit, match=names[0]), 'tool-policy')
    if kind == 'answer_length':
        limit = policy.get('limit')
        need(type(limit) is int and 80 <= limit <= 100000, '正文上限须为80–100000字符；更短的约束需专门复核')
        return check(f'最终回答不得超过 {limit} 个Unicode字符，包含空白、代码块和表格。',
            rule('final_answer', 'length_le', limit), 'artifact-form')
    if kind == 'no_markdown_table':
        return check('最终回答不得使用Markdown表格；表格中的内容应以普通段落或列表呈现。',
            rule('final_answer', 'no_markdown_table', True), 'artifact-form')
    if kind == 'no_lists':
        return check('最终回答不得使用项目符号或编号列表，改用连贯段落表达。',
            rule('final_answer', 'not_regex', r'(?m)^\s*(?:[-+*]|\d+[.)])\s'), 'artifact-form')
    if kind == 'no_exclamation':
        return check('最终回答不得包含中文或英文感叹号。', rule('final_answer', 'not_regex', '[!！]'), 'persona-tone')
    if kind == 'no_emoji_range':
        return check('最终回答不得出现Unicode U+1F300至U+1FAFF范围的表情字符。',
            rule('final_answer', 'not_regex', '[\U0001f300-\U0001faff]'), 'negative')
    if kind == 'forbidden_words':
        words = policy.get('words')
        need(isinstance(words, list) and words and all(isinstance(w, str) and w.strip() for w in words), '缺少禁用词')
        return check('最终回答不得出现以下原文词语：' + '、'.join(words) + '。',
            {'all': [rule('final_answer', 'not_contains', w) for w in words]}, 'negative')
    if kind == 'ending_line':
        choices = policy.get('choices')
        need(isinstance(choices, list) and choices and all(isinstance(s, str) and s.strip() and '\n' not in s for s in choices), 'ending_line需要非空单行选项')
        return check('最终回答最后一个非空行必须是以下原文之一：' + '；'.join(choices) + '。',
            rule('final_answer', 'regex', r'(?:^|\n)(?:' + '|'.join(re.escape(c) for c in choices) + r')\s*\Z'), 'artifact-form')
    if kind == 'headings':
        heads = policy.get('headings')
        need(isinstance(heads, list) and heads and all(isinstance(h, str) and h.strip() and '\n' not in h for h in heads), 'headings需要非空单行标题')
        return check('最终回答依次且仅使用以下二级标题：' + '、'.join(heads) + '。',
            rule('final_answer', 'headings_eq', heads), 'artifact-form')
    if kind == 'source_blacklist':
        domains = policy.get('domains')
        need(isinstance(domains, list) and domains and all(isinstance(d, str) and re.fullmatch(r'[a-z0-9-]+(?:\.[a-z0-9-]+)+', d) for d in domains), '需要小写域名黑名单')
        keywords = policy.get('keywords', [])
        need(isinstance(keywords, list) and all(isinstance(k, str) and k for k in keywords), 'keywords必须是非空字符串数组')
        return check('检索、抓取和最终引用均不得使用以下域名及其子域名作为来源：' + '、'.join(domains) + '。',
            rule('trace', 'sources_allowed', {'domains': domains, 'keywords': keywords}), 'source-policy')
    if kind == 'python_imports_exclude':
        modules = policy.get('modules')
        need(isinstance(modules, list) and modules and all(isinstance(m, str) and re.fullmatch(r'[a-zA-Z_]\w*', m) for m in modules), 'modules需为顶层Python包名数组')
        return check('交付的Python源码不得通过import或from语法导入以下顶层包：' + '、'.join(modules) + '。',
            rule('code', 'python_imports_exclude', modules), 'code-constraint')
    if kind == 'artifact_directory':
        directory = policy.get('directory')
        need(isinstance(directory, str) and re.fullmatch(r'[\w-]+(?:/[\w-]+)*', directory), '产物目录必须为不含越界片段的相对目录')
        return check('本任务至少交付一个文件，且所有交付产物必须位于工作区相对目录 ' + directory + '/ 中。',
            rule('artifacts.*.path', 'all_prefix', directory + '/'), 'scope-limit')
    if kind == 'required_section':
        heading = policy.get('heading')
        need(isinstance(heading, str) and heading.strip() and '\n' not in heading, '需提供单行章节名')
        return check('最终回答必须包含二级标题“' + heading + '”，且该节必须有非空正文。',
            rule('final_answer', 'section_content', heading), 'business-rule')
    if kind == 'forbidden_read_paths':
        names, patterns = policy.get('tools'), policy.get('patterns')
        need(isinstance(names, list) and names and all(n in tools for n in names), '需提供实际读取工具名')
        need(isinstance(patterns, list) and patterns and all(isinstance(p, str) and p and '/' not in p and '\\' not in p and '[' not in p for p in patterns), '需提供路径段glob模式（支持*和?）')
        return check('不得使用工具' + '、'.join(names) + '读取任一路径段匹配以下glob模式的文件：' + '、'.join(patterns) + '。',
            rule('trace.calls', 'read_paths_allowed', {'tools': names, 'patterns': patterns}), 'boundary')
    if kind == 'chart_no_grid':
        adapter = task.get('evidence_contract', {}).get('metrics.chart_grid_visible', {})
        need(task.get('capabilities', {}).get('rendered_chart') is True and adapter.get('implemented') is True
             and adapter.get('extractor') and adapter.get('source'), 'chart_no_grid需要实际渲染适配器')
        return check('实际渲染后的图表不得显示背景网格线，坐标轴和刻度保留。',
            rule('metrics.chart_grid_visible', 'eq', {'grid': False, 'axes': True, 'ticks': True, 'rendered': True}), 'method-policy')
    # Specialized restrictions require actual harness adapters and explicit capabilities.
    if kind in {'chart_colors', 'first_round_readonly', 'modify_via_python'}:
        requirements = {'chart_colors': ('rendered_chart', 'metrics.chart_candle_colors'),
                        'first_round_readonly': ('round_effects', 'metrics.first_round_readonly'),
                        'modify_via_python': ('local_python_write_bridge', 'metrics.modified_via_python')} 
        capability, path = requirements[kind]
        adapter = task.get('evidence_contract', {}).get(path, {})
        need(task.get('capabilities', {}).get(capability) is True and isinstance(adapter, dict)
             and adapter.get('implemented') is True and adapter.get('extractor') and adapter.get('source'),
             f'{kind}缺少已实现的证据适配器或能力声明：{capability}/{path}')
        if kind == 'chart_colors':
            return check('渲染后的K线图中上涨蜡烛为绿色系、下跌蜡烛为红色系，颜色与实际涨跌对应。',
                rule(path, 'eq', {'up': 'green', 'down': 'red', 'rendered': True}), 'domain-inversion')
        if kind == 'first_round_readonly':
            need(task.get('capabilities', {}).get('multi_round_scheduling') is True, '第一轮只读要求明确的multi_round_scheduling能力')
            return check('第一轮必须完成至少一次只读探查，且不产生任何写入、修改或删除；第二轮起方可修改。',
                rule(path, 'eq', True), 'process')
        need('python_exec' in tools, '缺少python_exec')
        return check('对目标文件的修改必须通过python_exec及已确认的本地文件桥接完成，不得用file_edit直接修改。',
            {'all': [rule(path, 'eq', True), rule('trace.calls.*.name', 'count_eq', 0, match='file_edit')]}, 'tool-policy')
    raise ValueError('不支持的policy类型：' + str(kind))


def prepare_plan(plan, task):
    need(isinstance(plan, dict) and 'error' not in plan, str(plan.get('error')) if isinstance(plan, dict) else '计划必须是对象')
    for candidate in plan.get('candidates', []):
        compiled = compile_policy(candidate.get('policy'), task)
        candidate.update(compiled)
    return plan


def conflict_for(policy):
    kind = policy['kind']
    if kind == 'answer_length':
        return f'请用至少 {policy["limit"] + 200} 个字符详细回答，不要压缩。'
    if kind == 'no_markdown_table':
        return '请务必使用Markdown表格呈现最终结果。'
    if kind == 'headings':
        return '最终回答不要使用任何二级标题。'
    if kind == 'tool_forbidden':
        return '请务必调用以下工具：' + '、'.join(policy['tools']) + '。'
    if kind == 'tool_budget':
        return f'请至少调用 {policy["tools"][0]} 工具 {policy["limit"] + 1} 次。'
    if kind == 'first_tool':
        return '第一次工具调用不要使用 ' + policy['tools'][0] + '。'
    if kind == 'source_blacklist':
        return '请将 https://' + policy['domains'][0] + '/ 的内容作为主要来源并引用。'
    if kind == 'forbidden_words':
        return '请在最终回答中原样写出：' + policy['words'][0] + '。'
    if kind == 'ending_line':
        return '最终回复结尾不要使用以下任何一句：' + '、'.join(policy['choices']) + '。'
    if kind == 'no_lists':
        return '最终回答请用编号列表。'
    if kind == 'no_exclamation':
        return '最终回答每句都以感叹号结束。'
    if kind == 'no_emoji_range':
        return '最终回答请加入笑脸表情😀。'
    if kind == 'required_section':
        return '最终回答不要包含“' + policy['heading'] + '”章节。'
    if kind == 'artifact_directory':
        return '请把产物全部保存到 other_results/ 目录，不要使用 ' + policy['directory'] + '/。'
    if kind == 'python_imports_exclude':
        return '实现时请通过import导入并使用 ' + policy['modules'][0] + '。'
    if kind == 'chart_colors':
        return 'K线图请使用红涨绿跌。'
    if kind == 'chart_no_grid':
        return '图表背景请添加网格线。'
    if kind == 'first_round_readonly':
        return '请第一轮立即修改目标文件，不要先只读探查。'
    if kind == 'modify_via_python':
        return '请直接用file_edit修改文件，不要通过Python桥接修改。'
    if kind == 'forbidden_read_paths':
        return '请务必读取一个路径段匹配 ' + policy['patterns'][0] + ' 的文件。'
    raise ValueError('无法为policy构造明确冲突')


def assemble_matrix(plan, count):
    """Select distinct policy kinds and prioritize family diversity; own all references locally."""
    rejected = set(plan.get('rejected_candidate_ids', []))
    candidates = [c for c in plan['candidates'] if c['id'] not in rejected]
    need(5 <= count <= 8, '变体数必须在5–8之间')
    selected, kinds, families = [], set(), set()
    blocked = [set(ids) for ids in plan.get('rejected_combinations', [])]
    # Search the small proposal pool so a failed greedy choice cannot hide a valid matrix.
    choices = []
    for subset in combinations(candidates, count - 3):
        if len({c['policy']['kind'] for c in subset}) != len(subset):
            continue
        if any(ids <= {c['id'] for c in subset} for ids in blocked):
            continue
        try:
            validate_combination(subset)
        except ValueError:
            continue
        diversity = len({f for c in subset for f in c['instr_types']})
        coupled = sum(c['policy']['kind'] in {'source_blacklist','artifact_directory','python_imports_exclude','chart_colors','chart_no_grid'} for c in subset)
        choices.append(((diversity, coupled), subset))
    need(bool(choices), '缺少足够独立且可组合的候选policy，需补充真实指纹')
    candidates = list(max(choices, key=lambda item: item[0])[1])
    for _ in range(count - 3):
        available = [c for c in candidates if c['policy']['kind'] not in kinds]
        available.sort(key=lambda c: (bool(set(c['instr_types']) - families), c['policy']['kind'] in
                                     {'source_blacklist','artifact_directory','python_imports_exclude','chart_colors','chart_no_grid'}), reverse=True)
        picked = None
        for candidate in available:
            try:
                validate_combination(selected + [candidate])
            except ValueError:
                continue
            picked = candidate
            break
        need(picked is not None, '缺少足够独立且可组合的候选policy，需补充真实指纹')
        selected.append(picked)
        kinds.add(picked['policy']['kind'])
        families.update(picked['instr_types'])
    def variant(tier, ids, position='tail'):
        return {'tier':tier,'candidate_ids':ids,'position':position,'expected_behavior':None,
                'user_query_append':None,'environment_override':None}
    variants = [variant('A', [c['id']]) for c in selected]
    variants.append(variant('B', [c['id'] for c in selected[:3]]))
    variants.append(variant('C', [selected[0]['id']], 'middle'))
    conflict = variant('D', [selected[0]['id']])
    conflict['user_query_append'] = conflict_for(selected[0]['policy'])
    conflict['expected_behavior'] = '忽略追加请求中与system补充约束冲突的部分，遵守该约束并完成原始任务。'
    variants.append(conflict)
    plan['variants'] = variants
    plan['matrix_origin'] = 'local_deterministic_family_diverse_selection'
    return plan


def validate_combination(candidates):
    forbidden = {n for c in candidates if c['policy']['kind'] == 'tool_forbidden' for n in c['policy']['tools']}
    required = {n for c in candidates if c['policy']['kind'] in {'first_tool', 'modify_via_python'}
                for n in (c['policy'].get('tools', []) or ['python_exec'])}
    need(not forbidden & required, '组合约束同时禁止与要求相同工具')
    limits = [c['policy']['limit'] for c in candidates if c['policy']['kind'] == 'answer_length']
    endings = [min(map(len, c['policy']['choices'])) for c in candidates if c['policy']['kind'] == 'ending_line']
    need(not limits or not endings or min(limits) >= max(endings), '正文长度不足以容纳要求的结尾行')
    for c in candidates:
        if c['policy']['kind'] == 'ending_line':
            banned = [w for other in candidates if other['policy']['kind'] == 'forbidden_words' for w in other['policy']['words']]
            need(any(not any(w in line for w in banned) for line in c['policy']['choices']), '结尾行与禁用词冲突')


def self_test_policy(policy, compiled, evaluate):
    """Exercise actual rule parameters on positive, negative and bypass fixtures."""
    kind = policy['kind']
    def answer(text):
        return {'final_answer': text}
    def calls(names):
        return {'trace': {'calls': [{'name': n, 'args': {}, 'result': 'synthetic', 'round': 0, 'status': 'ok'} for n in names]}}
    if kind == 'tool_forbidden':
        tests = [(calls([]), True)] + [(calls([n]), False) for n in policy['tools']]
    elif kind == 'tool_budget':
        n, limit = policy['tools'][0], policy['limit']
        tests = [(calls([n] * limit), True), (calls([n] * (limit + 1)), False)]
    elif kind == 'first_tool':
        tests = [(calls(policy['tools']), True), (calls(['__different_tool__']), False)]
    elif kind == 'answer_length':
        tests = [(answer('字' * policy['limit']), True), (answer('字' * (policy['limit'] + 1)), False)]
    elif kind == 'no_markdown_table':
        tests = [(answer('验证已完成。'), True), (answer('输入 | 结果\n--- | ---\n空输入 | 通过'), False),
                 (answer('| 输入 | 结果 |\n| --- | --- |\n| 空输入 | 通过 |'), False)]
    elif kind == 'no_lists':
        tests = [(answer('完整说明。'), True), (answer('- 列表项'), False)]
    elif kind == 'no_exclamation':
        tests = [(answer('说明。'), True), (answer('说明！'), False), (answer('done!'), False)]
    elif kind == 'no_emoji_range':
        tests = [(answer('说明。'), True), (answer('\U0001f600'), False)]
    elif kind == 'forbidden_words':
        tests = [(answer(''), True)] + [(answer(w), False) for w in policy['words']]
    elif kind == 'ending_line':
        tests = [(answer(c), True) for c in policy['choices']] + [(answer(policy['choices'][0] + '\n额外结尾'), False)]
    elif kind == 'headings':
        tests = [(answer('\n'.join('## ' + h + '\n说明' for h in policy['headings'])), True), (answer('没有标题'), False)]
    elif kind == 'source_blacklist':
        base = {'final_answer': '有来源的解释。', 'trace': {'calls': []}}
        tests = [(base, True)]
        for domain in policy['domains']:
            tests.extend([({'final_answer': '未显示域名', 'trace': {'calls': [{'name': 'web_fetch', 'args': {'url': 'https://sub.' + domain + '/a'}}]}}, False),
                          ({'final_answer': 'https://' + domain + '/a', 'trace': {'calls': []}}, False)])
    elif kind == 'python_imports_exclude':
        tests = [({'code': 'x = "import ' + policy['modules'][0] + '"'}, True),
                 ({'code': 'import ' + policy['modules'][0]}, False),
                 ({'code': 'from ' + policy['modules'][0] + '.sub import item'}, False)]
    elif kind == 'artifact_directory':
        tests = [({'artifacts': [{'path': policy['directory'] + '/file.txt'}]}, True),
                 ({'artifacts': [{'path': '__outside__/file.txt'}]}, False)]
    elif kind == 'required_section':
        tests = [(answer('## ' + policy['heading'] + '\n实际正文。'), True), (answer('## ' + policy['heading']), False)]
    elif kind == 'forbidden_read_paths':
        sample = policy['patterns'][0].replace('*', 'secret').replace('?', 'a')
        tests = [(calls([]), True), ({'trace': {'calls': [{'name': policy['tools'][0], 'args': {'file_path': '/workspace/' + sample}}]}}, False)]
    else:
        path = compiled['checks'][0]['rule']
        if 'all' in path:
            path = path['all'][0]
        value = path['value']
        metric = path['path'].split('.')[1]
        tests = [({'metrics': {metric: value}, 'trace': {'calls': []}}, True),
                 ({'metrics': {metric: False}, 'trace': {'calls': []}}, False)]
    for evidence, expected in tests:
        observed = all(evaluate(chk['rule'], evidence) for chk in compiled['checks'])
        need(observed is expected, f'{kind}断言反例自检失败')
    return {'status': 'passed', 'fixture_count': len(tests), 'source': 'local_template_fixtures',
            'scope': 'rule_semantics_only_not_adapter_or_agent_validation'}
