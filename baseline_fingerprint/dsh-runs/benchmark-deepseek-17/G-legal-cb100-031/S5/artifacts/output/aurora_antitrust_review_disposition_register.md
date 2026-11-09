# Aurora Pricing MDL Discovery Audit — Review Disposition Register

Matter: `CB-LD-2701` · Matter date: **2026-09-05** · Client: Aurora Home Supply Co. · Counterparty: *In re Residential Fixture Pricing*

System of record: one row per portfolio key. Each key is tested on four controls — **immutable identity**, **operative authority**, **current operations**, and **effective approval/revision**. A supported action requires all four; otherwise the key is an evidence hold and the missing control is stated.

Selected approach: **`aurora-antitrust:scoped-evidence`** (AUTHORIZED). Outcome: 6 supported actions, 6 evidence holds.

| Portfolio key | Concern | Entity | Source rev | Score | Identity | Authority | Operations | Approval / revision | Disposition | Owner (roster) |
|---|---|---|---|---|---|---|---|---|---|---|
| CBP-031-01 | Bates-Range Overlap | ENT-031-1000 | REV-2025.1 | 37 | agree | 215 records (R753) | covers 180 (E138) — mismatch | **pending / inactive, capacity 0** | **HOLD** | Samuel Kim (pending) |
| CBP-031-02 | Email-Family Separation | ENT-031-1001 | REV-2025.2 | 89 | agree | threshold 11% (R682) | result 14% (E716) | active, capacity 1 | SUPPORTED | Talia Brooks |
| CBP-031-03 | Request-Response Mismatch | ENT-031-1002 | REV-2025.3 | 91 | **collision (1002 / 2002)** | **blocks (R694)** | **open / unresolved (E452)** | active, capacity 4 | **HOLD** | Adrian Mensah |
| CBP-031-04 | Metadata Field Loss | ENT-031-1003 | REV-2025.4 | 45 | agree | due by 2025-11-27 (R665) | completed 2025-11-25 (E980) | active, capacity 4 | SUPPORTED | Farah Ibrahim |
| CBP-031-05 | Collection-Date Inconsistency (mobile chats) | ENT-031-1004 | REV-2025.5 | 70 | agree | **blocks (R821)** | **open / unresolved (E407)** | **pending / inactive, capacity 0** | **HOLD** | Dominic Alvarez (pending) |
| CBP-031-06 | Protective-Order Designation Error | ENT-031-1005 | REV-2025.6 | 82 | agree | 148 records (R246) | covers 125 (E214) — undercount | active, capacity 6 | SUPPORTED | Leona Park |
| CBP-031-07 | Production Gap | ENT-031-1006 | REV-2025.7 | 58 | agree | 78 records (R626) | covers 40 (E660) — undercount | active, capacity 6 | SUPPORTED | Henry Cho |
| CBP-031-08 | Legal-Hold Delivery Gap | ENT-031-1007 | REV-2025.1 | 57 | agree | must use notices@ (R397) | receipt used archive@ (E382) — wrong address | active, capacity 1 | SUPPORTED | Maya Ellison |
| CBP-031-09 | Clawback Deadline | ENT-031-1008 | REV-2025.2 | 61 | agree | due by 2025-03-31 (R664) | completed 2025-05-12 (E503) — late | active, capacity 1 | SUPPORTED | Jonas Feld |
| CBP-031-10 | Third-Party Subpoena Deadline | ENT-031-1009 | **REV-2024.2** | 33 | crosswalk cites REV-2025.3 | must use notices@ (R537) | receipt used archive@ (E178) | active, capacity 4 — **superseded revision** | **HOLD** | Willa Novak |
| CBP-031-11 | Custodian Omission (departed custodians) | ENT-031-1010 | REV-2025.4 | 55 | **collision (1010 / 2010)** | 98 records (R976) | covers 61 (E151) — mismatch | active, capacity 3 | **HOLD** | Owen Delgado |
| CBP-031-12 | Common-Interest Support Gap (privilege) | ENT-031-1011 | REV-2025.5 | 85 | agree | **blocks (R908)** | **open / unresolved (E253)** | active, capacity 1 | **HOLD** | Priya Raman |

## Evidence holds — missing control and cure condition

| Key | Missing control(s) | What must be cured before that record can be certified |
|---|---|---|
| CBP-031-01 | Effective approval/revision | Activate/confirm the owner (Samuel Kim is pending, inactive, capacity 0) and reconcile the overlapping Bates count (cert covers **180** vs authority population **215**, R753). |
| CBP-031-03 | Immutable identity; operative authority; current operations | Approved crosswalk revision resolving the ENT-031-1002 / ENT-031-2002 collision; close the request-response mismatch that "blocks completion" (R694) and the "open / unresolved" state (E452). |
| CBP-031-05 | Operative authority; current operations; effective approval/revision | Reconcile the mobile-chat collection-date inconsistency (open, E407; blocks, R821); activate owner (Dominic Alvarez is pending, inactive, capacity 0). |
| CBP-031-10 | Effective approval/revision (superseded revision) | Re-key CBP-031-10 to the later effective revision **REV-2025.3** (operations currently cite REV-2024.2), and confirm the correct notice address. |
| CBP-031-11 | Immutable identity | Approved crosswalk revision resolving the ENT-031-1010 / ENT-031-2010 collision; reconcile custodian-omission count (covers **61** vs population **98**, R976). |
| CBP-031-12 | Operative authority; current operations | Resolve the pending privilege challenge — the common-interest support gap that "blocks completion" (R908) and is "open / unresolved" (E253). |

## Supported actions — residual gaps to disclose (not block)

These six pass all four controls and may be certified now. Where a numeric or delivery discrepancy remains, disclose it in the certification rather than asserting a clean log-total.

| Key | Disclose in certification |
|---|---|
| CBP-031-02 | Email-family separation result **14%** exceeds the **11%** threshold (R682) — a family gap. |
| CBP-031-04 | Completed 2025-11-25, before the 2025-11-27 deadline — no residual gap. |
| CBP-031-06 | Certification covers **125** of the **148**-record designation-error population (R246). |
| CBP-031-07 | Certification covers **40** of the **78**-record production-gap population (R626). |
| CBP-031-08 | Legal-hold receipt used `archive-in_re_…@example.test` instead of the required `notices-aurora_…@example.test` (R397). |
| CBP-031-09 | Clawback deadline event completed **2025-05-12**, after the **2025-03-31** deadline (R664). |

## Provenance

Synthetic CounselBench-100 source record. All people, entities, events, amounts, and addresses are fictitious; the record is not legal advice.
