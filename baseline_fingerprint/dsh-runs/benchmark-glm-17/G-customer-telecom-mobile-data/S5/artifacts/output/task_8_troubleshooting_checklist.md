# 任务 8 · 排障操作清单（随会话进度勾选）

客户：John Smith / 555-123-2002 · 人在法国（漫游）· 无 Wi-Fi · 目标 run_speed_test = excellent · 只补流量 ≤2GB，不换套餐

## A. 恢复服务（Path 1）

- [ ] A1 客户 `check_status_bar` → 记录图标
- [ ] A2 飞行模式 ON → `toggle_airplane_mode` 关闭 → 复查状态栏
- [ ] A3 `check_sim_status`：Missing → `reseat_sim_card` → 确认 Active；Locked → **转人工**；Active → A4
- [ ] A4 `reset_apn_settings` → `reboot_device` → 复查状态栏
- [ ] A5 账户侧查线路是否暂停：
  - 欠费暂停 → 付清全部 Overdue 账单（确认 PAID）→ 恢复线路 → 客户 `reboot_device`
  - 合同到期暂停 → **转人工**（不允许恢复）
- [ ] 服务恢复确认（状态栏有信号）

## B. 恢复移动数据（Path 2.1）

- [ ] B1 `run_speed_test`（应为 'no connection'）
- [ ] B2 设备 Data Roaming OFF → `toggle_roaming` 打开 → 复测
- [ ] B3 线路未启用 roaming → **免费启用** → 复测
- [ ] B4 Mobile Data OFF → `toggle_data` 打开 → 复测
- [ ] B5 账户侧：data usage 是否超过套餐 data limit → 超限：
  - [ ] 确认补 2GB（客户已选定，不改套餐）
  - [ ] 按套餐 refuel 单价报价并获客户确认
  - [ ] 应用到 555-123-2002 对应线路 → 复测
- [ ] 数据连接恢复确认

## C. 提速到 excellent（Path 2.2）

- [ ] C1 `check_data_restriction_status`：Data Saver ON → `toggle_data_saver_mode` 关闭 → 复测
- [ ] C2 `check_network_mode_preference`：2G/3G → `set_network_mode_preference("4g_5g_preferred")` → 复测
- [ ] C3 `check_vpn_status`：VPN 激活/性能 Poor → `disconnect_vpn` → 复测
- [ ] `run_speed_test` = **excellent** ✅

## 转人工触发条件

- SIM Locked（PIN/PUK）
- 合同到期导致的线路暂停
- A/B/C 全部走完仍未恢复或未达 excellent

转交流程：先调用 `transfer_to_human_agents` → 再发送 `'YOU ARE BEING TRANSFERRED TO A HUMAN AGENT. PLEASE HOLD ON.'`
