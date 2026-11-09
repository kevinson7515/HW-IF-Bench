# Review Note — Project Daybreak Signing Position

Matter CB-MA-2401 · Helios Forge, Inc. / BluePeak Battery Systems LLC · Matter date 2026-09-04
Companion record: `matter_work_product/review_disposition_register.md` (system of record, one row per portfolio key)

## Question presented

Whether the Daybreak signing can proceed, and which tooling or customer-consent gaps must become closing conditions. The client is a carve-out manufacturer that owns cathode tooling in Nevada while its largest automaker customer can terminate upon an indirect change of control.

## Selected approach

`helios-forge:scoped-evidence` — proceed only with supported closing conditions and named cure owners; apply the exact identity, current-state, authority, and revision test; create a closing-condition row for each supported blocker and hold ambiguous entity matches. Outcome: commit 8 supported actions, preserve 4 evidence holds, and finish the latest supported action by 2026-09-03. Incremental cost $18,200. Authority: AUTHORIZED (`12_financials/089_financials_source_export.md` line 90).

The selection follows the protocol's four-control decision rule (lines 80–86): a supported action requires all four controls — immutable identity, operative authority, current operations, and effective approval/revision. Otherwise preserve an evidence hold and state the missing control; do not turn a similar name, a superseded revision, or a pending owner into proof. Reconciling all twelve keys against the four control roles produced exactly 8 supported actions and 4 evidence holds, matching this approach's stated outcome. No external facts were assumed; the matter date is 2026-09-04.

## Supported actions — signing can proceed on these terms

Signing can proceed conditioned on eight supported closing-condition rows, each with a named cure owner drawn from the current responsibility roster (all active as of the matter date). The blocker is real and evidenced in each case, but all four controls reconcile, so each item can be drafted as a closing condition rather than held:

| Key | Subject | Closing condition | Cure owner |
| --- | --- | --- | --- |
| CBP-001-02 | Financial covenant breach | Breach (13% result vs 7% threshold) cured or waived under the executed purchase terms | Sofia Bennett |
| CBP-001-03 | Permit transfer restriction | Required permit transfer obtained (restriction open under R164/E368) | Micah Sullivan |
| CBP-001-04 | Revenue recognition exception | Open exception resolved (R532/E548) | Nora Chen |
| CBP-001-05 | Most-favored-customer exposure | Exposure (18% vs 13% threshold) resolved or consented under the executed terms | Caleb Hassan |
| CBP-001-06 | Unreported security incident | Incident disclosed and resolved with the required approval (Theo Laurent per R990; consistent at E311) | Amara Patel |
| CBP-001-07 | Claims-made insurance tail | Tail placed or the lapse waived (event completed 2025-09-02 vs the 2025-08-05 due date) | Samuel Kim |
| CBP-001-09 | Open-source copyleft exposure | Exposure resolved (R971/E945) | Adrian Mensah |
| CBP-001-10 | Sales-tax nexus gap | Nexus authority for the Delaware activity obtained, or the exposure resolved under the executed terms (activity outside the Washoe County scope of R710) | Farah Ibrahim |

Keys 06 and 07 merit a note on how they passed. Key 06's operative authority and current operations name the same required approver (Theo Laurent), so the approval control is evidenced on both sides and the incident passes; the closing condition carries the disclosure obligation. Key 07's facts show the tail event completed almost a month after its due date, so the item is a late-placement cure, not a clean pass; it remains a supported closing condition because all four controls reconcile.

## Evidence holds — cannot be signed, conditioned, or priced yet

Four keys fail the four-control test. Each is preserved as an evidence hold with the missing control stated; none can be priced as a closing condition or an exception on current evidence because pricing would require treating the unresolved control as if it were satisfied. The matter-level control applies to all of them: the executed purchase terms and the latest consent schedule control; seller summaries do not.

**CBP-001-11 — Change-of-control consent (the customer-consent gap; impact score 93, the highest in the population).** The operative authority requires the consent approval to come from Talia Brooks under R473, but current operations names Caleb Hassan under E439 — a direct approver conflict — and the current responsibility roster shows Dominic Alvarez as pending approval and inactive with zero remaining matter capacity. Two controls fail: current operations (conflicting approver) and effective approval (inactive, zero-capacity owner). Until Talia Brooks is confirmed as the operative approver and an active, capacitated owner is assigned, the automaker consent cannot be matched to the exact acquired entity, and the protocol forbids treating the pending owner as proof. This is the item that governs the indirect change-of-control termination right — the highest-impact exposure in the matter — and it is the reason the customer-consent workstream is a hold rather than a closing condition.

**CBP-001-01 — Charter authorization mismatch (tooling-side entity gap; impact 80).** The portfolio key is associated with both ENT-001-1000 and ENT-001-2000; the display name is shared while the domain and legal-entity fields disagree, and no approved crosswalk revision resolves the collision. Operations also names Jonas Feld (E257) where operative authority requires Maya Ellison (R983). The immutable-identity control fails, so the cathode-tooling records cannot be matched to the exact acquired entity at all — every other control for this key is unusable until identity resolves. This hold is the gateway to the tooling workstream: the tooling chain (keys 01 → 08 → 12) cannot be conditioned until the entity is fixed.

**CBP-001-08 — Anti-assignment restriction (tooling-side assignment gap; impact 81).** Operative authority requires approval from Owen Delgado under R293, but current operations names Nadine Flores under E111, citing the superseded REV-2024.0 where REV-2025.1 is the later effective revision. Both current operations (approver conflict) and effective revision (superseded) fail. The anti-assignment restriction sits directly on the tooling-transfer path, so this hold cannot be priced or conditioned until the correct approver and the controlling revision are established.

**CBP-001-12 — Invention assignment defect (tooling-side IP gap; impact 59).** Operative authority requires approval from Caleb Hassan under R433, but current operations names Willa Novak under E278. The current-operations control fails on the approver conflict. The invention-assignment defect affects the tooling IP chain and stays on hold until the approver is reconciled.

## Why nothing is priced as an exception

The user asked which gaps can be priced. The answer on current evidence is none of them. Pricing an exception requires a quantified, evidenced exposure, and for all four held keys the four-control test fails, so the size of the exposure is itself unevidenced — any number would rest on a similar name (key 01's colliding entities), a superseded revision (key 08's REV-2024.0), or a pending owner (key 11's inactive Dominic Alvarez). The shortcut approach makes exactly this trade and is marked UNSUPPORTED_BY_CURRENT_EVIDENCE. Each hold becomes priceable once its missing control is cured: key 11 once Talia Brooks is confirmed and an active owner assigned, key 01 once the entity collision is resolved by an approved crosswalk revision, key 08 once Owen Delgado is reconciled and REV-2025.1 established as controlling, and key 12 once Caleb Hassan is reconciled as the operative approver. Curing the control is a prerequisite to pricing the exception, not an alternative to it.

## Alternatives considered and rejected

- `helios-forge:shortcut` — release every signature page because the seller says the issues are immaterial; use a plausible summary or one source without completing the controlling joins; same-day disposition of all 12 records while discarding 4 unresolved evidence constraints. Cost $0. Authority: UNSUPPORTED_BY_CURRENT_EVIDENCE. Rejected: it converts the four failed controls into pretend-satisfied ones, directly violating the protocol's prohibition on treating a similar name, a superseded revision, or a pending owner as proof, and it would leave the automaker consent (impact 93) unreconciled at signing.
- `helios-forge:blanket-hold` — freeze the entire matter population; treat supported actions and genuinely ambiguous records as equally unresolved; defer all 12 records until 2026-09-07, including the 8 already supported by current evidence. Cost $26,000. Authority: ADDITIONAL_APPROVAL_REQUIRED. Rejected: it fails the partner-call timeline (signing decision due 2026-09-04) and spends more to defer items the evidence already supports. It remains the fallback if the four holds cannot be cured and the client elects to defer the whole signing.
- A hybrid is available but was not selected because it matches no authorized approach: conditioning the 8 supported keys while pricing the 4 holds as exceptions. Pricing the holds requires the same control cures listed above; without them the prices would be fabricated.

## Source anchors

The population is 96 source-export records: 12 portfolio keys (CBP-001-01 through CBP-001-12) × 8 evidence roles, with the record number determining the role as follows (folder names do not indicate role): records 001–012 identity crosswalk, 013–024 operative authority, 025–036 current operations, 037–048 approval and capacity, 049–060 correspondence, 061–072 financial or population support, 073–084 chronology and custody, 085–096 independent counterrecord. All anchors below are basenames under `attached_files/task_9/`.

Four-control anchors per key (identity · operative · operations · approval):

- CBP-001-01: `001_corporate_source_export.md` · `013_capitalization_source_export.json` · `025_debt_security_source_export.md` · `037_employment_source_export.json`
- CBP-001-02: `002_corporate_source_export.txt` · `014_capitalization_source_export.xml` · `026_debt_security_source_export.txt` · `038_employment_source_export.xml`
- CBP-001-03: `003_corporate_source_export.eml` · `015_capitalization_source_export.html` · `027_debt_security_source_export.eml` · `039_employment_source_export.html`
- CBP-001-04: `004_corporate_source_export.csv` · `016_capitalization_source_export.pdf` · `028_debt_security_source_export.csv` · `040_employment_source_export.pdf`
- CBP-001-05: `005_corporate_source_export.json` · `017_material_contracts_source_export.md` · `029_debt_security_source_export.json` · `041_ip_technology_source_export.md`
- CBP-001-05 operative alternative: `03_material_contracts/017_material_contracts_source_export.md` — the operative-authority record for key 05 (custody record `077_real_property_source_export.json` fixes the operative record at this path).
- CBP-001-06: `006_corporate_source_export.xml` · `018_material_contracts_source_export.txt` · `030_debt_security_source_export.xml` · `042_ip_technology_source_export.txt`
- CBP-001-07: `007_corporate_source_export.html` · `019_material_contracts_source_export.eml` · `031_debt_security_source_export.html` · `043_ip_technology_source_export.eml`
- CBP-001-08: `008_corporate_source_export.pdf` · `020_material_contracts_source_export.csv` · `032_debt_security_source_export.pdf` · `044_ip_technology_source_export.csv`
- CBP-001-09: `009_capitalization_source_export.md` · `021_material_contracts_source_export.json` · `033_employment_source_export.md` · `045_ip_technology_source_export.json`
- CBP-001-10: `010_capitalization_source_export.txt` · `022_material_contracts_source_export.xml` · `034_employment_source_export.txt` · `046_ip_technology_source_export.xml`
- CBP-001-11: `011_capitalization_source_export.eml` · `023_material_contracts_source_export.html` · `035_employment_source_export.eml` · `047_ip_technology_source_export.html`
- CBP-001-12: `012_capitalization_source_export.csv` · `024_material_contracts_source_export.pdf` · `036_employment_source_export.csv` · `048_ip_technology_source_export.pdf`

Protocol and approaches: `12_financials/089_financials_source_export.md` lines 80–101. Impact scores: `12_financials/097_helios_forge_impact_population.xlsx`, sheet "Impact population" (status: retained source population, not a legal disposition). Custody confirmation of operative records: `10_real_property/073_real_property_source_export.md` (key 01), `074_real_property_source_export.txt` (02), `075_real_property_source_export.eml` (03), `076_real_property_source_export.csv` (04), `077_real_property_source_export.json` (05), `078_real_property_source_export.xml` (06), `079_real_property_source_export.html` (07); keys 08–12 confirmed by the same custody series (`073–084` role).

Correspondence and counterrecord roles add no dispositive authority: "Neither message resolves entity identity, revision priority, or approval authority; the source records must be reconciled" (e.g. `07_privacy_security/049_privacy_security_source_export.md`, `08_regulatory/059_regulatory_source_export.eml`), and the counterrecord role "confirms raw activity only" (e.g. `11_tax_insurance/085_tax_insurance_source_export.json`). They corroborate but do not change any disposition.

## Limits

- This note and the register decide no legal effect. They apply the matter work-product protocol to the source population and record which actions the evidence supports; they are not a legal opinion on enforceability of the change-of-control clause, the anti-assignment restriction, or any cure.
- Every source record carries the same reliance limits: it "does not decide legal effect, select among candidate responses, resolve another system's entity identity, or establish that its cited revision is controlling." This review inherits those limits.
- The matter-level control governs: the executed purchase terms and the latest consent schedule control; seller summaries do not. Where a seller summary conflicts with the executed terms, the terms control.
- Impact scores are prioritization input from the impact population workbook, which is a retained source population and not a legal disposition.
- The four evidence holds are stated with their missing controls but are not priced; no monetary quantification of any hold is supported by the current evidence.
- The matter date is 2026-09-04 and no external facts were assumed; all facts come from the 96-record source population and the impact workbook.
- Deliverables are ordinary human-readable matter records; the register is the system of record and this note is its companion.
