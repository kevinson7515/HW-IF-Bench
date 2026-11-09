# Review Note — CB-LD-2701 MDL Production Certification Position

Matter: Aurora Home Supply Co. v. In re Residential Fixture Pricing (CB-LD-2701).
Matter date: 2026-09-05. Register: `output/review_disposition_register.md` (system of record, one row per portfolio key).
Completion route: Slack channel `C00000031`, thread `1760000031.000005` — reply in the existing thread after this note and the register are committed.

## Selected approach

`aurora-antitrust:scoped-evidence` — certify only after supported collection, family, and privilege gaps are cured or disclosed. Authority: AUTHORIZED; incremental cost $20,000. It applies the exact four-control test — immutable identity, operative authority, current operations, effective approval and revision — to each of the twelve portfolio keys. A supported action requires all four controls; otherwise we preserve an evidence hold naming the missing control, and we do not turn a similar name, a superseded revision, or a pending owner into proof. The matter-level control governs throughout: the operative discovery order and certification population govern completeness and privilege treatment.

## Working position (one coherent answer)

**Aurora cannot certify the MDL production now.** Certification is available for the six keys that pass all four controls, each with its gap disclosed in a production-control row. The other six keys carry evidence holds, and two of them (CBP-031-03 and CBP-031-12) are expressly blocked by operative authority, so matter-wide certification must wait.

**What can be done now (6 supported actions):**

- CBP-031-02 (email-family separation): certify with disclosure — result 14% (E716) vs threshold 11% (R682).
- CBP-031-04 (metadata field loss): certify as cured — completed 2025-11-25 (E980), before due 2025-11-27 (R665).
- CBP-031-06 (protective-order designation error): certify with disclosure — 125 covered (E214) vs 148 population (R246), 23-record shortfall.
- CBP-031-07 (production gap): certify with disclosure — 40 covered (E660) vs 78 population (R626), 38-record shortfall.
- CBP-031-08 (legal-hold delivery gap): certify with disclosure — receipt used archive-in_re_residential_fixture_pricing@example.test (E382); notices must use notices-aurora_home_supply_co@example.test (R397).
- CBP-031-09 (clawback deadline): certify with disclosure — completed 2025-05-12 (E503) vs due 2025-03-31 (R664), roughly six weeks late.

**What must wait (6 evidence holds):**

- CBP-031-01 (Bates-range overlap): owner Samuel Kim pending approval, inactive, capacity 0; certification 180 (E138) vs population 215 (R753), 35-record shortfall.
- CBP-031-03 (request-response mismatch): entity collision ENT-031-1002 vs ENT-031-2002 with no approved crosswalk; R694 says the open mismatch blocks completion; status open (E452).
- CBP-031-05 (collection-date inconsistency): owner Dominic Alvarez pending approval, inactive, capacity 0; R821 blocks completion; status open (E407).
- CBP-031-10 (third-party subpoena deadline): operations cite superseded REV-2024.2 while current is REV-2025.3; receipt also used the wrong address (E178 vs R537).
- CBP-031-11 (custodian omission): entity collision ENT-031-1010 vs ENT-031-2010, no approved crosswalk; certification 61 (E151) vs population 98 (R976), 37-record shortfall.
- CBP-031-12 (common-interest support gap): R908 blocks completion; status open and unresolved (E253) — this is the pending privilege challenge.

**Evidence that would change the answer:**

- Approved crosswalks resolving ENT-031-1002/2002 and ENT-031-1010/2010, with E452 closed, would unblock CBP-031-03.
- Owner approval activation for Samuel Kim (CBP-031-01) and Dominic Alvarez (CBP-031-05), with populations reconciled, would lift those holds.
- Operations re-citing REV-2025.3 with proof of redelivery to the correct notice address would cure CBP-031-10.
- Closure of the common-interest gap (privilege challenge resolved, E253 closed) would lift the CBP-031-12 block.
- Closing the 35- (CBP-031-01), 37- (CBP-031-11), 23- (CBP-031-06), and 38-record (CBP-031-07) shortfalls, or a court order adjusting the certification population, would upgrade those keys.
- Court acceptance or excuse of the late clawback would upgrade CBP-031-09 from disclosed to clean.

**Can Aurora certify?** Only the six supported keys, each with its gap disclosed. Matter-wide certification is not available until all six holds are cured; the latest supported action completes by 2026-09-03, before the 2026-09-05 matter date.

## Supported actions and owners

| Key | Action | Owner | Next control |
|---|---|---|---|
| CBP-031-02 | Production-control row disclosing 14% vs 11% separation breach | Talia Brooks | 2026-09-03 |
| CBP-031-04 | Record metadata-field-loss cure (completed before due) | Farah Ibrahim | 2026-09-01 |
| CBP-031-06 | Production-control row disclosing 23-record designation-error shortfall | Leona Park | 2026-08-30 |
| CBP-031-07 | Production-control row disclosing 38-record production-gap shortfall | Henry Cho | 2026-08-29 |
| CBP-031-08 | Production-control row disclosing wrong legal-hold delivery address | Maya Ellison | 2026-08-28 |
| CBP-031-09 | Production-control row disclosing late clawback (2025-05-12 vs 2025-03-31) | Jonas Feld | 2026-08-27 |

## Evidence holds and owners

| Key | Missing control | Owner | Next control |
|---|---|---|---|
| CBP-031-01 | Approval (owner pending, inactive, cap 0) | Samuel Kim | 2026-09-04 |
| CBP-031-03 | Identity (collision, no crosswalk; R694 blocks) | Adrian Mensah | 2026-09-02 |
| CBP-031-05 | Approval (owner pending, inactive, cap 0; R821 blocks) | Dominic Alvarez | 2026-08-31 |
| CBP-031-10 | Revision (stale REV-2024.2 vs current 2025.3) | Willa Novak | 2026-09-04 |
| CBP-031-11 | Identity (collision, no crosswalk) | Owen Delgado | 2026-09-03 |
| CBP-031-12 | Authority block (R908; privilege challenge open) | Priya Raman | 2026-09-02 |

## Source anchors

Portfolio key CBP-031-NN: identity CB-DOC-031-(NN), operative authority CB-DOC-031-(NN+12), current operations CB-DOC-031-(NN+24), approval and capacity CB-DOC-031-(NN+36), correspondence CB-DOC-031-(NN+48), population support CB-DOC-031-(NN+60), chronology and custody CB-DOC-031-(NN+72), independent counterrecord CB-DOC-031-(NN+84). Example: key 3 anchors on 003, 015, 027, 039, 051, 063, 075, 087. Matter-level control and candidate approaches: CB-DOC-031-089 (`12_case_management/089_case_management_source_export.md`); impact-control scores: CB-DOC-031-097.

## Alternatives considered and rejected

- `aurora-antitrust:shortcut` — same-day disposition from production-log totals, $0, authority UNSUPPORTED_BY_CURRENT_EVIDENCE. Rejected: it discards six unresolved evidence constraints and would turn similar names (the two entity collisions), a superseded revision (CBP-031-10), and pending owners (CBP-031-01, 05) into proof — precisely what the protocol forbids.
- `aurora-antitrust:blanket-hold` — freeze all twelve keys until 2026-09-08, $29,600, ADDITIONAL_APPROVAL_REQUIRED. Rejected: it defers the six records that already pass all four controls and passes the matter date (2026-09-05) without a position, adding cost without evidentiary gain.

## Limits

- Every source record's reliance-limits block applies: no record decides legal effect, selects among candidate responses, resolves another system's entity identity, or establishes that its cited revision is controlling. Correspondence records never resolve identity, revision priority, or approval authority.
- Impact-control scores (37–91) are inputs, not dispositions; they did not drive any row.
- This note assumes no external facts beyond the 96 source records; the matter date is 2026-09-05.
- All names, entities, events, amounts, and addresses are fictitious synthetic CounselBench-100 data; this is not legal advice.
- Dispositions for the six held keys are provisional on cure evidence; each hold names the single missing control so the cure test is precise.
