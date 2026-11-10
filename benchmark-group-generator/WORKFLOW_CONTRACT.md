# v5.4 流程指令与运行事件接口

这份初版只用**外部提供的基线 fingerprint**选择反默认约束。生成器不会读取基线运行包。以下 `trace.events` 专指将来执行**某个变体**时采集的可见事件，与基线 fingerprint 分开。

## 可生成的流程策略

| 策略 | Agent 实际收到的要求 | 程序核验的核心条件 |
|---|---|---|
| `workflow_plan_progress` | 先展示复选框计划；默认每完成 3 次工具调用，更新清单和关键信息 | 首次工具调用前有计划；每第 3 次调用之后、下一次调用或结束前有可见进度消息 |
| `workflow_readonly_probe` | 先检查目标及环境；第一次写操作前必须真正完成只读探查 | 有成功的只读调用，且其发生于任何写调用之前 |
| `workflow_tool_discovery` | 先查真实工具目录，再选择任务工具并说明依据 | 首次调用是声明的目录工具，且成功返回；下一次工具调用前有可见说明 |
| `workflow_approval_gate` | 修改前列具体文件，等待用户明确确认；新增文件需重新确认 | 每次写调用之前有涵盖目标路径的确认请求及真实用户同意；尚无写操作时，已请求并等待可通过流程项 |
| `workflow_catalog_first` | 先调用任务确实提供的目录检索工具，再开始其他工具操作 | `trace.calls` 中首个工具名为目录工具；此项只检验首次调用，不检验目录结果或后续说明 |

前四项依赖下面的事件适配器；`workflow_catalog_first` 仅依赖本次运行的 `trace.calls` 和基线首次工具调用的 fingerprint。`--profile workflow` 中 A 档用于单项诊断，B/C/D 档把 4–6 项兼容策略写成编号列表；不同策略的程序断言分别评分。指令中的“先”“后”是 Agent 要采取的行动；`trace.events` 只存在于评测端。

## 输入任务需声明的能力

只有执行平台实际支持时，才能在提供的任务输入中声明如下能力：

```json
{
  "capabilities": {
    "visible_intermediate_messages": true,
    "operation_effects": true,
    "tool_catalog_available": true,
    "interactive_confirmation": true
  },
  "evidence_contract": {
    "trace.events": {
      "implemented": true,
      "extractor": "实际采集器的名称",
      "source": "实际运行事件来源"
    }
  }
}
```

规划和工具发现需要可见中间消息；只读与审批需要能区分工具调用的真实副作用；工具发现还需要 `tools` 中确有目录工具；审批需要运行平台能暂停、接收真实用户回复并继续。缺任一能力时不应声明 `true`。模型不能凭空填写能力或适配器。

外部 fingerprint 应提供与流程有关的观测，例如是否在首次工具调用前规划、是否在写入前只读探查、是否先查工具目录、是否在写入前等待确认。字段名可由提供方确定，模型提出的 `basis.field` 必须准确引用所提供的字段；仅有回复长度或工具总次数，不能证明这些流程现象。生成器会核对引用字段和值，但不能仅凭文件证明来源真实性。

## 变体运行证据的最小形状

`trace.events` 是按实际发生顺序排列的数组。合成结构示意：

```json
{
  "trace": {
    "events": [
      {"kind": "assistant_message", "content": "- [ ] 检查现状\n- [ ] 修改并核验"},
      {"kind": "tool_call", "name": "tool_catalog", "status": "completed", "effect": "none"},
      {"kind": "assistant_message", "content": "目录显示可使用 file_read，先检查目标文件。"},
      {"kind": "tool_call", "name": "file_read", "status": "completed", "effect": "readonly"},
      {"kind": "approval_request", "id": "request-1", "paths": ["parser.py"]},
      {"kind": "user_confirmation", "request_id": "request-1", "approved": true},
      {"kind": "tool_call", "name": "file_edit", "status": "completed", "effect": "write", "target_paths": ["parser.py"]},
      {"kind": "assistant_message", "content": "[进度]\n- [x] 检查现状\n关键信息：已确认解析分支。"}
    ]
  }
}
```

运行平台必须从真实事件中生成 `approval_request` 和 `user_confirmation`，不能从 Agent 自述或最终回答推断用户已经同意。`effect` 应根据实际操作分类，特别是执行代码、脚本或 shell 时不能只看工具名称。缺少事件、状态或副作用分类时，该检查会不可评分；普通违规返回失败。

“每三步”在本初版中明确为每三次**工具调用**，包括返回错误的调用。更新须发生在第 3、6、9 次调用之后，且在下一次调用或结束之前。程序检查可见消息中的计划、清单和关键信息标记；清单是否如实反映完成状态、关键信息是否真实，仍需结合轨迹人工或语义审查。

若 Agent 发出修改文件清单并正确等待，而本轮没有获得用户回复、没有写操作，审批流程项可通过；原任务完成度 TC 仍单独判断，不能因此记为 FULL。审批策略在这个初版中不放入 D 档冲突注入，避免将未完成的交互当成已完成任务。

## 验证边界

`examples/workflow_demo_*` 中所有任务、fingerprint、能力与事件均为**合成数据**。离线测试验证结构、组合和程序规则，不能证明真实运行平台已经采集上述事件，也不能证明 Agent 会遵从。正式使用前应让实际执行平台产出一份样例证据，核对每种事件的来源和顺序，再对少量变体回放与人工复核。
