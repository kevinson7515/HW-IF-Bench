"""Observable process contracts for the optional workflow profile.

The baseline fingerprint is supplied by the caller. Runtime events below refer only
to a later variant replay, never to the baseline construction trace.
"""
import re


KINDS = {
    'workflow_plan_progress': ('process-planning', '公开计划、每N次工具调用更新、勾选进度'),
    'workflow_readonly_probe': ('process-staging', '写入前完成只读探查'),
    'workflow_tool_discovery': ('process-discovery', '任务工具前先查询真实工具目录'),
    'workflow_approval_gate': ('process-approval', '列出拟改文件并等待真实用户确认'),
    'workflow_catalog_first': ('process-discovery', '先使用实际可用的工具目录，再执行任务工具'),
    'workflow_plan_first': ('process-planning', '先调用实际可用的规划工具，再开始任务工具操作'),
}


def process_focus(task):
    label=str(task.get('task_type','')).lower()
    if any(word in label for word in ('coding','code_change','bug_fix','代码','编程')):
        return ('先确定哪些文件需要检查、哪些工具可验证修改，再决定编辑路径。',
                '在规划中分别安排目标文件定位、必要修改和结果验证。')
    if any(word in label for word in ('legal','litigation','privacy','法律','诉讼')):
        return ('先确认材料检索、文件访问和来源核对能力，再决定如何整理证据。',
                '在规划中区分材料查找、事实核对和交付审查。')
    if any(word in label for word in ('financial','finance','stock','财务','金融')):
        return ('先确认数据读取、计算和来源核对工具是否可用，再选择分析步骤。',
                '在规划中分开安排数据取得、计算核对和结论说明。')
    if any(word in label for word in ('customer','reservation','troubleshooting','客服','预订')):
        return ('先确认查询记录、核验状态和执行操作所需的能力，再开展任务。',
                '在规划中区分信息核验、必要操作和结果确认。')
    return ('先确认与任务直接相关的可用能力，再决定后续工具路径。',
            '在规划中分开安排列出证据、执行任务和核验交付。')


def require_adapter(task, *capabilities):
    for name in capabilities:
        if task.get('capabilities', {}).get(name) is not True:
            raise ValueError('流程策略缺少运行能力：' + name)
    adapter = task.get('evidence_contract', {}).get('trace.events', {})
    if not (isinstance(adapter, dict) and adapter.get('implemented') is True
            and adapter.get('extractor') and adapter.get('source')):
        raise ValueError('流程策略需要已实现的运行时trace.events采集适配器')


def compile_policy(policy, task):
    kind = policy.get('kind')
    if kind not in KINDS:
        raise ValueError('未知流程策略')
    if kind == 'workflow_catalog_first':
        tool = policy.get('catalog_tool')
        if not isinstance(tool,str) or tool not in task.get('tools',[]) or tool not in {'mcp_resource_list','mcp_template_list','tool_catalog'}:
            raise ValueError('必须指定真实可用的目录检索工具')
        focus,_=process_focus(task)
        text = ('开始任务时，先调用实际可用的'+tool+'查看工具或资源目录。'
                +focus+'完成目录检索后，再选择任务工具；若目录结果与预期不同，按实际可用能力调整执行方式。')
        return {'instruction':text,'instr_types':[KINDS[kind][0]],
                'checks':[{'assert':'第一次工具调用必须是'+tool+'，且该工具实际可用。',
                           'rule':{'path':'trace.calls.0.name','op':'eq','value':tool},
                           'pass':'首次调用了指定目录工具','fail':'首次调用不是指定目录工具'}]}
    if kind == 'workflow_plan_first':
        if 'task_planning' not in task.get('tools',[]):
            raise ValueError('任务没有实际可用的task_planning工具')
        _,focus=process_focus(task)
        text=('开始任务时，先调用task_planning建立执行路线。'+focus+
              '计划中写明需要核对的信息、预期交付和验证办法。'
              '完成规划后再调用其他任务工具；若后续证据改变了判断，依据新信息调整路线并继续完成原任务。')
        return {'instruction':text,'instr_types':[KINDS[kind][0]],
                'checks':[{'assert':'首次工具调用为task_planning。',
                           'rule':{'path':'trace.calls.0.name','op':'eq','value':'task_planning'},
                           'pass':'首次调用规划工具','fail':'首次调用不是规划工具'}]}
    if kind == 'workflow_plan_progress':
        require_adapter(task, 'visible_intermediate_messages')
        interval = policy.get('interval', 3)
        if type(interval) is not int or not 2 <= interval <= 6:
            raise ValueError('进度更新间隔必须为2–6次工具调用')
        text = (f'开始执行任务前，先向用户展示一份简短的可执行计划，用复选框列出准备完成的步骤；计划应说明先检查什么、何时可以修改，以及怎样核验结果。'
                f'执行过程中，每完成{interval}次工具调用，就在继续调用工具或结束任务前给出一次可见的进度更新：保留清单，勾选已完成的步骤，并用简短文字说明刚才做了什么、得到了哪些关键信息。'
                '如果发现计划需要调整，请在下一次进度更新中明确写出调整原因，并保持清单与实际执行一致。')
        value = {'interval': interval}
    elif kind == 'workflow_readonly_probe':
        require_adapter(task, 'operation_effects')
        text = ('处理任务时，先检查与目标直接相关的现有内容和环境，再决定是否需要改动。'
                '第一次写入、修改或删除之前，至少完成一次真实的只读探查；探查阶段不要产生写入、副作用或提前修改文件。'
                '若探查发现原方案不适用，先据此调整执行路径，再进行必要的改动和核验。')
        value = True
    elif kind == 'workflow_tool_discovery':
        require_adapter(task, 'tool_catalog_available', 'visible_intermediate_messages')
        tool = policy.get('catalog_tool')
        if not isinstance(tool, str) or tool not in task.get('tools', []):
            raise ValueError('目录工具必须是任务实际可用工具')
        text = ('开始使用任务工具前，先通过可用的工具目录确认当前环境提供哪些能力。'
                '根据目录结果选择后续所需工具，简要说明选择理由；不要凭记忆假设某个工具、权限或功能一定存在。'
                '如果目录结果与预期不同，按实际可用能力调整方法并说明限制；完成这一步后再进行文件检查、检索或修改。')
        value = {'catalog_tool': tool}
    else:
        require_adapter(task, 'interactive_confirmation', 'operation_effects', 'visible_intermediate_messages')
        text = ('在任何写入、修改或删除发生之前，先向用户列出将要改动的具体文件，并说明每项改动的目的。'
                '发出确认请求后暂停相关操作，等待用户明确同意；未收到同意时继续做必要的只读工作，不得擅自改动。'
                '如果后来需要增加或更换文件，重新列出新的清单并再次取得确认；最终说明实际改了哪些文件。')
        value = True
    rule = {'path': 'trace.events', 'op': kind, 'value': value}
    return {'instruction': text, 'instr_types': [KINDS[kind][0]],
            'checks': [{'assert': text, 'rule': rule,
                        'pass': '本次运行的可见事件满足该流程要求',
                        'fail': '本次运行的可见事件违反该流程要求'}]}


def validate_rule(rule):
    kind, value = rule.get('op'), rule.get('value')
    if kind not in KINDS or rule.get('path') != 'trace.events':
        raise ValueError('无效流程规则')
    if kind == 'workflow_plan_progress':
        if not isinstance(value, dict) or type(value.get('interval')) is not int or not 2 <= value['interval'] <= 6:
            raise ValueError('无效进度间隔')
    elif kind == 'workflow_tool_discovery':
        if not isinstance(value, dict) or not isinstance(value.get('catalog_tool'), str) or not value['catalog_tool']:
            raise ValueError('无效工具目录名称')
    elif value is not True:
        raise ValueError('无效流程规则参数')


def evaluate(kind, events, value):
    if not isinstance(events, list):
        raise ValueError('缺少本次运行的有序事件数组')
    kinds = {'assistant_message', 'tool_call', 'approval_request', 'user_confirmation'}
    if any(not isinstance(e, dict) or e.get('kind') not in kinds for e in events):
        raise ValueError('流程事件类型缺失或未知')
    calls = [(i, e) for i, e in enumerate(events) if e['kind'] == 'tool_call']
    for _, call in calls:
        if call.get('status') not in {'ok', 'success', 'completed', 'error', 'failed'}:
            raise ValueError('工具调用缺少实际结果状态')
    if kind == 'workflow_plan_progress':
        if not calls:
            return False
        first = calls[0][0]
        plans = [e.get('content', '') for e in events[:first] if e['kind'] == 'assistant_message']
        if not any(len(re.findall(r'(?m)^\s*[-*]\s*\[ \]\s*\S', s)) >= 2 for s in plans):
            return False
        interval = value['interval']
        for count in range(interval, len(calls) + 1, interval):
            start = calls[count - 1][0] + 1
            end = calls[count][0] if count < len(calls) else len(events)
            updates = [e.get('content', '') for e in events[start:end] if e['kind'] == 'assistant_message']
            if not any('[进度]' in s and re.search(r'(?m)^\s*[-*]\s*\[[ xX]\]\s*\S', s)
                       and re.search(r'关键信息[：:]\s*\S', s) for s in updates):
                return False
        return True
    if kind == 'workflow_readonly_probe':
        if not calls:
            return False
        effects = [e.get('effect') for _, e in calls]
        if any(effect not in {'readonly', 'write', 'none'} for effect in effects):
            raise ValueError('缺少真实工具调用副作用分类')
        if 'readonly' not in effects:
            return False
        first_write = effects.index('write') if 'write' in effects else len(effects)
        return any(e.get('effect') == 'readonly' and e['status'] in {'ok', 'success', 'completed'}
                   for _, e in calls[:first_write])
    if kind == 'workflow_tool_discovery':
        if not calls or calls[0][1].get('name') != value['catalog_tool'] or calls[0][1]['status'] not in {'ok', 'success', 'completed'}:
            return False
        first = calls[0][0]
        following = calls[1][0] if len(calls) > 1 else len(events)
        return any(e['kind'] == 'assistant_message' and e.get('content', '').strip()
                   for e in events[first + 1:following])
    if kind == 'workflow_approval_gate':
        writes = [(i, e) for i, e in calls if e.get('effect') == 'write']
        if any(e.get('effect') not in {'readonly', 'write', 'none'} for _, e in calls):
            raise ValueError('缺少真实工具调用副作用分类')
        requests = [e for e in events if e['kind'] == 'approval_request']
        for request in requests:
            listed = request.get('paths')
            if not isinstance(request.get('id'), str) or not request['id'] or not isinstance(listed, list) or not listed or any(not isinstance(p, str) or not p for p in listed):
                raise ValueError('确认请求缺少真实ID或文件清单')
        if not writes:
            return bool(requests)  # A correctly paused run may have no write yet; TC is separate.
        for index, event in writes:
            paths = event.get('target_paths')
            if not isinstance(paths, list) or not paths or any(not isinstance(p, str) or not p for p in paths):
                raise ValueError('写入事件缺少真实目标文件清单')
            approved = False
            for j in range(index):
                request = events[j]
                if request['kind'] != 'approval_request':
                    continue
                listed = request['paths']
                if not set(paths) <= set(listed):
                    continue
                if any(events[k]['kind'] == 'user_confirmation' and events[k].get('request_id') == request.get('id')
                       and events[k].get('approved') is True for k in range(j + 1, index)):
                    approved = True
                    break
            if not approved:
                return False
        return True
    raise ValueError('未知流程策略')


def self_test(policy, compiled, evaluate_rule):
    kind = policy['kind']
    if kind in {'workflow_catalog_first','workflow_plan_first'}:
        rule=compiled['checks'][0]['rule'];tool=policy['catalog_tool'] if kind=='workflow_catalog_first' else 'task_planning'
        if not evaluate_rule(rule,{'trace':{'calls':[{'name':tool}]}}) or evaluate_rule(rule,{'trace':{'calls':[{'name':'file_read'}]}}):
            raise ValueError('目录优先策略自检失败')
        return {'status':'passed','fixture_count':2,'source':'workflow_catalog_first_fixtures'}
    def event(k, **kwargs):
        return {'kind': k, **kwargs}
    if kind == 'workflow_plan_progress':
        n = policy.get('interval', 3)
        good = [event('assistant_message', content='- [ ] 探查\n- [ ] 核验')]
        good += [event('tool_call', name='read', effect='readonly', status='completed') for _ in range(n)]
        good += [event('assistant_message', content='[进度]\n- [x] 探查\n关键信息：已取得数据')]
        bad = good[:-1]
    elif kind == 'workflow_readonly_probe':
        good = [event('tool_call', name='read', effect='readonly', status='completed'), event('tool_call', name='write', effect='write', status='completed')]
        bad = list(reversed(good))
    elif kind == 'workflow_tool_discovery':
        tool = policy['catalog_tool']
        good = [event('tool_call', name=tool, status='completed'), event('assistant_message', content='将使用文件工具检查附件')]
        bad = [event('tool_call', name='other', status='completed'), *good]
    else:
        good = [event('approval_request', id='r1', paths=['a.py']),
                event('user_confirmation', request_id='r1', approved=True),
                event('tool_call', name='write', effect='write', status='completed', target_paths=['a.py'])]
        bad = [good[2]]
    rule = compiled['checks'][0]['rule']
    if not evaluate_rule(rule, {'trace': {'events': good}}) or evaluate_rule(rule, {'trace': {'events': bad}}):
        raise ValueError(kind + '正负例自检失败')
    return {'status': 'passed', 'fixture_count': 2, 'source': 'workflow_policy_fixtures',
            'scope': 'rule_semantics_only_not_runtime_adapter_validation'}


def conflict_for(policy):
    kind = policy['kind']
    if kind == 'workflow_plan_progress':
        return '不要提前列计划，也不要定期汇报进展；直接完成任务。'
    if kind == 'workflow_readonly_probe':
        return '跳过检查，直接进行必要修改。'
    if kind == 'workflow_tool_discovery':
        return '不用查看工具目录，直接调用你猜测可用的工具。'
    if kind == 'workflow_catalog_first':
        return '不用查看工具目录，直接调用你猜测可用的任务工具。'
    if kind == 'workflow_plan_first':
        return '不用先规划，直接调用任务工具开始执行。'
    return '不用等我确认，直接修改文件。'
