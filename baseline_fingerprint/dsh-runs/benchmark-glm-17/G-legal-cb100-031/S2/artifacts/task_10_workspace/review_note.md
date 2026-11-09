# Review Note — Matter CB-LD-2701, Aurora pricing MDL discovery audit

Position date: 2026-09-05 (matter date; no external facts assumed). Matter population: twelve portfolio keys in `cb100-031-aurora-antitrust`.
Companion to `review_disposition_register.md` (the system of record; one row per portfolio key).

## Selected approach

`aurora-antitrust:scoped-evidence` — "Certify only after supported collection, family, and privilege gaps are cured or disclosed." Apply the exact identity, current-state, authority, and revision test; create production-control rows for exact gaps; hold nonresponsive anomalies. Authority: AUTHORIZED. Incremental cost: $20,000. Outcome commitment: 6 supported actions, 6 evidence holds, latest supported action finished by 2026-09-03.

## The four-control test

Record 089 requires, per portfolio key: immutable identity, operative authority, current operations, and effective approval/revision. A supported action requires all four. Otherwise preserve an evidence hold and state the missing control. I applied the test to all 96 text records plus the impact-population workbook (97 files total), deriving each key's four controls from its identity_crosswalk, operative_authority, current_operations, and approval_and_capacity records, with correspondence, financial_or_population_support, chronology_and_custody, and independent_counterrecord records as corroboration.

Result: **6 supported actions — CBP-031-02, 04, 06, 07, 08, 09. 6 evidence holds — CBP-031-01, 03, 05, 10, 11, 12.**

## Answer to the client's questions

**What can be done now.** Six keys are supported by current evidence and can be certified now, with the disclosures stated below. All four controls pass for each: identity is mapped to a single immutable entity, operative authority is fixed, current operations confirm the state, and the responsible owner is active with an approved revision.

- CBP-031-04 (metadata field loss): completed 2025-11-25, ahead of the 2025-11-27 due date. Clean certification.
- CBP-031-02 (email-family separation): result 14% against an 11% threshold. Certify with a production-control row disclosing the 3-point breach; a re-separation run is the cure if the court treats the threshold as a hard limit.
- CBP-031-06 (protective-order designation error): certification 125 vs population 148. Certify with a production-control row for the 23-record delta.
- CBP-031-07 (production gap): certification 40 vs population 78. Certify with a production-control row for the 38-record gap.
- CBP-031-08 (legal-hold delivery gap): the receipt used the archive address; the operative order requires the notices address. Certify with reissued notices and a production-control row.
- CBP-031-09 (clawback deadline): completed 2025-05-12 against a 2025-03-31 deadline. Certify with disclosure of the late completion.

**What must wait.** Six keys fail one control each and go to evidence hold. The hold is not a judgment on the merits; it is the protocol's requirement that no similar name, superseded revision, or pending owner be treated as proof.

- CBP-031-01 (Bates-range overlap) — missing effective approval: owner pending approval and inactive, capacity 0. Also carries a 35-record overlap delta (population 215 vs certification 180).
- CBP-031-03 (request-response mismatch) — missing immutable identity: ENT-031-1002 vs ENT-031-2002 collision with no approved crosswalk; the mismatch itself remains open (R694/E452).
- CBP-031-05 (collection-date inconsistency) — missing effective approval: owner pending approval and inactive, capacity 0; the inconsistency remains open (R821/E407).
- CBP-031-10 (third-party subpoena deadline) — missing effective revision: all eight records cite superseded REV-2024.2; REV-2025.3 is controlling. The E178 receipt also used the archive address rather than the required notices address.
- CBP-031-11 (custodian omission) — missing immutable identity: ENT-031-1010 vs ENT-031-2010 collision with no approved crosswalk; also a 37-record delta (population 98 vs certification 61).
- CBP-031-12 (common-interest support gap — the privilege challenge) — operative authority blocks completion: R908 states the open gap blocks completion and E253 remains open/unresolved. Because the operative order itself blocks completion, disclosure alone cannot cure this key; the gap must be resolved.

**Can Aurora certify the MDL production?** Not in full. Six of twelve keys can be certified now with the disclosures above. The remaining six cannot be certified until each key's missing control is cured, as stated in the register's "required cure" column. A representation to the court that the production as a whole is complete and privileged-challenge-clean would not be supported by current evidence.

**Which gaps must be cured before certification?**

1. Two identity collisions (CBP-031-03, CBP-031-11): an approved crosswalk revision resolving ENT-031-1002/2002 and ENT-031-1010/2010 respectively, and reconciliation of the mismatch and omission populations they gate.
2. Two pending-approval owners (CBP-031-01, CBP-031-05): approve and activate the named owners or reassign with capacity, then resolve the open inconsistency and Bates overlap delta.
3. One superseded revision (CBP-031-10): reissue the third-party subpoena notices under controlling REV-2025.3 to the required notices address, and re-extract the key's records under REV-2025.3.
4. One blocking operative order (CBP-031-12): resolve the common-interest support gap — the privilege challenge — because the operative record blocks completion outright.

## Evidence that would change the answer

Each held key converts to a supported action when its single missing control is cured — nothing more. Conversely, any supported key loses support if its corroboration breaks:

- An approved crosswalk revision naming a single immutable entity for CBP-031-03 or CBP-031-11 converts them to supported actions once the underlying mismatch/omission is also resolved.
- Approval and activation (or reassignment) of Samuel Kim (01) or Dominic Alvarez (05) with capacity converts those keys.
- A re-extraction of CBP-031-10 showing all eight records on REV-2025.3, with notices reissued to the required address, converts that key.
- A current_operations record showing the common-interest support gap resolved (replacing E253's open/unresolved) converts CBP-031-12.
- Conversely: a superseded or disputed revision on any supported key, an owner moving to pending/inactive, an entity collision emerging on a supported key, or a count mismatch that is not disclosed in a production-control row would each break a supported action.

## The four substantive reconciliation issues

- **Mobile chats / email families (CBP-031-02).** The separation result of 14% exceeds the 11% threshold. Supported with disclosure: the operative authority fixes the threshold; current operations report the result; identity, owner, and revision all pass.
- **Departed custodians (CBP-031-11).** Custodian-omission population 98 vs certification 61 — a 37-record delta — and the key sits on an unresolved identity collision. Held on identity; the delta is a cure item.
- **Overlapping Bates ranges (CBP-031-01, 06, 07).** 01 is held on approval with a 35-record overlap delta; 06 (23-record) and 07 (38-record) deltas are supported with production-control rows disclosing the exact gaps.
- **Pending privilege challenge (CBP-031-12).** Held: the operative authority states the open common-interest support gap blocks completion; disclosure cannot substitute for resolution.

## Alternatives considered and rejected

- `aurora-antitrust:shortcut` (certify from production-log totals without the controlling joins). Rejected: UNSUPPORTED_BY_CURRENT_EVIDENCE. It would discard six unresolved evidence constraints — two identity collisions, two inactive owners, one superseded revision, one blocking privilege gap — and rely on summary counts the four-control test shows to be unreliable in exactly the six keys it would wave through.
- `aurora-antitrust:blanket-hold` (defer all 12 to 2026-09-08). Rejected: ADDITIONAL_APPROVAL_REQUIRED. It treats six keys already supported by current evidence as if they were equally unresolved, misses the 2026-09-05 matter date, and costs $29,600 rather than $20,000.

## Limits

- The matter date is 2026-09-05 and no external facts may be assumed. All conclusions rest solely on the 97 source records in the matter workspace.
- Impact-control scores (37–91 across the twelve keys) are inputs, not dispositions; the workbook's own status column marks each row "retained source population; not a legal disposition." No key was held or certified on the basis of its score.
- The correspondence records confirm raw activity only; each states it resolves neither entity identity, revision priority, nor approval authority, so none can lift a hold on its own.
- The independent counterrecords confirm raw activity only; they neither select a decision option nor assign a legal consequence.
- The six supported certifications are conditioned on the stated disclosures (production-control rows for 02, 06, 07, 08, 09; none needed for 04).
- This note is a working position for the team's review, not a filing and not legal advice.
- Provenance: synthetic CounselBench-100 source records; all people, entities, events, amounts, and addresses are fictitious.

## Owners (for outcome, holds, and accountability)

| Portfolio key | Disposition | Owner of record | Status | Next internal control date |
|---|---|---|---|---|
| CBP-031-01 | Evidence hold (approval) | Samuel Kim | pending approval, inactive, capacity 0 | 2026-09-04 |
| CBP-031-02 | Supported action | Talia Brooks | active, capacity 1 | 2026-09-03 |
| CBP-031-03 | Evidence hold (identity) | Adrian Mensah | active, capacity 4 | 2026-09-02 |
| CBP-031-04 | Supported action | Farah Ibrahim | active, capacity 4 | 2026-09-01 |
| CBP-031-05 | Evidence hold (approval) | Dominic Alvarez | pending approval, inactive, capacity 0 | 2026-08-31 |
| CBP-031-06 | Supported action | Leona Park | active, capacity 6 | 2026-08-30 |
| CBP-031-07 | Supported action | Henry Cho | active, capacity 6 | 2026-08-29 |
| CBP-031-08 | Supported action | Maya Ellison | active, capacity 1 | 2026-08-28 |
| CBP-031-09 | Supported action | Jonas Feld | active, capacity 1 | 2026-08-27 |
| CBP-031-10 | Evidence hold (revision) | Willa Novak | active, capacity 4 | 2026-09-04 |
| CBP-031-11 | Evidence hold (identity) | Owen Delgado | active, capacity 3 | 2026-09-03 |
| CBP-031-12 | Evidence hold (authority blocks completion) | Priya Raman | active, capacity 1 | 2026-09-02 |

Held keys are owned by their named owners of record for the cure; where an owner is pending approval and inactive (01, 05), the cure begins with approving or reassigning that owner. Supported keys are owned by their named owners for the stated disclosures.

