# Review Disposition Register — Matter CB-LD-2701 (Aurora pricing MDL discovery audit)

System of record for the twelve portfolio keys in `cb100-031-aurora-antitrust`. One row per portfolio key.
Selected approach: `aurora-antitrust:scoped-evidence` (AUTHORIZED). Matter date: 2026-09-05.
Four-control test per record 089: immutable identity (I), operative authority (A), current operations (C), effective approval/revision (P). A supported action requires all four; otherwise an evidence hold is preserved with the missing control stated.

## Register

| Portfolio key | Production issue | I | A | C | P | Disposition | Missing control (holds only) | Required cure before certification | Owner of record | Next internal control date |
|---|---|---|---|---|---|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | OK | OK | OK | FAIL | **Evidence hold** | Effective approval — owner pending approval and inactive, capacity 0 | Approve/activate or reassign owner; reconcile 35-record Bates overlap delta (population 215 vs certification 180) | Samuel Kim (pending approval, inactive) | 2026-09-04 |
| CBP-031-02 | Email-family separation | OK | OK | OK | OK | **Supported action** (certify with disclosure) | — | Production-control row disclosing 3-point threshold breach (result 14% vs threshold 11%); cure by re-separation if the court treats the threshold as a hard limit | Talia Brooks (active, cap 1) | 2026-09-03 |
| CBP-031-03 | Request-response mismatch | FAIL | OK | OK | OK | **Evidence hold** | Immutable identity — ENT-031-1002 vs ENT-031-2002 collision, no approved crosswalk | Approved crosswalk revision resolving the entity collision; resolve the open request-response mismatch (R694/E452) | Adrian Mensah (active, cap 4) | 2026-09-02 |
| CBP-031-04 | Metadata field loss | OK | OK | OK | OK | **Supported action** (certify) | — | None — event completed 2025-11-25, before the 2025-11-27 due date | Farah Ibrahim (active, cap 4) | 2026-09-01 |
| CBP-031-05 | Collection-date inconsistency | OK | OK | OK | FAIL | **Evidence hold** | Effective approval — owner pending approval and inactive, capacity 0 | Approve/activate or reassign owner; resolve the open collection-date inconsistency (R821/E407) | Dominic Alvarez (pending approval, inactive) | 2026-08-31 |
| CBP-031-06 | Protective-order designation error | OK | OK | OK | OK | **Supported action** (certify with disclosure) | — | Production-control row for the 23-record designation-error delta (population 148 vs certification 125) | Leona Park (active, cap 6) | 2026-08-30 |
| CBP-031-07 | Production gap | OK | OK | OK | OK | **Supported action** (certify with disclosure) | — | Production-control row for the 38-record production gap (population 78 vs certification 40) | Henry Cho (active, cap 6) | 2026-08-29 |
| CBP-031-08 | Legal-hold delivery gap | OK | OK | OK | OK | **Supported action** (certify with disclosure) | — | Reissue hold notice to `notices-aurora_home_supply_co@example.test` (receipt used the archive address); production-control row documenting the delivery gap | Maya Ellison (active, cap 1) | 2026-08-28 |
| CBP-031-09 | Clawback deadline | OK | OK | OK | OK | **Supported action** (certify with disclosure) | — | Disclose late completion: event completed 2025-05-12 against a 2025-03-31 deadline | Jonas Feld (active, cap 1) | 2026-08-27 |
| CBP-031-10 | Third-party subpoena deadline | OK | OK | OK | FAIL | **Evidence hold** | Effective revision — all eight records cite superseded REV-2024.2; REV-2025.3 is controlling | Reissue notices under controlling REV-2025.3 to `notices-aurora_home_supply_co@example.test` (E178 receipt used the archive address); re-extract the key under REV-2025.3 | Willa Novak (active, cap 4) | 2026-09-04 |
| CBP-031-11 | Custodian omission | FAIL | OK | OK | OK | **Evidence hold** | Immutable identity — ENT-031-1010 vs ENT-031-2010 collision, no approved crosswalk | Approved crosswalk revision resolving the entity collision; reconcile the 37-record custodian-omission delta (population 98 vs certification 61) | Owen Delgado (active, cap 3) | 2026-09-03 |
| CBP-031-12 | Common-interest support gap (privilege challenge) | OK | OK | OK | FAIL | **Evidence hold** | Operative authority blocks completion — R908: the open gap blocks completion; E253 open/unresolved | Resolve the common-interest support gap (privilege challenge); disclosure alone is insufficient because the operative order blocks completion | Priya Raman (active, cap 1) | 2026-09-02 |

## Counts

- Supported actions: 6 — CBP-031-02, 04, 06, 07, 08, 09
- Evidence holds: 6 — CBP-031-01, 03, 05, 10, 11, 12
- Latest supported action finishes 2026-09-03 (CBP-031-02 control date), within the scoped-evidence deadline of 2026-09-03 and ahead of the 2026-09-05 matter date.

## Per-key evidence anchors

Each key's four controls come from its identity_crosswalk, operative_authority, current_operations, and approval_and_capacity records; correspondence, financial_or_population_support, chronology_and_custody, and independent_counterrecord records corroborate.

- **CBP-031-01** — 001 (identity, ENT-031-1000, REV-2025.1), 013 (authority, R753 population 215), 025 (current, E138 certification 180), 037 (approval, Samuel Kim pending/inactive cap 0); 049, 061, 073, 085; xlsx row 1 (score 37).
- **CBP-031-02** — 002 (identity, ENT-031-1001), 014 (authority, R682 threshold 11%), 026 (current, E716 result 14%), 038 (approval, Talia Brooks active cap 1, control 2026-09-03); 050, 062, 074, 086; xlsx row 2 (score 89).
- **CBP-031-03** — 003 (identity collision 1002/2002, no approved crosswalk), 015 (authority, R694 open mismatch blocks completion), 027 (current, E452 open/unresolved), 039 (approval, Adrian Mensah active cap 4); 051, 063, 075, 087; xlsx row 3 (score 91).
- **CBP-031-04** — 004 (identity, ENT-031-1003), 016 (authority, R665 due 2025-11-27), 028 (current, E980 completed 2025-11-25), 040 (approval, Farah Ibrahim active cap 4); 052, 064, 076, 088; xlsx row 4 (score 45).
- **CBP-031-05** — 005 (identity, ENT-031-1004), 017 (authority, R821 open inconsistency blocks completion), 029 (current, E407 open/unresolved), 041 (approval, Dominic Alvarez pending/inactive cap 0); 053, 065, 077, 089; xlsx row 5 (score 70).
- **CBP-031-06** — 006 (identity, ENT-031-1005), 018 (authority, R246 population 148), 030 (current, E214 certification 125), 042 (approval, Leona Park active cap 6); 054, 066, 078, 090; xlsx row 6 (score 82).
- **CBP-031-07** — 007 (identity, ENT-031-1006), 019 (authority, R626 population 78), 031 (current, E660 certification 40), 043 (approval, Henry Cho active cap 6); 055, 067, 079, 091; xlsx row 7 (score 58).
- **CBP-031-08** — 008 (identity, ENT-031-1007), 020 (authority, R397 notices must use `notices-aurora_home_supply_co@example.test`), 032 (current, E382 receipt used `archive-in_re_residential_fixture_pricing@example.test`), 044 (approval, Maya Ellison active cap 1); 056, 068, 080, 092; xlsx row 8 (score 57).
- **CBP-031-09** — 009 (identity, ENT-031-1008), 021 (authority, R664 due 2025-03-31), 033 (current, E503 completed 2025-05-12), 045 (approval, Jonas Feld active cap 1); 057, 069, 081, 093; xlsx row 9 (score 61).
- **CBP-031-10** — 010 (identity, ENT-031-1009; ref REV-2024.2 vs current REV-2025.3), 022 (authority, R537; cites REV-2024.2 but REV-2025.3 is the later effective revision), 034 (current, E178 wrong-address receipt, REV-2024.2), 046 (approval, Willa Novak active cap 4; REV-2024.2 vs REV-2025.3); 058, 070, 082, 094 — all eight records of this key cite the superseded revision; xlsx row 10 (score 33, source_revision REV-2024.2).
- **CBP-031-11** — 011 (identity collision 1010/2010, no approved crosswalk), 023 (authority, R976 population 98), 035 (current, E151 certification 61), 047 (approval, Owen Delgado active cap 3); 059, 071, 083, 095; xlsx row 11 (score 55).
- **CBP-031-12** — 012 (identity, ENT-031-1011), 024 (authority, R908 open common-interest support gap blocks completion), 036 (current, E253 open/unresolved), 048 (approval, Priya Raman active cap 1); 060, 072, 084, 096; xlsx row 12 (score 85).

Decision protocol: `12_case_management/089_case_management_source_export.md` (Matter work-product protocol).
Impact population: `12_case_management/097_aurora_antitrust_impact_population.xlsx` — all twelve rows "retained source population; not a legal disposition"; impact-control scores are inputs, not dispositions.

Provenance: synthetic CounselBench-100 source records. All people, entities, events, amounts, and addresses are fictitious; this register is not legal advice.
