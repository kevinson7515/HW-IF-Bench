# Aurora MDL Production — Review Note & Working Position

- Matter: CB-LD-2701 (Aurora pricing MDL discovery audit) · Client: Aurora Home Supply Co.
- Matter date / team position deadline: 2026-09-05
- System of record: `output/aurora_mdl_review_disposition_register.csv` (one row per portfolio key)

## Selected approach

`aurora-antitrust:scoped-evidence` (Authority: AUTHORIZED). Certify only where all four controls pass; preserve an evidence hold and name the missing control everywhere else. Do not treat a similar name, a superseded revision, or a pending owner as proof.

Four-control test per key: (1) immutable identity, (2) operative authority, (3) current operations, (4) effective approval/revision.

## Bottom line

- **Do now (certify):** 6 supported keys — CBP-031-02, 04, 06, 07, 08, 09.
- **Wait (hold):** 6 keys — CBP-031-01, 03, 05, 10, 11, 12.
- **Aurora cannot certify the whole MDL production today.** It can certify the 6 supported keys; full certification requires curing the 6 holds before 2026-09-05.
- **Evidence that changes the answer:** for each hold, the missing control (below). An approved active owner, a resolving identity crosswalk, an unblocked operative authority, or a non-superseded revision flips that key to supported.

## Supported actions (certify now)

| Key | Subject | Basis |
|---|---|---|
| CBP-031-02 | Email-family separation | identity agree; threshold operative; result stated; owner active (cap 1) |
| CBP-031-04 | Metadata field loss | identity agree; due 2025-11-27 vs completed 2025-11-25; owner active (cap 4) |
| CBP-031-06 | Protective-order designation error | identity agree; population stated; certification stated; owner active (cap 6) |
| CBP-031-07 | Production gap | identity agree; population stated; certification stated; owner active (cap 6) |
| CBP-031-08 | Legal-hold delivery gap | identity agree; notice rule stated; receipt stated; owner active (cap 1) |
| CBP-031-09 | Clawback deadline | identity agree; deadline stated; completion stated; owner active (cap 1) |

Latest supported control date: 2026-09-03 (CBP-031-02). Residual authority-vs-operations deltas (e.g., 148 vs 125, 78 vs 40, receipt archive vs notices, 2025-05-12 vs due 2025-03-31) are disclosed in the register, not certification blockers under the four-control test.

## Evidence holds (do not certify until cured)

| Key | Subject | Missing control | Gap | Owner |
|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | approval_and_capacity | pending approval, inactive, capacity 0 (Samuel Kim); Bates 215 (R753) vs 180 (E138) | Samuel Kim |
| CBP-031-03 | Request-response mismatch | identity + authority + operations | identity collision ENT-031-1002/2002; "open … blocks completion"; "open and unresolved" | Adrian Mensah (roster) / Henry Cho (crosswalk) |
| CBP-031-05 | Collection-date inconsistency | authority + operations + approval | "open … blocks completion" (R821); "open and unresolved"; pending owner, capacity 0 | Dominic Alvarez (roster) / Jonas Feld (collection) |
| CBP-031-10 | Third-party subpoena deadline | operative_authority | cites REV-2024.2; REV-2025.3 later effective (superseded revision); receipt archive vs notices | Willa Novak |
| CBP-031-11 | Custodian omission | identity | identity collision ENT-031-1010/2010 (departed custodian) | Owen Delgado (roster) |
| CBP-031-12 | Common-interest support gap | authority + operations | "open … blocks completion" (R908); "open and unresolved" | Priya Raman |

## Source anchors

- Protocol / approach: `12_case_management/089_case_management_source_export.md` ("Matter work-product protocol").
- Impact population: `12_case_management/097_aurora_antitrust_impact_population.xlsx`.
- Per-key control records (identity / authority / operations / approval): key K → CB-DOC-031-{K, K+12, K+24, K+36} (e.g., CBP-031-05 → 005, 017, 029, 041).

## Alternatives considered

- `aurora-antitrust:shortcut` — certify from log totals without custodians/overlaps. Rejected: UNSUPPORTED_BY_CURRENT_EVIDENCE.
- `aurora-antitrust:blanket-hold` — freeze all 12. Rejected: defers the 6 already-supported keys; ADDITIONAL_APPROVAL_REQUIRED.

## Limits

Synthetic CounselBench-100 records; not legal advice. No external facts assumed. The disposition turns only on the four documented controls; correspondence records uniformly flag reconciliation but do not themselves change a control's pass/fail.

## Close the loop (Slack reply)

Channel `C00000031`, thread `1760000031.000005` (reply, not a new post):

> Position (matter 2026-09-05): Aurora can certify 6 keys now (CBP-031-02, 04, 06, 07, 08, 09) under scoped-evidence. 6 keys are on hold pending cure — 01 (pending owner, Bates 215/180), 03 (identity collision), 05 (open collection-date + pending owner), 10 (superseded revision REV-2024.2), 11 (identity collision, departed custodian), 12 (open common-interest gap). Owners recorded in the register; latest supported action lands 2026-09-03. Full MDL certification waits on those six cures. Register + note committed to output/.
