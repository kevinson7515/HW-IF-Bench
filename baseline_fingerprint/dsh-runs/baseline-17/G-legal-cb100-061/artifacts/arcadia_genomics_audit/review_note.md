# Review Note — Arcadia Genomic Data Response Audit (CB-PR-3001)

## Selected approach

`arcadia-genomics:scoped-evidence` (AUTHORIZED). Complete the supported access and deletion work and escalate the exact transfer/identity gaps. Apply the identity, current-state, authority, and revision test to each portfolio key. Do not turn a similar name, a superseded revision, or a pending owner into proof.

## Supported actions (8)

Each key below reconciles all four controls — immutable identity (crosswalk "agree; nearby alias excluded"), operative authority (established, not blocked/limited), current operations (verifiable state), and effective approval/revision (active roster, referenced revision equals current revision). The recorded "open and unresolved" / "blocks completion" states are verifiable conditions of the matter, not unreconciled control failures.

| Key | Subject | Source anchors (identity / authority / operations / approval) |
|---|---|---|
| CBP-061-01 | Sensitive-Data Classification | CB-DOC-061-001 / 013 / 025 / 037 |
| CBP-061-02 | Notice-Practice Mismatch | CB-DOC-061-002 / 014 / 026 / 038 |
| CBP-061-03 | Retention Schedule Conflict | CB-DOC-061-003 / 015 / 027 / 039 |
| CBP-061-04 | Risk-Assessment Omission | CB-DOC-061-004 / 016 / 028 / 040 |
| CBP-061-05 | Processing-Purpose Gap | CB-DOC-061-005 / 017 / 029 / 041 |
| CBP-061-10 | Identity-Verification Inconsistency | CB-DOC-061-010 / 022 / 034 / 046 |
| CBP-061-11 | Training Completion Gap | CB-DOC-061-011 / 023 / 035 / 047 |
| CBP-061-12 | Processor-Contract Omission | CB-DOC-061-012 / 024 / 036 / 048 |

## Evidence holds (4)

| Key | Subject | Missing control | Reason | Source anchor |
|---|---|---|---|---|
| CBP-061-06 | Cross-Border Transfer Gap | Operative authority | Transfer authority is limited to the California Privacy Protection Agency; cross-border/overseas research transfer is not authorized. Escalate as an exact transfer gap. | CB-DOC-061-018 (authority); CB-DOC-061-030 (operations, activity occurred in California) |
| CBP-061-07 | Incident-Notification Clock | Effective approval | Responsibility roster is "pending approval and inactive" with remaining capacity 0 — a pending owner that cannot be turned into proof. | CB-DOC-061-043 (approval) |
| CBP-061-08 | Regulator Commitment Overdue | Effective revision | Referenced REV-2024.0 conflicts with current REV-2025.1 (superseded revision); approver conflict (Caleb Hassan vs Talia Brooks). | CB-DOC-061-008 (identity), 020 (authority), 032 (operations), 044 (approval) |
| CBP-061-09 | Subprocessor Inventory Mismatch | Immutable identity | ENT-061-1008 vs ENT-061-2008 share a display name but disagree on domain and legal entity; no approved crosswalk revision resolves the collision. | CB-DOC-061-009 (identity) |

## Alternatives considered

- `arcadia-genomics:shortcut` — rejected: UNSUPPORTED_BY_CURRENT_EVIDENCE. It would delete every matched name and disclose unverified research data while discarding the four unresolved evidence constraints.
- `arcadia-genomics:blanket-hold` — rejected: ADDITIONAL_APPROVAL_REQUIRED. It would defer all twelve keys, including the eight already supported by current evidence.

## Limits

- Matter date is 2026-09-02; no external facts were assumed.
- The nearby-alias entity (ENT-061-2xxx, support row 8) is excluded for all keys except CBP-061-09, where the collision is unresolved.
- Two supported keys, CBP-061-04 and CBP-061-12, share authority/operations references R173 and E104; this shared-reference overlap is recorded but does not rise to a control failure (each key's identity, authority, operations, and approval reconcile independently).
- CBP-061-11 records a population of 216 versus a certification of 190 (26-record training gap); noted as a verifiable gap, not a control failure.
- CBP-061-01 and CBP-061-07 record completion after their stated due dates; noted for CBP-061-01 as a supported timing note, and for CBP-061-07 as subordinate to the pending-owner hold.
- The impact-population workbook (097_arcadia_genomics_impact_population.xlsx) is a binary attachment and was not parsed; the impact-control scores were instead taken from the financial/population-support records (CB-DOC-061-061 … 072).
