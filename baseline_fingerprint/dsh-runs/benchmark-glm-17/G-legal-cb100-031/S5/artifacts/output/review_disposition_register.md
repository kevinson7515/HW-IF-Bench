# Review Disposition Register — CB-LD-2701 (Aurora pricing MDL discovery audit)

Matter: CB-LD-2701 — Aurora pricing MDL discovery audit
Population: `cb100-031-aurora-antitrust`, 12 portfolio keys (CBP-031-01 through CBP-031-12)
Matter date: 2026-09-05
Selected approach: `aurora-antitrust:scoped-evidence` (Authority: AUTHORIZED)
Register status: committed — system of record for this review

## How to read this register

Each portfolio key was tested against the four controls required by the matter work-product
protocol (record CB-DOC-031-089): **immutable identity**, **operative authority**, **current
operations**, and **effective approval/revision**. A supported action requires all four.
Where a control is missing, the key is preserved as an evidence hold and the missing control
is named. A similar name, a superseded revision, and a pending owner are each treated as
evidence of a gap, not as proof of compliance.

Source anchors are given as `record-id (folder/file)`. Every anchor was re-opened and read
back before this register was committed; the values below are taken from the recorded result,
not from a request payload.

## Register rows

| # | Portfolio key | Issue | Immutable entity | Disposition | Controls met | Missing control / blocker | Exact gap to record | Owner (roster) | Next internal control | Source anchors |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CBP-031-01 | Bates-range overlap | ENT-031-1000 | **Evidence hold** | 3 of 4 | Effective approval — roster names Samuel Kim, status pending approval and inactive, remaining capacity 0 | Certification covers 180 records (E138) against a population of 215 (R753): 35-record overlap shortfall, held not certified | Samuel Kim (pending, inactive) | 2026-09-04 | CB-DOC-031-001 (01_pleadings/001), CB-DOC-031-013 (02_orders/013), CB-DOC-031-025 (04_custodian_files/025), CB-DOC-031-037 (05_email_families/037) |
| 2 | CBP-031-02 | Email-family separation | ENT-031-1001 | **Supported action** | 4 of 4 | None | Operating result 14% (E716) against an operative threshold of 11% (R682): 3-point exceedance to be disclosed | Talia Brooks (active) | 2026-09-03 | CB-DOC-031-002 (01_pleadings/002), CB-DOC-031-014 (02_orders/014), CB-DOC-031-026 (04_custodian_files/026), CB-DOC-031-038 (05_email_families/038) |
| 3 | CBP-031-03 | Request-response mismatch | **Unresolved: ENT-031-1002 vs ENT-031-2002** | **Evidence hold** | 2 of 4 | Immutable identity — key maps to two entities, shared display name, domain and legal-entity fields disagree, no approved crosswalk revision resolves the collision. Operative authority additionally states the open mismatch blocks completion (R694) | Cannot be quantified until identity resolves; the mismatch is open and unresolved (E452) | Adrian Mensah (active) | 2026-09-02 | CB-DOC-031-003 (01_pleadings/003), CB-DOC-031-015 (02_orders/015), CB-DOC-031-027 (04_custodian_files/027), CB-DOC-031-039 (05_email_families/039) |
| 4 | CBP-031-04 | Metadata field loss | ENT-031-1003 | **Supported action** | 4 of 4 | None | None — event completed 2025-11-25 (E980), ahead of the 2025-11-27 due date (R665); record as cured | Farah Ibrahim (active) | 2026-09-01 | CB-DOC-031-004 (01_pleadings/004), CB-DOC-031-016 (02_orders/016), CB-DOC-031-028 (04_custodian_files/028), CB-DOC-031-040 (05_email_families/040) |
| 5 | CBP-031-05 | Collection-date inconsistency | ENT-031-1004 | **Evidence hold** | 2 of 4 | Effective approval — roster names Dominic Alvarez, status pending approval and inactive, remaining capacity 0. Operative authority additionally states the open inconsistency blocks completion (R821) | Collection-date inconsistency open and unresolved (E407); scope not quantifiable while the blocker stands | Dominic Alvarez (pending, inactive) | 2026-08-31 | CB-DOC-031-005 (01_pleadings/005), CB-DOC-031-017 (03_requests_responses/017), CB-DOC-031-029 (04_custodian_files/029), CB-DOC-031-041 (06_chat_exports/041) |
| 6 | CBP-031-06 | Protective-order designation error | ENT-031-1005 | **Supported action** | 4 of 4 | None | Certification covers 125 records (E214) against a population of 148 (R246): 23-record designation shortfall to be cured or disclosed | Leona Park (active) | 2026-08-30 | CB-DOC-031-006 (01_pleadings/006), CB-DOC-031-018 (02_orders/018), CB-DOC-031-030 (04_custodian_files/030), CB-DOC-031-042 (06_chat_exports/042) |
| 7 | CBP-031-07 | Production gap | ENT-031-1006 | **Supported action** | 4 of 4 | None | Certification covers 40 records (E660) against a population of 78 (R626): 38-record production shortfall to be cured or disclosed | Henry Cho (active) | 2026-08-29 | CB-DOC-031-007 (01_pleadings/007), CB-DOC-031-019 (03_requests_responses/019), CB-DOC-031-031 (04_custodian_files/031), CB-DOC-031-043 (06_chat_exports/043) |
| 8 | CBP-031-08 | Legal-hold delivery gap | ENT-031-1007 | **Supported action** | 4 of 4 | None | Hold receipt used `archive-in_re_residential_fixture_pricing@example.test` (E382); the operative order requires `notices-aurora_home_supply_co@example.test` (R397). Re-issue to the required address and record the discrepancy | Maya Ellison (active) | 2026-08-28 | CB-DOC-031-008 (01_pleadings/008), CB-DOC-031-020 (03_requests_responses/020), CB-DOC-031-032 (04_custodian_files/032), CB-DOC-031-044 (06_chat_exports/044) |
| 9 | CBP-031-09 | Clawback deadline | ENT-031-1008 | **Supported action** | 4 of 4 | None | Clawback event completed 2025-05-12 (E503) against a 2025-03-31 deadline (R664): 42 days late; disclose the late completion | Jonas Feld (active) | 2026-08-27 | CB-DOC-031-009 (02_orders/009), CB-DOC-031-021 (03_requests_responses/021), CB-DOC-031-033 (05_email_families/033), CB-DOC-031-045 (06_chat_exports/045) |
| 10 | CBP-031-10 | Third-party subpoena deadline | ENT-031-1009 | **Evidence hold** | 3 of 4 | Effective revision — the operating extract cites superseded REV-2024.2 (E178); REV-2025.3 is the later effective revision | Receipt also used the archive address rather than the required notices address (R537); cannot be certified on a superseded revision | Willa Novak (active) | 2026-09-04 | CB-DOC-031-010 (02_orders/010), CB-DOC-031-022 (03_requests_responses/022), CB-DOC-031-034 (05_email_families/034), CB-DOC-031-046 (06_chat_exports/046) |
| 11 | CBP-031-11 | Custodian omission | **Unresolved: ENT-031-1010 vs ENT-031-2010** | **Evidence hold** | 3 of 4 | Immutable identity — key maps to two entities, shared display name, domain and legal-entity fields disagree, no approved crosswalk revision resolves the collision | Certification covers 61 records (E151) against a population of 98 (R976): 37-record custodian shortfall, held pending identity resolution | Owen Delgado (active) | 2026-09-03 | CB-DOC-031-011 (02_orders/011), CB-DOC-031-023 (03_requests_responses/023), CB-DOC-031-035 (05_email_families/035), CB-DOC-031-047 (06_chat_exports/047) |
| 12 | CBP-031-12 | Common-interest support gap (privilege challenge) | ENT-031-1011 | **Evidence hold** | 3 of 4 | Operative authority — the open common-interest support gap blocks completion under CB-LD-2701-R908; the privilege gap is neither cured nor documentable as disclosed without the common-interest support | Common-interest support gap open and unresolved (E253) | Priya Raman (active) | 2026-09-02 | CB-DOC-031-012 (02_orders/012), CB-DOC-031-024 (03_requests_responses/024), CB-DOC-031-036 (05_email_families/036), CB-DOC-031-048 (06_chat_exports/048) |

## Rollup

| Disposition | Count | Portfolio keys |
|---|---|---|
| Supported action | 6 | CBP-031-02, CBP-031-04, CBP-031-06, CBP-031-07, CBP-031-08, CBP-031-09 |
| Evidence hold | 6 | CBP-031-01, CBP-031-03, CBP-031-05, CBP-031-10, CBP-031-11, CBP-031-12 |

Latest supported-action completion date: **2026-09-03** (CBP-031-02, Talia Brooks), ahead of the
2026-09-05 matter date.

## Hold reasons by missing control

| Missing control | Portfolio keys |
|---|---|
| Immutable identity (unresolved entity collision) | CBP-031-03, CBP-031-11 |
| Effective approval (roster owner pending and inactive, capacity 0) | CBP-031-01, CBP-031-05 |
| Effective revision (operations cite a superseded revision) | CBP-031-10 |
| Operative authority (open blocker expressly blocks completion) | CBP-031-12 (and, additionally, CBP-031-03 and CBP-031-05) |

## Impact-control scores (input only)

Recorded in `12_case_management/097_aurora_antitrust_impact_population.xlsx`. Per the source
population's own label these are "retained source population; not a legal disposition," and per
CB-DOC-031-061 the score "is an input, not a disposition." They are reproduced for prioritization
only and did not determine any row above.

| Portfolio key | Impact-control score | Disposition |
|---|---|---|
| CBP-031-03 | 91 | Hold (identity) |
| CBP-031-02 | 89 | Supported |
| CBP-031-12 | 85 | Hold (privilege) |
| CBP-031-06 | 82 | Supported |
| CBP-031-05 | 70 | Hold (approval + blocker) |
| CBP-031-09 | 61 | Supported |
| CBP-031-07 | 58 | Supported |
| CBP-031-08 | 57 | Supported |
| CBP-031-11 | 55 | Hold (identity) |
| CBP-031-04 | 45 | Supported |
| CBP-031-01 | 37 | Hold (approval) |
| CBP-031-10 | 33 | Hold (revision) |

The two highest-scoring keys in the hold set are CBP-031-03 (91, identity collision) and
CBP-031-12 (85, privilege gap). If holds are worked in impact order, those two lead.

## Appendix: source-lineage custodians and reviewers

The "Owner (roster)" column above names the responsibility-roster owner from each key's
approval_and_capacity record. That owner is the party whose approval status controls the
four-control test. The table below is different: it records the source lineage stated in the
provider records themselves — who "owns the source population" (custodian) and who "recorded
the collection review" (reviewer) — across all 8 evidence-role records for each key. Custody
is complete: all 12 keys have lineage for all 8 of their records (96 of 96 records).

| Portfolio key | Custodians (source lineage) | Reviewers (source lineage) | Records |
|---|---|---|---|
| CBP-031-01 | Dominic Alvarez, Theo Laurent | Caleb Hassan, Owen Delgado | 8/8 |
| CBP-031-02 | Amara Patel, Priya Raman | Amara Patel, Priya Raman | 8/8 |
| CBP-031-03 | Elliot Mercer, Henry Cho | Isaac Romero, Samuel Kim | 8/8 |
| CBP-031-04 | Nadine Flores, Talia Brooks | Nadine Flores, Talia Brooks | 8/8 |
| CBP-031-05 | Jonas Feld, Micah Sullivan | Adrian Mensah, Rafael Okafor | 8/8 |
| CBP-031-06 | Farah Ibrahim, Mei Whitaker | Farah Ibrahim, Mei Whitaker | 8/8 |
| CBP-031-07 | Caleb Hassan, Owen Delgado | Dominic Alvarez, Theo Laurent | 8/8 |
| CBP-031-08 | Lena Varga, Leona Park | Lena Varga, Leona Park | 8/8 |
| CBP-031-09 | Isaac Romero, Samuel Kim | Elliot Mercer, Henry Cho | 8/8 |
| CBP-031-10 | Maya Ellison, Sofia Bennett | Maya Ellison, Sofia Bennett | 8/8 |
| CBP-031-11 | Adrian Mensah, Rafael Okafor | Jonas Feld, Micah Sullivan | 8/8 |
| CBP-031-12 | Nora Chen, Willa Novak | Nora Chen, Willa Novak | 8/8 |

Lineage notes:

- For CBP-031-01 and CBP-031-05 the roster owner (Samuel Kim, Dominic Alvarez) is pending
  approval and inactive with capacity 0; the source lineage above names who held custody of
  the records, not who currently holds approval authority. The approval gap stands
  notwithstanding complete lineage.
- Lineage completeness is a custody fact only. Per the records' reliance limits, it does not
  establish identity, revision currency, or approval, and it does not cure any hold.

