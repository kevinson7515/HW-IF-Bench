# Aurora MDL Discovery — Review Note

Matter: CB-LD-2701 · Aurora pricing MDL discovery audit · Matter date: 2026-09-05
Prepared to close the loop with the litigation team before any further representation.

## Selected approach

`aurora-antitrust:scoped-evidence` (AUTHORIZED). Certify only after supported collection,
family, and privilege gaps are cured or disclosed. Commit 6 supported actions, preserve
6 evidence holds, and finish the latest supported action by 2026-09-03. Incremental cost
$20,000.

## Bottom line for the client

Aurora **cannot certify the full MDL production today**. It can certify **6 keys now**;
**6 keys must wait** until their gap is cured. The other two candidate approaches are
unusable: `shortcut` (certify from log totals) is UNSUPPORTED_BY_CURRENT_EVIDENCE, and
`blanket-hold` (freeze all 12) wastes $29,600 and needs additional approval because it
defers 6 records that are already supported.

## Supported actions — certify now (6)

- CBP-031-02 Email-family separation — resolved (14%, E716).
- CBP-031-04 Metadata field loss — disclosed; create a production-control row.
- CBP-031-06 Protective-order designation error — disclosed (148 records, R246).
- CBP-031-07 Production gap — disclosed; control row.
- CBP-031-08 Legal-hold delivery gap — disclosed; correct address identified (R397).
- CBP-031-11 Custodian omission — departed custodian's 98 records identified (R97).

## Evidence holds — must wait (6) + gap + owner

1. **CBP-031-01 Bates-range overlap** — reconcile 180 (E138) vs 215 (R753); owner Samuel Kim is
   pending/inactive, reassign. Owner: Samuel Kim → active owner. (013.json vs 025.md / 061.json)
2. **CBP-031-03 Request-response mismatch** — resolve mismatch blocking completion. Owner: Adrian Mensah.
3. **CBP-031-05 Collection-date inconsistency** — resolve open inconsistency (R821 blocks; E407 open);
   owner Dominic Alvarez pending/inactive, reassign. Owner: Dominic Alvarez → active owner.
4. **CBP-031-09 Clawback deadline** — reconcile due 2025-03-31 (R664) vs completed 05-12 (E503).
   Owner: Jonas Feld.
5. **CBP-031-10 Third-party subpoena deadline** — replace superseded REV-2024.2 with REV-2025.3.
   Owner: Maya Ellison.
6. **CBP-031-12 Common-interest support gap** — resolve privilege/common-interest gap (R908 blocks).
   Owner: Priya Raman.

## What evidence would change the answer

Each hold lifts when its specific control is cured, then it converts to a supported action:

- 01: a single reconciled Bates population (one count, one reference) from the operative order.
- 03: matched request/response pair removing the "blocks completion" condition.
- 05: a resolved collection-date record plus an **active owner with capacity**.
- 09: one operative clawback date (order or docket) resolving due-vs-completed.
- 10: the operative record re-issued at REV-2025.3 (no REV-2024.2 residue).
- 12: privilege challenge ruling or common-interest waiver/document resolving the R908 gap.

## Source anchors

Impact population: `12_case_management/097_aurora_antitrust_impact_population.xlsx`.
Operative-authority and approval records: `02_orders/013…016`, `03_requests_responses/017…024`,
`04_custodian_files/025…032`, `05_email_families/033…040`, `06_chat_exports/041…048`,
`07_privilege_material/049…056`, `08_production_logs/057…064`, `09_depositions/065…072`,
`10_expert_material/073…080`, `11_third_party/081…088`, `12_case_management/089…096`.

## Alternatives considered

- `shortcut` — rejected: unsupported by current evidence (would discard 6 unresolved constraints).
- `blanket-hold` — rejected: over-broad; needs additional approval and defers 6 supported records.

## Limits

No external facts assumed beyond the matter date 2026-09-05. This note states a working
disposition and remediation position; it does not replace court-ordered certification. Provider
records were re-read before finalizing so the recorded result, not the request payload, is confirmed.

## Close-the-loop (Slack)

Reply in channel `C00000031`, thread `1760000031.000005` (005_pleadings_source_export.json) —
do not open a new top-level post, and only after this register and note are committed.
