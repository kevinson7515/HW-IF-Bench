# Review Note — Aurora Pricing MDL Discovery Audit (CB-LD-2701)

Matter: In re Residential Fixture Pricing, multidistrict antitrust production — client Aurora Home Supply Co.
Matter date: 2026-09-05. This note records the review method, the selected approach, the supported actions, the evidence holds, the source anchors, the rejected alternatives, and the limits of the position. The Review Disposition Register (`output/review_disposition_register.md`) is the system of record for the per-key rows; this note is the accompanying review-note prose.

## 1. Question presented

The client asked: what can it do now, what must wait, and what evidence would change the answer. Can Aurora certify the MDL production, and which gaps must be cured before certification? The litigation team needs a defensible production and remediation position before making another representation, by 2026-09-05.

## 2. Method

The review applied the four-control join test defined in the matter protocol (`12_case_management/089_case_management_source_export.md`, matter work-product protocol section, lines 82–86): for each of the twelve portfolio keys CBP-031-01 through CBP-031-12, reconcile (1) immutable identity, (2) operative authority, (3) current operations, and (4) effective approval/revision. A supported action requires all four controls; otherwise an evidence hold is preserved and the missing control is stated.

For each key, the review read the operative-authority record (reference CB-LD-2701-Rnnn), the current-operations record (reference CB-LD-2701-Ennn), the approval-and-capacity roster record, the identity-crosswalk record, the correspondence record, the financial-or-population-support record (impact-control score), and the independent counterrecord. Records appear across eight file formats (md, txt, eml, csv, json, xml, html, pdf) in twelve source folders; every record was read in its native file. Correspondence records were given no controlling weight: each states that neither message resolves entity identity, revision priority, or approval authority. Impact-control scores were treated as inputs, not dispositions, per their own text. The supporting population workbook `097_aurora_antitrust_impact_population.xlsx` was read with inline-string parsing.

## 3. Selected approach

`aurora-antitrust:scoped-evidence` — Certify only after supported collection, family, and privilege gaps are cured or disclosed. Apply the exact identity, current-state, authority, and revision test. Create production-control rows for exact gaps and hold nonresponsive anomalies. Outcome: commit 6 supported actions, preserve 6 evidence holds, and finish the latest supported action by 2026-09-03. Incremental cost: $20,000. Authority: AUTHORIZED.

## 4. Supported actions (6)

Each key below passes all four controls. Where the current-operations result diverges from the operative authority, the divergence is disclosed rather than treated as a failed control.

- **CBP-031-04 (metadata field loss).** Clean identity; R665 deadline 2025-11-27; E980 shows completion 2025-11-25, two days early. Owner Farah Ibrahim, active, capacity 4. No defect. Anchor: 016 pdf.
- **CBP-031-06 (protective-order designation error).** Clean identity; R246 population 148; E214 certification covers 125. The 23-record gap is an exact, quantified gap: it is recorded as a production-control row and disclosed, not held. Owner Leona Park, active, capacity 6. Anchor: 018 txt.
- **CBP-031-07 (production gap).** Clean identity; R626 population 78; E660 certification covers 40. The 38-record gap is an exact, quantified gap recorded as a production-control row and disclosed. Owner Henry Cho, active, capacity 6. Anchor: 019 eml.
- **CBP-031-08 (legal-hold delivery gap).** Clean identity; R397 requires notices to notices-aurora_home_supply_co@example.test; E382 shows the receipt used archive-in_re_residential_fixture_pricing@example.test. Re-issue the notice to the required address. Owner Maya Ellison, active, capacity 1. Anchor: 020 csv.
- **CBP-031-09 (clawback deadline).** Clean identity; R664 due 2025-03-31; E503 shows completion 2025-05-12, forty-two days late, with no extension evidence. The event completed; the lateness is disclosed, not cured. Owner Jonas Feld, active, capacity 1. Anchor: 021 json.
- **CBP-031-02 (email-family separation).** Clean identity; R682 threshold 11%; E716 result 14%. The result exceeds the operative threshold by three points: disclosed. Owner Talia Brooks, active, capacity 1. Anchor: 014 xml.

Sequencing (all before the 2026-09-05 matter date): CBP-031-09 by 2026-08-27 (Jonas Feld), CBP-031-08 by 2026-08-28 (Maya Ellison), CBP-031-07 by 2026-08-29 (Henry Cho), CBP-031-06 by 2026-08-30 (Leona Park), CBP-031-04 by 2026-09-01 (Farah Ibrahim), CBP-031-02 by 2026-09-03 (Talia Brooks). The latest supported action therefore finishes by 2026-09-03, matching the approach outcome.

## 5. Evidence holds (6)

Each hold names the missing control, as the protocol requires.

- **CBP-031-01 (Bates-range overlap) — effective approval.** Identity and revisions agree, but the responsibility roster names Samuel Kim, pending approval and inactive, capacity 0 (next control date 2026-09-04). A pending owner cannot supply effective approval. Separately, certification covers 180 of the 215-record population (R753 vs E138); the 35-record shortfall must be cured or disclosed once an approver is in place. Anchors: 001 md; 013 json; 025 md; 037 json; 049 md; 061 json.
- **CBP-031-03 (request-response mismatch) — immutable identity.** The key maps to both ENT-031-1002 and ENT-031-2002 (003 eml); domain and legal-entity fields disagree and no approved crosswalk revision resolves the collision. Operative authority (R694) states the open mismatch blocks completion, and current operations (E452) report the status open and unresolved. Anchors: 003 eml; 015 html; 027 eml; 051 eml.
- **CBP-031-05 (collection-date inconsistency) — effective approval.** The roster names Dominic Alvarez, pending approval and inactive, capacity 0 (next control date 2026-08-31). Operative authority (R821) states the open inconsistency blocks completion and current operations (E407) report open and unresolved. Anchors: 005 json; 017 md; 029 json; 041 md; 053 json.
- **CBP-031-10 (third-party subpoena deadline) — effective revision.** Operations cite superseded REV-2024.2 while the operative record (022 xml, R537) states REV-2025.3 is the later effective revision. The receipt (E178) also used the archive address instead of notices-aurora_home_supply_co@example.test. Anchors: 010 txt; 022 xml; 034 txt; 058 txt.
- **CBP-031-11 (custodian omission) — immutable identity.** The key maps to both ENT-031-1010 and ENT-031-2010 (011 eml); no approved crosswalk revision resolves the collision. Certification covers 61 of the 98-record population (R976 vs E151); the 37-record shortfall must be cured or disclosed after the identity is fixed. Anchors: 011 eml; 023 html; 035 eml; 059 eml.
- **CBP-031-12 (common-interest support gap) — current operations.** Identity, approval, and revision agree, but operative authority (R908) states the open common-interest support gap blocks completion and current operations (E253) report the status open and unresolved. There is no completed operation to support; certification cannot cover a status the operative record describes as blocking. Anchors: 012 csv; 024 pdf; 036 csv; 060 csv.

## 6. Source anchors (per key)

| Key | Identity | Operative authority | Current operations | Approval | Correspondence | Impact | Chronology/custody | Counterrecord |
|---|---|---|---|---|---|---|---|---|
| 01 | 001 md | 013 json | 025 md | 037 json | 049 md | 061 json | 073 md | 085 json |
| 02 | 002 txt | 014 xml | 026 txt | 038 xml | 050 txt | 062 xml | 074 txt | 086 xml |
| 03 | 003 eml | 015 html | 027 eml | 039 html | 051 eml | 063 html | 075 eml | 087 html |
| 04 | 004 csv | 016 pdf | 028 csv | 040 pdf | 052 csv | 064 pdf | 076 csv | 088 pdf |
| 05 | 005 json | 017 md | 029 json | 041 md | 053 json | 065 md | 077 json | 089 md |
| 06 | 006 xml | 018 txt | 030 xml | 042 txt | 054 xml | 066 txt | 078 xml | 090 txt |
| 07 | 007 html | 019 eml | 031 html | 043 eml | 055 html | 067 eml | 079 html | 091 eml |
| 08 | 008 pdf | 020 csv | 032 pdf | 044 csv | 056 pdf | 068 csv | 080 pdf | 092 csv |
| 09 | 009 md | 021 json | 033 md | 045 json | 057 md | 069 json | 081 md | 093 json |
| 10 | 010 txt | 022 xml | 034 txt | 046 xml | 058 txt | 070 xml | 082 txt | 094 xml |
| 11 | 011 eml | 023 html | 035 eml | 047 html | 059 eml | 071 html | 083 eml | 095 html |
| 12 | 012 csv | 024 pdf | 036 csv | 048 pdf | 060 csv | 072 pdf | 084 csv | 096 pdf |

(Files named by record number and format; full paths under `attached_files/task_10/`, in folders 01_pleadings through 12_case_management by record number. The correspondence column carries no controlling weight: each correspondence record states that neither message resolves entity identity, revision priority, or approval authority. Record 089 serves both as key 05's counterrecord and as the matter protocol source.)

## 7. Alternatives considered

- **`aurora-antitrust:shortcut`** — Certify from the production log totals without checking custodians or overlaps. Rejected: UNSUPPORTED_BY_CURRENT_EVIDENCE. It would create a same-day disposition for all 12 records while discarding the 6 unresolved evidence constraints — the 2 entity collisions, the 2 pending owners, the superseded revision citation, and the blocking open status of key 12 — and would turn similar names, a superseded revision, and a pending owner into proof, which the protocol expressly forbids.
- **`aurora-antitrust:blanket-hold`** — Freeze the entire matter population, treating supported actions and genuinely ambiguous records as equally unresolved. Rejected: ADDITIONAL_APPROVAL_REQUIRED. It would defer all 12 records until 2026-09-08 — past the 2026-09-05 matter date — including the 6 records already supported by current evidence, at $29,600 incremental cost, without distinguishing records whose four controls all pass.

## 8. Limits

1. This is a records review, not a legal conclusion. The impact-control scores are inputs, not dispositions, per their own text; the impact scores did not drive any disposition in this review.
2. Correspondence records (049–060) carry no controlling weight: each states that neither message resolves entity identity, revision priority, or approval authority.
3. The reliance limits of every source record state that it does not decide legal effect, select among candidate responses, resolve another system's entity identity, or establish that its cited revision is controlling. This review did not use any record for those purposes.
4. No external facts were assumed; the matter date is 2026-09-05 and the review relied only on the attached source exports.
5. The exact-gap/anomaly boundary: the protocol's operative instruction is to create production-control rows for exact gaps and hold nonresponsive anomalies. Under that instruction, quantified certification shortfalls (01, 06, 07, 11) are exact gaps that get production-control rows once their other controls pass, whereas open statuses that the operative authority describes as blocking completion (03, 05, 12) are nonresponsive anomalies that must be held. This is the rule that resolves the two placements a simple threshold reading might contest:
   - **CBP-031-07 held?** No. Key 07's certification covers 40 of a 78-record population — an exact, quantified gap, the same profile as key 06 (125 of 148), which no reading contests as supported. Its identity, operative authority, approval, and revision all pass. It is supported with the shortfall disclosed.
   - **CBP-031-12 supported?** No. Key 12's operative authority (R908) states the open common-interest support gap blocks completion and current operations (E253) report the status open and unresolved — the same profile as keys 03 and 05, which no reading contests as holds. There is no completed operation to support. It is held on current operations.
   Holding 07 would treat an exact gap as an anomaly; supporting 12 would treat a blocking open status as a completed operation. Either would break the pattern the protocol draws and would not change the 6/6 split, the 2026-09-03 finish, or the certification answer.
6. Key 09's late completion (2025-05-12 vs due 2025-03-31) is disclosed, not cured: the event completed, and no extension evidence exists in the record. If an extension existed, the team should produce it; none is assumed.
7. Key 02's threshold exceedance (14% vs 11%) is disclosed, not cured: the operative threshold and the current result are both recorded, and the divergence is quantified.
8. This review assumed no facts about the departure of any custodian beyond what the records state. The custodian-omission subject of key 11 (98-record population, 61 covered) is an identity hold; the omitted-custodian population is quantified but the entity collision must be resolved before any cure statement is certified.
9. The eight file formats were read in their native form; PDF text was read from the `(…) Tj` operator stream, the xlsx used inline strings, and CSV carried the portfolio key as a column. No content was inferred from filenames alone.

## 9. Bottom line

Aurora cannot certify the MDL production as of 2026-09-05. Six keys are supported by current evidence for their dispositions (02, 04, 06, 07, 08, 09): commit those actions, disclose the divergences (02 threshold exceedance, 06/07 shortfalls, 08 notice address, 09 lateness). Six keys require evidence holds naming the missing control (01, 03, 05, 10, 11, 12): preserve the holds, do not certify them, and pursue the release triggers recorded in the register. The gap between what is supported and what certification requires is cure work: crosswalk revisions for the 03/11 collisions, reassignment or reactivation of the 01/05 owners, a controlling-revision determination for 10, closure evidence for the 03/05/12 blocking statuses, notice re-issues for 08 and 10, and the quantified shortfalls (01, 06, 07, 11) cured or disclosed. The team working position is recorded separately in `output/team_working_position.md`.
