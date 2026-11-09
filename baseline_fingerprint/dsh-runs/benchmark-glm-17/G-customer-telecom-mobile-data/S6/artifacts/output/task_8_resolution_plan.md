# Task 8 技术支持处理方案 — John Smith / 555-123-2002

依据文档：
- `attached_files/task_8/main_policy.md`（代理政策，含客户识别、逾期账单、线路暂停、流量充值、换套餐、数据漫游）
- `attached_files/task_8/tech_support_manual.md`（故障排查手册，设备侧诊断/修复动作）
- `attached_files/task_8/tech_support_workflow.md`（结构化排查工作流 Path 1 / 2.1 / 2.2 / 3）

## 0. 场景与目标

| 项 | 内容 |
| --- | --- |
| 客户自述 | John Smith，号码 555-123-2002 |
| 位置 | 法国（归属网络之外，属漫游） |
| 症状 | 手机显示"无服务"；移动数据不可用；无 Wi-Fi |
| 目标 | 恢复连接，且 `run_speed_test` 达到 **excellent** |
| 客户约束 | 可以补充 2GB 流量（refuel）；**不更换套餐** |

## 1. 第一步：识别客户（必须先做）

main_policy.md「Technical Support」：*You must first identify the customer.*

可用的查询方式（「Customer Lookup」）：
1. 电话号码
2. 客户 ID
3. 姓名 + 出生日期（按姓名查询时 DOB 必填）

本例客户已提供电话号码 **555-123-2002**，按电话号码查询客户档案即可完成识别，无需额外索取出生日期。

查询后需从档案确认：
- 账户状态（Active / Suspended / Pending Verification / Closed）
- 该号码对应的 line ID、line 状态（Active / Suspended / Pending Activation / Closed）
- 是否存在 **Overdue** 账单（关系到线路暂停与恢复）
- line 的 data usage（GB）与 plan 的 data limit（GB），用于判断是否超出限额
- line 的 roaming status（关系到境外数据）
- plan 的 data refueling price per GB（用于计算 2GB 充值价格）

后续所有账户侧操作（开启漫游、充值流量）都必须作用于 **555-123-2002 对应的那条 line**。

## 2. 问题分类

按 workflow「Initial Problem Classification」：
- 主诉一：**无服务**（Path 1）
- 主诉二：**移动数据不可用**（Path 2.1）
- 规则：*"For multiple issues, address basic connectivity first."* → 先恢复服务，再恢复数据，最后把速度优化到 excellent（Path 2.2）。
- 客户无 Wi-Fi：Path 2 明确 *"does not cover wifi data issues"*，不涉及 Wi-Fi 排查；全部依赖蜂窝数据。

## 3. Path 1：无服务排查（按序执行，每步后让用户查看状态栏确认）

**Step 1.0 — 确认是否为无服务问题**
- 请用户执行 `check_status_bar`。
- 状态栏显示 "📵 No Signal" 或 "✈️ Airplane Mode" → 确认无服务问题，进入 Step 1.1。
- 若已有信号强度图标（📶¹~📶⁴）→ 并非无服务问题，直接进入 Path 2.1。

**Step 1.1 — 飞行模式与网络状态**
- 请用户执行 `check_network_status`。
- 飞行模式 ON → 请用户 `toggle_airplane_mode` 关闭 → 再看状态栏确认服务是否恢复。
- 飞行模式 OFF → 进入 Step 1.2。

**Step 1.2 — SIM 卡状态**
- 请用户执行 `check_sim_status`。
- **Missing** → 请用户 `reseat_sim_card` 重新插拔 → 确认 SIM 变为 **Active** → 看状态栏确认。
- **Locked（PIN/PUK）** → 手册规定 **escalate to technical support for assistance with SIM security**（转人工前先尽力完成其他可解步骤）。
- **Active** → 进入 Step 1.3。

**Step 1.3 — APN 设置**
- 请用户执行 `check_apn_settings`。
- APN 显示 Incorrect → 请用户 `reset_apn_settings` → **必须** `reboot_device`（重置后需重启才生效）→ 看状态栏确认。

**Step 1.4 — 线路是否被暂停**
- 账户侧查询 555-123-2002 对应 line 的状态与暂停原因。
- **暂停原因 = 逾期账单**：
  1. 按「Overdue Bill Payment」流程处理：确认账单状态为 **Overdue** → 核对金额 → 发送 payment request（账单状态变为 AWAITING PAYMENT；同一时间只能有一张 AWAITING PAYMENT 账单；发送前必须自查账单确实 Overdue）→ 请用户用 `check_payment_request` 查看并接受 → 客服执行 `make_payment` → **确认账单状态已更新为 PAID** 后再告知用户已支付。
  2. 所有逾期账单付清后，恢复线路（lift suspension）。
  3. 恢复后**必须让用户重启设备**（`reboot_device`）才能重新获得服务。
- **暂停原因 = 合同到期日已过**：即使付清账单也**不允许**恢复 → 转人工。
- 恢复/确认后请用户看状态栏确认服务恢复。

## 4. Path 2.1：移动数据不可用

**Step 2.1.0 — 确认数据不可用**
- 请用户执行 `run_speed_test`。返回 'no connection' → 确认移动数据不可用，按 Path 2.1 继续；解决后若速度不是 excellent，再走 Path 2.2。

**Step 2.1.1 — 先确认服务**
- Path 1 完成并确认有服务后，请用户重新 `run_speed_test`；仍无连接 → Step 2.1.2。

**Step 2.1.2 — 是否在境外（本例：是，法国）**
- 请用户执行 `check_network_status`，查看 **Data Roaming**：
  - **OFF** → 请用户 `toggle_roaming` 打开 → 重新 `run_speed_test`。
  - **ON 但仍不工作** → 账户侧检查该 line 的 **roaming status**：
    - 未启用 → 依据政策「Data Roaming」：**免费为用户开启**（enable roaming at no cost）→ 重新 `run_speed_test`。
    - 已启用 → 进入 Step 2.1.3。
  - 仍无连接 → Step 2.1.3。

**Step 2.1.3 — 移动数据开关**
- `check_network_status` 中 Mobile Data：
  - **OFF** → 请用户 `toggle_data` 打开 → 重新 `run_speed_test`；仍无连接 → Step 2.1.4。
  - **ON** → Step 2.1.4。

**Step 2.1.4 — 数据用量是否超限**
- 账户侧比对：line 的 data usage 是否超过 plan 的 data limit。超出则数据连接被切断。
- **若已超限**，政策给出两个选项：
  1. 换更大流量的套餐；
  2. 按 plan 的 data refueling price per GB 充值流量（refuel）。
  - 客户明确**不换套餐** → 走 refuel：
    - 询问需要补充多少（客户已表示 **2GB**；政策上限 2GB，2GB 在允许范围内）。
    - 按套餐单价计算总价，**先向客户确认价格**，确认后再执行。
    - 将充值的 2GB 应用到 **555-123-2002 对应的 line**。
    - 请用户重新 `run_speed_test` 验证连接恢复。
- **若未超限** → 请用户 `run_speed_test`；仍无连接 → 转人工（transfer_to_human_agents）。

## 5. Path 2.2：速度未达 excellent（连接恢复后）

若 `run_speed_test` 返回 poor / fair / good（任何低于 excellent 的速度都算慢）：

**Step 2.2.1 — 数据限制设置**
- 请用户执行 `check_data_restriction_status`。
- Data Saver ON → 请用户 `toggle_data_saver_mode` 关闭 → 重新测速；未到 excellent → 下一步。

**Step 2.2.2 — 网络模式偏好**
- 请用户执行 `check_network_mode_preference`。
- 若为 2G/3G → 请用户 `set_network_mode_preference(mode="4g_5g_preferred")` → 重新测速；未到 excellent → 下一步。

**Step 2.2.3 — VPN**
- 请用户执行 `check_vpn_status`。
- VPN 处于连接状态（尤其 performance 为 Poor）→ 请用户 `disconnect_vpn` → 重新测速。
- 无 VPN 或断开后仍不达 excellent → 转人工。

## 6. 完成标准（全部满足才算解决）

1. `check_status_bar` 显示信号强度图标（非 No Signal、非飞行模式），移动数据为 Data Enabled。
2. `run_speed_test` 返回 **excellent**。
3. 客户确认手机恢复可用。

## 7. 约束与红线（来自 main_policy.md）

- 不提供政策与工具之外的信息、知识或流程，不给主观建议或评论。
- 一次只做一个工具调用；工具调用与对用户的回复不能同时进行。
- **流量充值**：上限 2GB；先询问数量、**确认价格**、再应用到用户提供的号码对应的 line。
- **不更换套餐**：客户已明确拒绝换套餐，只在其主动同意时才走「Change Plan」流程。
- **漫游**：客户在境外（法国），若 line 未启用漫游，**免费开启**。
- **线路暂停**：仅在所有逾期账单付清后可恢复；合同到期日已过的不可恢复。
- **暂停恢复 / APN 重置后必须重启设备**。
- **转人工**：仅在无法在自身权限内解决时（SIM PIN/PUK 锁定、合同到期导致的暂停、全部步骤后仍无连接或速度不达 excellent）。转人工 = 先调用 `transfer_to_human_agents`，再发送 "YOU ARE BEING TRANSFERRED TO A HUMAN AGENT. PLEASE HOLD ON."
- 转人工前必须穷尽所有可行解法。

## 8. 本会话环境限制

本会话未接入任何电信域工具（客户查询、line/plan 查询、漫游开启、流量充值、`transfer_to_human_agents` 等），E2B 沙箱中也仅镜像了三份政策文档。因此：
- 账户侧动作无法实际执行，本文件给出的是可直接照做的完整操作序列。
- 设备侧动作（`check_*` / `toggle_*` / `set_*` / `reboot_device`）由客户在其手机上执行，客服按本方案逐步引导。
- 对应的分步引导话术见 `output/task_8_agent_script.md`。
