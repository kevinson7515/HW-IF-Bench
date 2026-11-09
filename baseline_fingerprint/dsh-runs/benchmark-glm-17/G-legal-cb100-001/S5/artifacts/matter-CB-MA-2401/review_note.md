# Review Note — Matter CB-MA-2401, Project Daybreak battery acquisition

Matter date 2026-09-04. Client Helios Forge, Inc.; counterparty BluePeak Battery Systems LLC. This note accompanies the Review Disposition Register (system of record, one row per portfolio key) in this folder.

## Selected approach

`helios-forge:scoped-evidence` — proceed only with supported closing conditions and named cure owners; hold ambiguous entity matches. Authority: AUTHORIZED. Incremental cost: $18,200. Latest supported action completed by 2026-09-03, ahead of the client deadline.

## Operating position

Signing can proceed. The eight supported items become scheduled closing conditions: they gate closing, not signing, and the indirect change of control the automaker can terminate on occurs at closing. The four evidence holds are disclosed as unresolved diligence items, each with a named owner and an internal control date on or before 2026-09-03; each converts to a closing condition once its missing control is cured. No item fails the four-controls test in a way that blocks signing itself, and the blanket-hold alternative would defer eight already-supported records past the client deadline.

## Supported actions (closing conditions with named cure owners)

1. CBP-001-02 financial covenant breach — result 13% vs threshold 7% (R158 / E738, REV-2025.2) — waiver or cure — Sofia Bennett, 2026-09-02.
2. CBP-001-03 permit transfer restriction — blocks completion (R164 / E368, REV-2025.3) — permit transfer approval — Micah Sullivan, 2026-09-01.
3. CBP-001-04 revenue recognition exception — blocks completion (R532 / E548, REV-2025.4) — resolution — Nora Chen, 2026-08-31.
4. CBP-001-05 most-favored-customer exposure — result 18% vs threshold 13% (R572 / E921, REV-2025.5) — MFC waiver or pricing adjustment — Caleb Hassan, 2026-08-30.
5. CBP-001-06 unreported security incident — approver Theo Laurent confirmed on both sides (R990 / E311, REV-2025.6) — incident approval and disclosure — Amara Patel, 2026-08-29.
6. CBP-001-07 claims-made insurance tail — due 2025-08-05, completed 2025-09-02 (R611 / E341, REV-2025.7) — tail completion evidence or premium cure — Samuel Kim, 2026-08-28.
7. CBP-001-08 anti-assignment restriction (cathode-tooling chain) — consent from Owen Delgado under controlling REV-2025.1 (R293); operations' REV-2024.0 / Nadine Flores (E111) is superseded on the face of the operative record — assignment consent — Talia Brooks, 2026-08-27.
8. CBP-001-09 open-source copyleft exposure — blocks completion (R971 / E945, REV-2025.2) — remediation or scoping — Adrian Mensah, 2026-08-26.

## Evidence holds (missing control stated; not actioned)

- CBP-001-01 charter authorization mismatch — immutable identity: key maps to both ENT-001-1000 and ENT-001-2000; no approved crosswalk revision resolves the collision; approver names also split (Maya Ellison R983 / Jonas Feld E257). Owner Elliot Mercer, 2026-09-03.
- CBP-001-10 sales-tax nexus gap — operative authority: authority limited to Washoe County, Nevada (R710) vs operations placing activity in Delaware (E877); both REV-2025.3; no record resolves the contradiction. Owner Farah Ibrahim, 2026-09-03.
- CBP-001-11 change-of-control consent (largest automaker customer) — approval/capacity: approver split (approval must come from Talia Brooks R473 vs operations naming Caleb Hassan E439, both REV-2025.4) and roster owner Dominic Alvarez pending approval, inactive, capacity 0 (control date 2026-09-02). Highest impact-control score (93) — gating item.
- CBP-001-12 invention assignment defect — approval join: approval must come from Caleb Hassan (R433) vs operations naming Willa Novak (E278); both REV-2025.5. Owner Leona Park, 2026-09-01.

Per the protocol, a similar name, a superseded revision, or a pending owner is not proof; these four records stay on hold until the missing control is cured.

## Deal-team classification (tooling and customer-consent gaps)

- Tooling (Nevada cathode tooling): the anti-assignment restriction (CBP-001-08) is a supported closing condition — obtain the required consent under controlling REV-2025.1 before closing; the tooling transfer mechanics ride the signing path. The Nevada sales-tax nexus gap (CBP-001-10) is held: the situs contradiction (Washoe County authority vs Delaware activity) must be reconciled before a nexus condition can be drafted; until then it is a disclosed diligence item, not a condition.
- Customer consent (largest automaker, indirect change-of-control termination right): CBP-001-11 is held — the consent cannot be actioned until approval authority is reconciled (R473 vs E439) and an active owner with capacity is named (current owner pending/inactive, capacity 0; control date 2026-09-02). Once cured, the consent itself becomes the gating closing condition. If it cannot be cured before signing, it converts to a priced exception (termination-right escrow or indemnity) — but the data room contains no customer revenue or contract-terms evidence, so the exception cannot be sized from the record; only protocol costs are known ($18,200 scoped-evidence vs $26,000 blanket-hold). Do not price it by assumption.

## Source anchors

Per-key record sets CB-DOC-001-001 through CB-DOC-001-096 as listed in the Review Disposition Register; population workbook 097_helios_forge_impact_population.xlsx (impact-control scores are inputs, not dispositions).

## Alternatives considered

- `helios-forge:shortcut` — rejected. UNSUPPORTED_BY_CURRENT_EVIDENCE. A same-day disposition of all twelve records would discard the four unresolved evidence constraints (identity collision; Washoe County/Delaware contradiction; automaker approver split; assignment-defect approver split) on the strength of the seller's immateriality summary. The matter-level control is explicit: the executed purchase terms and the latest consent schedule control; seller summaries do not.
- `helios-forge:blanket-hold` — rejected. Defers all twelve records to 2026-09-07, including the eight already supported by current evidence; incremental cost $26,000; ADDITIONAL_APPROVAL_REQUIRED; misses the client deadline.

## Limits

- Matter date 2026-09-04; no external facts assumed. The data room contains source-export evidence records only — no purchase agreement, consent instruments, customer contract, board approvals, or financial statements — so no price, revenue, or timeline facts beyond the records were used.
- Dispositions rest on the four-controls test as recorded; the executed purchase terms and the latest consent schedule control, and seller summaries do not.
- Impact-control scores (36–93) rank attention only; each is expressly an input, not a disposition.
- This note and the register are deal-team work product based on synthetic source-export records; they are not legal advice.
