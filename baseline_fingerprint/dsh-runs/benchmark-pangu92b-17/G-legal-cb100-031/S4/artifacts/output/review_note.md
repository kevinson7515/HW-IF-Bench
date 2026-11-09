# Review Note — Aurora Pricing MDL certification position (CB-LD-2701)

**Selected approach:** `aurora-antitrust:scoped-evidence` (AUTHORIZED).
Certify only after supported collection, family, and privilege gaps are cured or
disclosed, applying the exact identity, current-state, authority, and revision test.
Create production-control rows for the exact gaps below and hold nonresponsive anomalies.

## Supported actions (commit — 6)

CBP-031-02, CBP-031-04, CBP-031-06, CBP-031-07, CBP-031-08, CBP-031-09.
Each has all four controls effective: immutable identity resolves to one entity,
operative authority is not blocked, current operations are not open/unresolved, and
approval is active with remaining capacity. Their correspondence/privilege records
disclose the business-owner-vs-counterparty discrepancies (e.g. 14% vs 11% for 02;
125 vs 148 records for 06; 40 vs 78 for 07; receipt vs notices email for 08) and are
recorded as disclosed gaps, not certification blockers.

## Evidence holds (preserve — 6)

- **CBP-031-01** — missing effective approval (pending/inactive, capacity 0); also
  population discrepancy 180 (E138) vs 215 (R753).
- **CBP-031-03** — unresolved identity collision (ENT-031-1002 vs ENT-031-2002);
  authority and current state open/block completion.
- **CBP-031-05** — open authority/current state (blocks completion) and missing
  effective approval (pending/inactive, capacity 0).
- **CBP-031-10** — current-operations extract cites superseded REV-2024.2 instead of
  current REV-2025.3.
- **CBP-031-11** — unresolved identity collision (ENT-031-1010 vs ENT-031-2010).
- **CBP-031-12** — open authority/current state (blocks completion).

## Source anchors

Register rows in `output/review_disposition_register.md`; record IDs per key listed
there (identity/authority/current-ops/approval/correspondence = CB-DOC-031-0N,
0(N+12), 0(N+24), 0(N+36), 0(N+48)).

## Alternatives considered

- `aurora-antitrust:shortcut` — certify from production-log totals without checking
  custodians or overlaps. **Rejected: unsupported by current evidence** (ignores the
  identity collisions, open authorities, and superseded revision).
- `aurora-antitrust:blanket-hold` — freeze the entire matter population. **Not selected**;
  requires additional approval and defers all 12 records to 2026-09-08, which is later
  than the supported-action deadline and over-holds the six supported keys.

## Limits

Matter date is 2026-09-05; no external facts assumed. The six holds remain open until
their missing control is cured (identity collision resolved, approval activated, or
superseded revision superseded by the current revision). The latest supported action
(CBP-031-02) carries a control date of 2026-09-03, inside the deadline. Incremental cost
of the scoped approach is $20,000.