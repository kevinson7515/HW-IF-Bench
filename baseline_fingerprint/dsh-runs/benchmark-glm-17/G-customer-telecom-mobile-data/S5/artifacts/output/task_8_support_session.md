# 任务 8 · 技术支持会话处理记录（John Smith / 555-123-2002）

## 1. 会话信息

- 处理时间：2025-02-25 12:08:00 EST（依据 main_policy 时钟）
- 客户自述：John Smith，号码 555-123-2002
- 渠道：技术支持（Technical Support）
- 问题描述：
  - 人在法国（归属网络以外，属漫游场景）
  - 手机显示"无服务"（No Service）
  - 移动数据不可用
  - 无 Wi-Fi 可用
- 客户目标：恢复连接，且测速（run_speed_test）达到 **excellent**
- 客户约束：
  - 可接受补充流量（data refueling），最多 **2GB**
  - **不更换套餐**（不做 plan change）

## 2. 身份识别

- 依据 main_policy「Customer Lookup」：可凭 **电话号码** / 客户 ID / 姓名+出生日期 查询客户；按姓名查询时才必须提供出生日期。
- 客户已提供姓名与电话号码，按号码 **555-123-2002** 查询即可完成识别；后续所有账户侧核验（线路状态、漫游、用量、套餐、账单）均应对该号码对应的线路执行。
- main_policy「Technical Support」要求先识别客户再开展支持；本会话以该号码为准。

## 3. 问题分类与处理顺序

依据 tech_support_workflow「Initial Problem Classification」：多个问题并存时**先处理基础连接**。

1. 无服务（Path 1）——蜂窝服务是移动数据的前提
2. 移动数据不可用（Path 2.1）——含漫游（人在法国）与流量额度
3. 测速未达 excellent（Path 2.2）——提速优化

## 4. 本轮已发送给客户的消息

> 您好 John，感谢您提供姓名和号码 555-123-2002，我这边已记录，后续都以这个号码对应的线路来处理。
>
> 先跟您对齐一下情况：
> - 您人在法国（归属网络以外的漫游地区）
> - 手机显示"无服务"，移动数据不可用，也没有 Wi-Fi
> - 目标：恢复连接，并让测速达到 excellent
> - 如需补流量：最多 2GB，不更换套餐
>
> 由于移动数据必须先有蜂窝服务，我们按顺序来：先恢复服务 → 再恢复数据（您在法国，会重点检查漫游和流量额度）→ 最后把速度优化到 excellent。
>
> 第一步：请您查看手机的状态栏（check_status_bar），告诉我看到的图标，特别是：
> 1. 是否显示 ✈️ 飞行模式
> 2. 信号：📵 无信号，还是 📶 几格（Poor / Fair / Good / Excellent）
> 3. 网络类型（5G / 4G 等）
> 4. 📱 Data Enabled 还是 📵 Data Disabled
> 5. 是否有 🔽 Data Saver、🔒 VPN 图标
> 6. 电量百分比
>
> 您把看到的内容发给我，我们一步步排查。

## 5. 后续处理流程（决策树）

### 阶段 A：恢复蜂窝服务（Path 1）

| 步骤 | 请客户执行 | 判定与分支 |
|---|---|---|
| 1.0 | `check_status_bar` | 显示无信号/飞行模式 → 1.1；已有信号 → 转阶段 B |
| 1.1 | `check_network_status` | 飞行模式 ON → `toggle_airplane_mode` 关闭 → 复查状态栏；OFF → 1.2 |
| 1.2 | `check_sim_status` | Missing → `reseat_sim_card` → 确认 Active → 复查状态栏；Locked（PIN/PUK）→ **转人工**（SIM 安全）；Active → 1.3 |
| 1.3 | `reset_apn_settings` → `reboot_device` | 复查状态栏（APN 重置后必须重启才生效）；仍未恢复 → 1.4 |
| 1.4 | 账户侧核验线路是否暂停 | 见下方「线路暂停处理」 |

**线路暂停处理**（main_policy「Line Suspension」）：

- 暂停原因：有逾期账单 / 线路合同到期日已过。
- 若因逾期账单暂停：付清全部逾期账单后可以恢复线路。付款流程（Overdue Bill Payment）：
  1. 确认账单状态为 Overdue（发送付款请求前必须确认，工具不校验）
  2. 确认账单应付金额
  3. 发送付款请求（账单状态 → AWAITING PAYMENT；同一时间只能有一张账单处于该状态）
  4. 请客户用 check_payment_request 查看付款请求
  5. 客户接受后 make_payment
  6. **确认账单状态变为 PAID 后**再告知客户已付清
- 若合同到期日已过：**不允许恢复**，即使付清欠费 → 转人工。
- 恢复线路后，客户必须 `reboot_device` 才会重新有服务。
- 1.4 之后仍未恢复 → 转人工。

### 阶段 B：恢复移动数据（Path 2.1）

前提：服务已恢复。先请客户 `run_speed_test`；返回 'no connection' 即数据不可用，继续下列步骤。

| 步骤 | 操作 | 判定与分支 |
|---|---|---|
| 2.1.2 漫游（客户在法国） | 客户 `check_network_status` 查看设备侧 Data Roaming | OFF → `toggle_roaming` 打开 → 复测；ON 但仍无连接 → 账户侧核验**线路是否 roaming enabled**：未启用 → 按政策**免费启用**（no cost）→ 复测；已启用仍无连接 → 2.1.3 |
| 2.1.3 移动数据开关 | 客户 `check_network_status` 查看 Mobile Data | OFF → `toggle_data` 打开 → 复测，仍无连接 → 2.1.4；ON 但不工作 → 2.1.4 |
| 2.1.4 流量用量 | 账户侧比对线路 data usage 与套餐 data limit | 超限 → 按客户既定选择走 **2GB 补充流量**（见下）；未超限 → 复测，仍无连接 → 转人工 |

**2GB 补充流量**（main_policy「Data Refueling」）：

- 上限：单次最多 **2GB**；客户已明确补 2GB，且**不做 plan change**。
- 流程：确认数量（2GB）→ 按该线路套餐的 **data refueling price per GB** 计算并**向客户确认总价** → 应用到号码 555-123-2002 对应的线路 → 复测。
- 报价必须来自工具查询到的该线路套餐实际单价；未查询到单价前不得报价。
- 完成后复测：仍无连接 → 转人工；有连接但速度非 excellent → 阶段 C。

### 阶段 C：提速到 excellent（Path 2.2）

| 步骤 | 请客户执行 | 判定与分支 |
|---|---|---|
| 2.2.1 | `check_data_restriction_status` | Data Saver ON → `toggle_data_saver_mode` 关闭 → 复测；OFF 或关闭后仍未达 excellent → 2.2.2 |
| 2.2.2 | `check_network_mode_preference` | 2G/3G → `set_network_mode_preference("4g_5g_preferred")` → 复测；已是最优 → 2.2.3 |
| 2.2.3 | `check_vpn_status` | VPN 激活（manual：连接且性能为 Poor）→ `disconnect_vpn` → 复测；无 VPN 或断开后仍未达 excellent → **转人工** |

## 6. 客户约束的落实

- **不更换套餐**：全程不主动推荐、不执行 plan change；流量超限时仅按客户既定选择走 refuel。若 refuel 不可行（超过 2GB 上限或客户拒绝），按 workflow 转人工。
- **2GB 上限**：data refueling 最大 2GB。
- **漫游免费**：客户在归属网络以外旅行，线路未启用 roaming 时应**免费启用**，不产生费用。
- **无 Wi-Fi**：所有恢复手段依赖蜂窝网络；本案例不涉及 MMS 排障路径（含 Wi-Fi Calling 干扰项）。

## 7. 升级（转人工）条件

- SIM 卡 Locked（PIN/PUK 安全问题）
- 线路因合同到期日已过而暂停（不允许恢复）
- 阶段 A / B / C 全部步骤走完，仍未恢复服务 / 数据，或测速未达 excellent
- 转交流程：**先调用 transfer_to_human_agents，再发送固定话术** `'YOU ARE BEING TRANSFERRED TO A HUMAN AGENT. PLEASE HOLD ON.'`
- 转人工前必须已尝试所有可行的解决步骤（manual 与 workflow 均有此要求）。

## 8. 运行规则（main_policy）

- 一次只进行一个工具调用；工具调用与给客户的消息不同时进行。
- 不提供政策与工具之外的信息，不作主观推荐或评论。
- 拒绝违反政策的请求。

## 9. 当前状态与待办

- 已发出第一轮消息：请客户查看状态栏（`check_status_bar`）并回报图标。
- 等待客户回报：飞行模式 / 信号强度 / 网络类型 / 数据开关 / Data Saver / VPN / 电量。
- 账户侧待核验（需工具支持）：客户资料；号码 555-123-2002 对应线路的状态（是否 Suspended）、roaming 状态、data usage；所属套餐的 data limit 与 data refueling price per GB；是否有 Overdue 账单；合同到期日。
