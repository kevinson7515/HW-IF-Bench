# Aurora MDL Discovery Audit — Review Disposition Register

Matter: CB-LD-2701 — Aurora pricing MDL discovery audit
Matter date: 2026-09-05
Approach: `aurora-antitrust:scoped-evidence` (AUTHORIZED)
System of record: one row per portfolio key in `cb100-031-aurora-antitrust`.

Four controls per key — a supported action requires ALL four; any failure preserves an evidence hold:
1. Identity (identity_crosswalk) — single resolved entity, fields agree.
2. Authority (operative_authority) — operative requirement stated, not "blocks completion".
3. Current state (current_operations) — current state stated, not "open and unresolved".
4. Approval/revision (approval_and_capacity) — active owner with capacity; revision consistent.

| Portfolio key | Subject | Entity | Owner (roster) | Identity | Authority | Current | Approval/rev | Disposition |
|---|---|---|---|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | ENT-031-1000 | Samuel Kim (pending, capacity 0) | PASS | PASS (215 / R753) | PASS (180 / E138) | FAIL — pending/0 | **HOLD** |
| CBP-031-02 | Email-family separation | ENT-031-1001 | Talia Brooks (active) | PASS | PASS (11% / R682) | PASS (14% / E716) | PASS | **SUPPORTED** — disclose 14% > 11% threshold |
| CBP-031-03 | Request-response mismatch | ENT-031-1002 | Adrian Mensah (active) | FAIL — collision (ENT-031-1002 vs ENT-031-2002) | FAIL — blocks (R694) | FAIL — open (E452) | PASS | **HOLD** |
| CBP-031-04 | Metadata field loss | ENT-031-1003 | Farah Ibrahim (active) | PASS | PASS (due 2025-11-27 / R665) | PASS (completed 2025-11-25 / E980) | PASS | **SUPPORTED** |
| CBP-031-05 | Collection-date inconsistency | ENT-031-1004 | Dominic Alvarez (pending, capacity 0) | PASS | FAIL — blocks (R821) | FAIL — open (E407) | FAIL — pending/0 | **HOLD** |
| CBP-031-06 | Protective-order designation error | ENT-031-1005 | Leona Park (active) | PASS | PASS (148 / R246) | PASS (125 / E214) | PASS | **SUPPORTED** — disclose 125 vs 148 designation gap |
| CBP-031-07 | Production gap | ENT-031-1006 | Henry Cho (active) | PASS | PASS (78 / R626) | PASS (40 / E660) | PASS | **SUPPORTED** — disclose 40 vs 78 gap |
| CBP-031-08 | Legal-hold delivery gap | ENT-031-1007 | Maya Ellison (active) | PASS | PASS (notices@ / R397) | PASS (archive@ / E382) | PASS | **SUPPORTED** — disclose delivery-address mismatch |
| CBP-031-09 | Clawback deadline | ENT-031-1008 | Jonas Feld (active) | PASS | PASS (due 2025-03-31 / R664) | PASS (completed 2025-05-12 / E503) | PASS | **SUPPORTED** — disclose late clawback completion |
| CBP-031-10 | Third-party subpoena deadline | ENT-031-1009 | Willa Novak (active) | PASS | PASS (notices@ / R537) | PASS (archive@ / E178) | FAIL — revision inconsistent (REV-2025.3 crosswalk vs REV-2024.2 source) | **HOLD** |
| CBP-031-11 | Custodian omission | ENT-031-1010 | Owen Delgado (active) | FAIL — collision (ENT-031-1010 vs ENT-031-2010) | PASS (98 / R976) | PASS (61 / E151) | PASS | **HOLD** |
| CBP-031-12 | Common-interest support gap | ENT-031-1011 | Priya Raman (active) | PASS | FAIL — blocks (R908) | FAIL — open (E253) | PASS | **HOLD** |

## Summary

- Supported actions (certify now, with disclosure): CBP-031-02, 04, 06, 07, 08, 09 — **6**
- Evidence holds (cure before certification): CBP-031-01, 03, 05, 10, 11, 12 — **6**

Source anchors: impact population `097_aurora_antitrust_impact_population.xlsx`; identity crosswalk CB-DOC-031-001…012; operative authority CB-DOC-031-013…024; current operations CB-DOC-031-025…036; approval/capacity CB-DOC-031-037…048; correspondence CB-DOC-031-049…060.
