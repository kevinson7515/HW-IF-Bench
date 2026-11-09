# Aurora MDL Production — Review Note & Working Position

- **Matter:** CB-LD-2701 — Aurora pricing MDL discovery audit
- **Client:** Aurora Home Supply Co.
- **Counterparty:** In re Residential Fixture Pricing
- **Matter date:** 2026-09-05 (no external facts assumed)
- **System of record:** Review Disposition Register (one row per portfolio key)

## Selected approach

**`aurora-antitrust:scoped-evidence` — AUTHORIZED.**

Aurora **cannot fully certify** the MDL production today. Under scoped-evidence it can
**commit 6 supported actions** and **preserve 6 evidence holds**, finishing the latest
supported action by **2026-09-03** (two days before the matter date). Incremental cost
$20,000.

## Why not full certification

The four-control test (immutable identity, operative authority, current operations,
effective approval/revision) is satisfied for only 6 of 12 portfolio keys. A missing
control becomes an **evidence hold**, not a certification. Similar names, superseded
revisions, and pending owners are not proof.

## Supported actions (6)

| Key | Issue | Owner | Next control |
|---|---|---|---|
| CBP-031-02 | Email-family separation | Talia Brooks | 2026-09-03 |
| CBP-031-04 | Metadata field loss | Farah Ibrahim | 2026-09-01 |
| CBP-031-06 | Protective-order designation error | Leona Park | 2026-08-30 |
| CBP-031-07 | Production gap | Henry Cho | 2026-08-29 |
| CBP-031-08 | Legal-hold delivery gap | Maya Ellison | 2026-08-28 |
| CBP-031-09 | Clawback deadline | Jonas Feld | 2026-08-27 |

Each supported action carries a **disclosed** gap recorded in the register (population
or date/email mismatches between the operative-authority and current-operations records).
These are disclosed, not cured; certification is limited to the supported population.

## Evidence holds (6)

| Key | Issue | Missing control / gap | Owner | Revisit |
|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | Effective approval (pending/inactive, capacity 0); 180 vs 215 records | Samuel Kim | 2026-09-04 |
| CBP-031-03 | Request-response mismatch | Identity collision ENT-031-1002 vs ENT-031-2002; open mismatch blocks completion | Adrian Mensah | 2026-09-02 |
| CBP-031-05 | Collection-date inconsistency | Effective approval (pending/inactive, capacity 0); open inconsistency blocks completion | Dominic Alvarez | 2026-08-31 |
| CBP-031-10 | Third-party subpoena deadline | Superseded revision (current_ops cites REV-2024.2; REV-2025.3 later effective); email mismatch | Willa Novak | 2026-09-04 |
| CBP-031-11 | Custodian omission | Identity collision ENT-031-1010 vs ENT-031-2010; 98 vs 61 records | Owen Delgado | 2026-09-03 |
| CBP-031-12 | Common-interest support gap | Open gap blocks completion (R908 / E253) | Priya Raman | 2026-09-02 |

## Gaps to cure before full certification

1. Resolve the two identity collisions (CBP-031-03, CBP-031-11) with an approved crosswalk revision.
2. Activate/approve the two pending, zero-capacity approvals (CBP-031-01, CBP-031-05).
3. Re-baseline CBP-031-10 current operations to REV-2025.3 and reconcile the subpoena-notice address.
4. Close the open common-interest gap (CBP-031-12).
5. Reconcile the disclosed population/date/email mismatches on the six supported keys.

## Alternatives considered

- **`aurora-antitrust:shortcut`** — certify from production-log totals without checking custodians or overlaps. **UNSUPPORTED_BY_CURRENT_EVIDENCE.**
- **`aurora-antitrust:blanket-hold`** — freeze the entire matter population. **ADDITIONAL_APPROVAL_REQUIRED.**

## Limits

- One register row per portfolio key; the four-control test is applied exactly.
- Impact-control scores in the population workbook are inputs, not dispositions.
- This note does not decide legal effect or select among candidate responses.
