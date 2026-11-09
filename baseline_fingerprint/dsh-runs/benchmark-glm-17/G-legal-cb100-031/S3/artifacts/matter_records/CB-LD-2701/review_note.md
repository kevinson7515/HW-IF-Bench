# Review Note — CB-LD-2701 Aurora pricing MDL discovery audit

Matter: CB-LD-2701 · Client: Aurora Home Supply Co. (Aurora) · Counterparty: In re Residential Fixture Pricing
Population: `cb100-031-aurora-antitrust`, 12 portfolio keys (CBP-031-01 through CBP-031-12) · Note date: 2026-09-05
Companion document: [Review Disposition Register](review_disposition_register.md) (system of record, one row per portfolio key).

## Selected approach

`aurora-antitrust:scoped-evidence` — *Certify only after supported collection, family, and privilege gaps are cured or disclosed.* This approach is AUTHORIZED under the matter work-product protocol (089_case_management_source_export.md). It applies the exact four-control test per key, creates production-control rows for exact gaps, and holds nonresponsive anomalies. Cost: $20,000. Committed outcome: 6 supported actions, 6 evidence holds, latest supported action finished by 2026-09-03.

The question presented: what can Aurora do now, what must wait, and what evidence would change the answer — can Aurora certify the MDL production, and which gaps must be cured first?

**Answer: Aurora cannot certify the whole production now.** Six keys carry all four controls and can be certified now with disclosed gaps; six keys each fail a named control and must be held until cured.

## Four-control test applied

Each key was tested for (1) immutable identity, (2) operative authority, (3) current operations, and (4) effective approval/revision. A supported action requires all four. A similar name, a superseded revision, or a pending owner is not proof.

## Supported actions (6) — certify now with disclosed gaps

These keys pass all four controls. Each carries an exact gap that must be disclosed in a production-control row; none of the gaps defeats the four controls.

1. **CBP-031-02 — Email-family separation.** Roster: Talia Brooks, active, capacity 1 (038). Operative threshold 11% under CB-LD-2701-R682 (014); operations result 14% under CB-LD-2701-E716 (026). Disclose: separation result exceeds the operative threshold. Owner: Talia Brooks. Next control date 2026-09-03 — **this is the latest supported-action finish date**, consistent with the scoped-evidence outcome.
2. **CBP-031-04 — Metadata field loss.** Roster: Farah Ibrahim, active, capacity 4 (040). Operative due 2025-11-27 under CB-LD-2701-R665 (016); event completed 2025-11-25 under CB-LD-2701-E980 (028). Completion preceded the due date; certify. Owner: Farah Ibrahim. Next control date 2026-09-01.
3. **CBP-031-06 — Protective-order designation error.** Roster: Leona Park, active, capacity 6 (042). Operative population 148 records under CB-LD-2701-R246 (018); certification covers 125 records under CB-LD-2701-E214 (030). Disclose: certification 125 vs population 148. Owner: Leona Park. Next control date 2026-08-30.
4. **CBP-031-07 — Production gap.** Roster: Henry Cho, active, capacity 6 (043). Operative population 78 records under CB-LD-2701-R626 (019); certification covers 40 records under CB-LD-2701-E660 (031). Disclose: certification 40 vs population 78. Owner: Henry Cho. Next control date 2026-08-29.
5. **CBP-031-08 — Legal-hold delivery gap.** Roster: Maya Ellison, active, capacity 1 (044). Operative: notices must use notices-aurora_home_supply_co@example.test under CB-LD-2701-R397 (020); operations: receipt used archive-in_re_residential_fixture_pricing@example.test under CB-LD-2701-E382 (032). Disclose: wrong notice address; correct going forward. Owner: Maya Ellison. Next control date 2026-08-28.
6. **CBP-031-09 — Clawback deadline.** Roster: Jonas Feld, active, capacity 1 (045). Operative due 2025-03-31 under CB-LD-2701-R664 (021); event completed 2025-05-12 under CB-LD-2701-E503 (033). Disclose: completion after the due date. Owner: Jonas Feld. Next control date 2026-08-27.

## Evidence holds (6) — preserve; state missing control

These keys each fail one or more controls. Disposition: preserve evidence hold; do not certify until the named control is cured.

1. **CBP-031-01 — Bates-range overlap. Missing control: approval.** Roster: Samuel Kim, pending approval, inactive, capacity 0 (037). Identity, operative (population 215, CB-LD-2701-R753, 013), and operations (certification 180, CB-LD-2701-E138, 025) pass. Cure: approved, active roster entry. On cure, also disclose certification 180 vs population 215. Owner: Samuel Kim (roster). Next control date 2026-09-04.
2. **CBP-031-03 — Request-response mismatch. Missing control: identity.** Entity collision: CBP-031-03 maps to both ENT-031-1002 and ENT-031-2002; no approved crosswalk revision resolves it (003). Operative: open mismatch blocks completion under CB-LD-2701-R694 (015). Roster passes (Adrian Mensah, active, 039). Cure: approved crosswalk revision resolving the collision; then close the open mismatch under R694. Owner: Adrian Mensah. Next control date 2026-09-02.
3. **CBP-031-05 — Collection-date inconsistency (mobile chats). Missing controls: approval; operative blocker.** Roster: Dominic Alvarez, pending approval, inactive, capacity 0 (041). Operative: open collection-date inconsistency blocks completion under CB-LD-2701-R821 (017); operations status open and unresolved, CB-LD-2701-E407 (029). Cure: approved, active roster entry and closure of the mobile-chat collection-date inconsistency under R821. Owner: Dominic Alvarez. Next control date 2026-08-31.
4. **CBP-031-10 — Third-party subpoena deadline. Missing control: revision.** Operations cite superseded REV-2024.2 while REV-2025.3 is the later effective revision (022, 034, 046). Roster passes (Willa Novak, active, 046). Cure: re-run and re-cite current operations under REV-2025.3; notices must use the court-ordered notices-aurora_home_supply_co@example.test address (R537). Owner: Willa Novak. Next control date 2026-09-04.
5. **CBP-031-11 — Custodian omission (departed custodians). Missing control: identity.** Entity collision: CBP-031-11 maps to both ENT-031-1010 and ENT-031-2010; no approved crosswalk revision resolves it (011). Operative population 98 under CB-LD-2701-R976 (023); certification 61 under CB-LD-2701-E151 (035). Roster passes (Owen Delgado, active, 047). Cure: approved crosswalk revision resolving the collision; then reconcile certification 61 vs population 98. Owner: Owen Delgado. Next control date 2026-09-03.
6. **CBP-031-12 — Common-interest support gap (privilege challenge). Missing control: operative authority.** Operative: open common-interest support gap blocks completion under CB-LD-2701-R908 (024); operations status open and unresolved, CB-LD-2701-E253 (036). Identity and roster pass (Priya Raman, active, 048). Cure: resolve the common-interest support gap underlying the pending privilege challenge. Owner: Priya Raman. Next control date 2026-09-02.

## Evidence that would change the answer

For each hold, specific evidence would convert it to a supported action:

- **Keys 03, 11 (identity collisions):** an approved crosswalk revision resolving ENT-031-1002 vs ENT-031-2002 and ENT-031-1010 vs ENT-031-2010, respectively.
- **Key 10 (stale revision):** current operations re-issued under REV-2025.3 (not the superseded REV-2024.2), with notices sent to the court-ordered address.
- **Keys 01, 05 (pending owners):** roster entries approved and activated (Samuel Kim; Dominic Alvarez) with capacity restored.
- **Keys 05, 12 (operative blockers):** documented closure of the collection-date inconsistency under R821 and of the common-interest support gap under R908.
- **Key 01 (on cure):** an operative order or reconciliation resolving the 180-vs-215 Bates-range overlap, so the disclosed gap has a controlling figure.

No external facts were assumed; all findings trace to the 96 source files in `attached_files/task_10/` and the matter protocol at `12_case_management/089_case_management_source_export.md`.

## Alternatives considered and rejected

- **`aurora-antitrust:shortcut`** — certify from production log totals without checking custodians or overlaps. Rejected: UNSUPPORTED_BY_CURRENT_EVIDENCE. It would create a same-day disposition for all 12 records while discarding 6 unresolved evidence constraints (2 identity collisions, 1 stale revision, 2 pending owners, 1 operative blocker) — precisely what the protocol forbids: turning a similar name, superseded revision, or pending owner into proof.
- **`aurora-antitrust:blanket-hold`** — freeze the entire matter population until 2026-09-08. Rejected: ADDITIONAL_APPROVAL_REQUIRED and inferior on the evidence. It would defer 6 keys already supported by all four controls (02, 04, 06, 07, 08, 09), miss the 2026-09-03 finish committed in the authorized approach, and cost $29,600 vs $20,000.

## Reliance limits

- The 12 impact_control_score values in 097_aurora_antitrust_impact_population.xlsx (33–91) are inputs, not legal dispositions; none was used to rank or decide any key.
- Source files state reliance limits individually: none decides legal effect, selects among candidate responses, resolves another system's entity identity, or establishes that its cited revision is controlling. Dispositions here rest on the four-control test, not on any single file's characterization.
- The 097 xlsx confirms key-to-entity mapping and that source populations are retained, "not a legal disposition."
- Correspondence records (049–060) frame the disputes but resolve nothing: "Neither message resolves entity identity, revision priority, or approval authority; the source records must be reconciled." This note performs that reconciliation.
- This note and the register record the working position as of 2026-09-05. Cures listed above would change the holds; nothing else in the record does.
