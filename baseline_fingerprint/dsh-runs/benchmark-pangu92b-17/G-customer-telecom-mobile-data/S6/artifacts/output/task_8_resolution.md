# Technical Support Case Resolution — Task 8

## Customer
- Name: John Smith
- Phone: 555-123-2002
- Location: France (outside home network / roaming)

## Reported Issue
- Phone shows "No Service" (no cellular signal).
- Mobile data unavailable.
- No Wi-Fi available.
- Goal: restore speed test to "excellent".
- Constraints: willing to add 2GB of data; will NOT change plan.

## Diagnosis
1. Primary: The user is abroad (France). "No Service" while roaming typically means the line is not roaming-enabled, so the device cannot register on a foreign network.
2. Secondary: Mobile data is unavailable — the line's monthly data allowance has likely been exhausted.

## Resolution (per main policy + tech support workflow)
1. **Enable roaming on the line (carrier side) — at no cost.**
   Per policy: "If a user is traveling outside their home network, you should check if the line is roaming enabled. If it is not, you should enable it at no cost for the user."
2. **Guide the user to enable Data Roaming on the device** (toggle_roaming).
3. **Refuel 2GB of data** (user agreed; maximum refuel is 2GB).
   Per policy: refuel at the plan's per-GB price; do NOT change the plan (user declined).
4. **Verify** with a speed test — expect "excellent".

Fallback (Path 2.2 — slow data) if speed is still not "excellent" after the above:
- Turn Data Saver OFF.
- Set network mode preference to "4g_5g_preferred".
- Disconnect any active VPN.

## Outcome
- Roaming enabled on the line (no charge).
- 2GB data refueled (plan unchanged).
- Device Data Roaming enabled by the user.
- Speed test restored to "excellent".

## Notes
- No plan change was performed (user declined).
- No transfer to a human agent was required — the issue was resolved within the agent's scope.
