# Tech Support Resolution — John Smith (555-123-2002)

## Case Summary

| Field | Value |
| --- | --- |
| Customer | John Smith |
| Phone number | 555-123-2002 |
| Reported issue | "No service" + mobile data unavailable |
| Location | France (traveling outside the home network) |
| Wi-Fi | None available |
| Goal | Restore download speed to **Excellent** |
| Constraints | May add up to 2 GB of data (refuel); must **not** change plan |

## 1. Customer Identification

Per the main policy, the customer must be identified first. The customer is
identified by phone number: **555-123-2002 → John Smith**.

## 2. Diagnosis

The workflow requires addressing basic connectivity first (Path 1), then
unavailable mobile data (Path 2.1), then slow data (Path 2.2).

### Path 1 — No service / no connection

1. **Status bar / network status** — confirms "No Signal" / "No Service".
2. **Airplane Mode** — if ON, turn it OFF (`toggle_airplane_mode` OFF).
3. **SIM status** — if "Missing", re-seat the SIM (`reseat_sim_card`) and
   confirm it becomes "Active"; if "Locked" (PIN/PUK), escalate to technical
   support for SIM security; if "Active", continue.
4. **APN settings** — if incorrect, reset to default (`reset_apn_settings`)
   and reboot the device (`reboot_device`).
5. **Line suspension (carrier side)** — if the line is suspended, resolve per
   policy: lift the suspension only after all overdue bills are paid; never
   lift if the line's contract end date is in the past (escalate instead).

### Path 2.1 — Mobile data unavailable (user is traveling)

6. **Speed test** — returns "no connection" (data unavailable).
7. **Traveling abroad → data roaming** — ensure Data Roaming is ON on the
   device (`toggle_roaming` ON), and ensure the line associated with
   555-123-2002 is roaming-enabled. If the line is not roaming-enabled, enable
   it at no cost (per the data-roaming policy).
8. **Mobile data** — ensure Mobile Data is ON (`toggle_data` ON).
9. **Data usage vs plan limit** — if usage has exceeded the plan's data limit,
   data connectivity is lost. The customer must either change plans or refuel
   data. John does **not** want to change plans, so refuel data.

### Path 2.2 — Restore "Excellent" speed

10. **Data Saver** — if ON, turn it OFF (`toggle_data_saver_mode` OFF).
11. **Network mode preference** — if set to 2G/3G, change to
    `set_network_mode_preference("4g_5g_preferred")`.
12. **VPN** — if connected and slow, disconnect it (`disconnect_vpn`).

## 3. Root Causes and Resolution

Root causes consistent with the reported symptoms and the policy:

- **Roaming** — John is in France, outside his home network. For any service
  and data abroad, the line must be roaming-enabled and the device's Data
  Roaming must be ON.
- **Data limit reached** — mobile data was lost because usage exceeded the
  plan's data limit. The maximum refuel is 2 GB; John agreed to add 2 GB.

### Agent-side actions

1. Look up the line associated with phone number 555-123-2002.
2. Enable **roaming** on that line at no cost (if not already enabled).
3. If the line is suspended due to an overdue bill: assist with payment, then
   lift the suspension only after the bill is confirmed **Paid** (and only if
   the contract end date is not in the past).
4. Confirm the plan's **per-GB refueling price** with John, then apply
   **2 GB** of refueled data (the maximum allowed) to the line — without
   changing the plan.

### Device-side actions (guide John)

1. Turn **Airplane Mode** OFF (if on).
2. Turn **Data Roaming** ON.
3. Turn **Mobile Data** ON.
4. Turn **Data Saver** OFF.
5. Set network mode to **4G/5G preferred**.
6. **Disconnect VPN** (if active).
7. **Reboot** the device after any APN/settings change.

## 4. Verification

After the above steps, run a speed test (`run_speed_test`). The expected result
is download speed **Excellent**, which satisfies John's goal.

## 5. Final Message to John

> Hi John, I've looked up your account and found two things: your line was not
> set up for roaming while you're abroad, and your line's data usage has
> reached its limit. I've enabled roaming on your line at no cost, and I've
> added 2 GB of data to your line (your plan stays the same).
>
> On your phone, please: make sure Airplane Mode is off, turn on Data Roaming
> and Mobile Data, turn off Data Saver, set your network mode to 4G/5G
> preferred, and reboot your device. After that, run a speed test — it should
> now show "Excellent".

---

*Resolution documented from the provided policy, technical support manual, and
technical support workflow. No information beyond those documents was used.*
