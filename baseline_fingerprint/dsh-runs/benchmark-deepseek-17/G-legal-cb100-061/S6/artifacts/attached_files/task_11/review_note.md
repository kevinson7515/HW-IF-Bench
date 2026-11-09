# Review note — CB-PR-3001 Arcadia genomic data response audit

## Selected approach

`arcadia-genomics:scoped-evidence` (Authority: AUTHORIZED). Apply the identity,
current-state, authority, and revision test per portfolio key; commit supported access and
deletion work; escalate exact transfer gaps; preserve an evidence hold where a control is
missing.

## Supported actions (8)

CBP-061-01 (sensitive-data classification), CBP-061-02 (notice-practice mismatch),
CBP-061-03 (retention schedule conflict), CBP-061-04 (risk-assessment omission),
CBP-061-05 (processing-purpose gap), CBP-061-10 (identity-verification inconsistency),
CBP-061-11 (training completion gap), CBP-061-12 (processor-contract omission).

Each satisfies all four controls: identity crosswalk resolves to a single entity, operative
authority is stated, current operations are current (complete or open-and-unresolved, not
superseded), and approval is active with a controlling revision.

## Evidence holds (4)

- CBP-061-06 (cross-border transfer gap) — missing operative authority. CB-DOC-061-018
  records that transfer authority is "limited to California Privacy Protection Agency"
  (CB-PR-3001-R637), which does not extend to the overseas research transfer; current
  operations (CB-DOC-061-030) record the activity in California. Escalate as a transfer gap.
- CBP-061-07 (incident-notification clock) — missing effective approval. CB-DOC-061-043
  records the responsibility roster as "pending approval and inactive" with remaining matter
  capacity 0 (pending owner).
- CBP-061-08 (regulator commitment overdue) — missing effective revision. CB-DOC-061-020
  states operations cite REV-2024.0 while REV-2025.1 is the later effective revision; the
  superseded revision repeats across CB-DOC-061-008, -032, and -044.
- CBP-061-09 (subprocessor inventory mismatch) — missing immutable identity. CB-DOC-061-009
  records the key as associated with both ENT-061-1008 and ENT-061-2008 with no approved
  crosswalk revision resolving the collision.

## Source anchors

Control records (identity = -001..-012, authority = -013..-024, current operations =
-025..-036, approval = -037..-048) for each key; impact population
097_arcadia_genomics_impact_population.xlsx (CBP-061-08 source revision REV-2024.0).
Supporting correspondence, financial/population, chronology, and independent-counterrecord
exports are non-controlling.

## Alternatives

- `arcadia-genomics:shortcut` — rejected; UNSUPPORTED_BY_CURRENT_EVIDENCE (would discard
  4 unresolved evidence constraints and produce an unsupported same-day disposition).
- `arcadia-genomics:blanket-hold` — rejected; ADDITIONAL_APPROVAL_REQUIRED (would defer
  all 12, including the 8 already supported).

## Limits

Matter date is 2026-09-02; no external facts assumed. The register and this note are the
system of record; disposition derives only from the task-scoped native records above.
