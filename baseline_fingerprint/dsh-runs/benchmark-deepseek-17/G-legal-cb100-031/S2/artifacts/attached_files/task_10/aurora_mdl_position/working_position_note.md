# Aurora MDL Production — Working Position Note

Matter: CB-LD-2701 — Aurora pricing MDL discovery audit
Prepared for: litigation team representation due 2026-09-05
Approach: `aurora-antitrust:scoped-evidence` — AUTHORIZED

## Bottom line

Aurora **cannot certify the full MDL production now**. Six of twelve portfolio keys are
supported and can be certified immediately with disclosure; six must be held until specific
gaps are cured. Certification must be scoped, not blanket: certify the six supported keys,
create production-control rows for the disclosed residual discrepancies, and preserve six
evidence holds with named owners and the missing control stated.

## Selected approach and why

`aurora-antitrust:scoped-evidence` is the only AUTHORIZED route. It applies the exact
identity / current-state / authority / revision test per key: certify only where all four
controls hold, disclose curable numeric/address discrepancies, and hold nonresponsive or
blocking anomalies.

Rejected alternatives:
- `aurora-antitrust:shortcut` (certify from production-log totals without checking custodians
  or overlaps) — **UNSUPPORTED**.
- `aurora-antitrust:blanket-hold` (freeze everything) — **ADDITIONAL_APPROVAL_REQUIRED**;
  over-broad and unnecessary because six keys are already certifiable.

## What Aurora can certify now (6 supported actions)

| Key | Subject | Owner | Disclosure on the certification |
|---|---|---|---|
| CBP-031-02 | Email-family separation | Talia Brooks | Result 14% exceeds 11% threshold (E716 vs R682) |
| CBP-031-04 | Metadata field loss | Farah Ibrahim | Event completed 2025-11-25, before 2025-11-27 deadline |
| CBP-031-06 | Protective-order designation error | Leona Park | Certified 125 vs operative 148 records |
| CBP-031-07 | Production gap | Henry Cho | Certified 40 vs operative 78 records |
| CBP-031-08 | Legal-hold delivery gap | Maya Ellison | Receipt used archive@ vs required notices@ |
| CBP-031-09 | Clawback deadline | Jonas Feld | Clawback completed 2025-05-12, after 2025-03-31 deadline |

Each supported key has all four controls satisfied; the listed discrepancy is disclosed in a
production-control row, not silently certified.

## What must wait (6 evidence holds) and what cures each

| Key | Subject | Missing control | Cure / owner |
|---|---|---|---|
| CBP-031-01 | Bates-range overlap | Approval (pending, capacity 0) | Samuel Kim approves + reconcile 180 (E138) vs 215 (R753) Bates count |
| CBP-031-03 | Request-response mismatch | Identity + Authority + Current | Resolve ENT-031-1002 vs ENT-031-2002 collision; close open mismatch (R694/E452) — Adrian Mensah |
| CBP-031-05 | Collection-date inconsistency | Authority + Current + Approval | Close open inconsistency (R821/E407); Dominic Alvarez approval (pending, capacity 0) |
| CBP-031-10 | Third-party subpoena deadline | Revision | Reconcile REV-2025.3 (crosswalk) vs REV-2024.2 (source) + address mismatch — Willa Novak |
| CBP-031-11 | Custodian omission | Identity | Resolve ENT-031-1010 vs ENT-031-2010 collision; collect departed custodians (61 vs 98) — Owen Delgado |
| CBP-031-12 | Common-interest support gap | Authority + Current | Close open gap (R908/E253) — Priya Raman |

## Mapping to the four named reconciliation issues

- **Overlapping Bates ranges** → CBP-031-01 (hold): 180 vs 215 records and unapproved sign-off.
- **Departed custodians** → CBP-031-11 (hold): entity collision plus 61-of-98 custodian shortfall.
- **Mobile chats / collection** → CBP-031-05 (hold) and CBP-031-03 (hold): open collection-date
  inconsistency and request-response mismatch block chat-collection completeness.
- **Pending privilege challenge** → CBP-031-12 (hold, common-interest support gap) with CBP-031-06,
  08, 09 supported-but-disclosed privilege designations.

## What evidence would change the answer

- **01** — a revised Bates population reconciling 180 vs 215, or a signed approval, converts the
  hold to supported-with-disclosure.
- **03 / 05 / 12** — a close-out of the "blocks completion" / "open and unresolved" records
  (e.g., a supplemental production or stipulation) cures the authority + current-state failures.
- **10** — a single consistent revision across the crosswalk and source population (and the
  correct delivery address) cures the revision hold.
- **11** — a resolved entity crosswalk and the collected departed-custodian data (61 → 98) cures
  the identity hold.
- Any key currently "supported" would downgrade to hold if its disclosure is challenged as a
  material omission rather than a disclosed residual.

## Limits

- Matter date 2026-09-05; no external facts are assumed. All determinations are drawn from the
  CB-DOC-031 source records and the impact population `097_aurora_antitrust_impact_population.xlsx`.
- Impact-control scores in the xlsx are inputs, not dispositions, and were not used to override the
  four-control test.
- Completion route: reply in Slack channel `C00000031`, thread `1760000031.000005`
  (`005_pleadings_source_export.json`); do not open a new top-level post. Use only after this
  register and note are committed; re-open each changed provider record before finishing so the
  recorded result, not the request payload, is confirmed.
