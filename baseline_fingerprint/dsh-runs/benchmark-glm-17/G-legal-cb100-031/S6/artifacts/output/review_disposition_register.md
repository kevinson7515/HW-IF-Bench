# Review Disposition Register — Aurora Pricing MDL Discovery Audit (CB-LD-2701)

Matter: In re Residential Fixture Pricing, multidistrict antitrust production — client Aurora Home Supply Co.
Matter date: 2026-09-05. Selected approach: `aurora-antitrust:scoped-evidence` (authorized; $20,000 incremental cost).
Register date: 2026-09-05. This register is the system of record: one row per portfolio key, twelve rows total.

Four-control test per key (approach definition, 12_case_management/089): (1) immutable identity, (2) operative authority, (3) current operations, (4) effective approval/revision. A supported action requires all four controls. Otherwise an evidence hold is preserved and the missing control is stated. The source-anchor cell lists, in role order: identity crosswalk, operative authority, current operations, approval and capacity, correspondence, financial/population support (impact score), chronology and custody, independent counterrecord.

| Key | Subject | Entity | C1 Identity | C2 Operative authority | C3 Current operations | C4 Approval/revision | Owner (status / capacity / next control date) | Impact | Disposition | Missing control (holds only) | Source anchors |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | ENT-031-1000 | Pass — REV-2025.1 crosswalk, domain/legal/native key agree, nearby alias excluded | R753: population 215 (rev. REV-2025.1) | E138: certification covers 180 — shortfall 35 | Fail — Samuel Kim pending/inactive, capacity 0 | Samuel Kim (pending approval, inactive / 0 / 2026-09-04) | 37 (input, not a disposition) | Evidence hold | Effective approval — owner pending approval and inactive, capacity 0; quantified shortfall 180 of 215 cured or disclosed | 001 md; 013 json; 025 md; 037 json; 049 md; 061 json; 073 md; 085 json |
| CBP-031-02 | Email-family separation | ENT-031-1001 | Pass — clean crosswalk | R682: threshold 11% (rev. REV-2025.2) | E716: result 14% — exceeds threshold by 3 points | Pass — Talia Brooks active, capacity 1 | Talia Brooks (active / 1 / 2026-09-03) | 89 (input, not a disposition) | Supported action, disclose threshold exceedance (14% vs 11%) | — | 002 txt; 014 xml; 026 txt; 038 xml; 050 txt; 062 xml; 074 txt; 086 xml |
| CBP-031-03 | Request-response mismatch | ENT-031-1002 vs ENT-031-2002 | Fail — entity collision, no approved crosswalk revision resolves it | R694: open mismatch blocks completion (rev. REV-2025.3) | E452: status open and unresolved | Pass — Adrian Mensah active, capacity 4 | Adrian Mensah (active / 4 / 2026-09-02) | 91 (input, not a disposition) | Evidence hold | Immutable identity — ENT-031-1002/ENT-031-2002 collision unresolved; operative authority states blocks completion; current operations open and unresolved | 003 eml; 015 html; 027 eml; 039 html; 051 eml; 063 html; 075 eml; 087 html |
| CBP-031-04 | Metadata field loss | ENT-031-1003 | Pass — clean crosswalk | R665: due 2025-11-27 (rev. REV-2025.4) | E980: completed 2025-11-25 — timely | Pass — Farah Ibrahim active, capacity 4 | Farah Ibrahim (active / 4 / 2026-09-01) | 45 (input, not a disposition) | Supported action, no defect | — | 004 csv; 016 pdf; 028 csv; 040 pdf; 052 csv; 064 pdf; 076 csv; 088 pdf |
| CBP-031-05 | Collection-date inconsistency | ENT-031-1004 | Pass — clean crosswalk | R821: open inconsistency blocks completion (rev. REV-2025.5) | E407: status open and unresolved | Fail — Dominic Alvarez pending/inactive, capacity 0 | Dominic Alvarez (pending approval, inactive / 0 / 2026-08-31) | 70 (input, not a disposition) | Evidence hold | Effective approval — owner pending approval and inactive, capacity 0; operative authority states blocks completion; current operations open and unresolved | 005 json; 017 md; 029 json; 041 md; 053 json; 065 md; 077 json; 089 md |
| CBP-031-06 | Protective-order designation error | ENT-031-1005 | Pass — clean crosswalk | R246: population 148 (rev. REV-2025.6) | E214: certification covers 125 — shortfall 23 | Pass — Leona Park active, capacity 6 | Leona Park (active / 6 / 2026-08-30) | 82 (input, not a disposition) | Supported action, disclose shortfall 125 of 148 | — | 006 xml; 018 txt; 030 xml; 042 txt; 054 xml; 066 txt; 078 xml; 090 txt |
| CBP-031-07 | Production gap | ENT-031-1006 | Pass — clean crosswalk | R626: population 78 (rev. REV-2025.7) | E660: certification covers 40 — shortfall 38 | Pass — Henry Cho active, capacity 6 | Henry Cho (active / 6 / 2026-08-29) | 58 (input, not a disposition) | Supported action, disclose shortfall 40 of 78 | — | 007 html; 019 eml; 031 html; 043 eml; 055 html; 067 eml; 079 html; 091 eml |
| CBP-031-08 | Legal-hold delivery gap | ENT-031-1007 | Pass — clean crosswalk | R397: notices must use notices-aurora_home_supply_co@example.test (rev. REV-2025.1) | E382: receipt used archive-in_re_residential_fixture_pricing@example.test — noncompliant address | Pass — Maya Ellison active, capacity 1 | Maya Ellison (active / 1 / 2026-08-28) | 57 (input, not a disposition) | Supported action, re-issue notice to the required address | — | 008 pdf; 020 csv; 032 pdf; 044 csv; 056 pdf; 068 csv; 080 pdf; 092 csv |
| CBP-031-09 | Clawback deadline | ENT-031-1008 | Pass — clean crosswalk | R664: due 2025-03-31 (rev. REV-2025.2) | E503: event completed 2025-05-12 — late by 42 days, no extension evidence | Pass — Jonas Feld active, capacity 1 | Jonas Feld (active / 1 / 2026-08-27) | 61 (input, not a disposition) | Supported action, disclose late completion (2025-05-12 vs due 2025-03-31) | — | 009 md; 021 json; 033 md; 045 json; 057 md; 069 json; 081 md; 093 json |
| CBP-031-10 | Third-party subpoena deadline | ENT-031-1009 | Pass — clean crosswalk | R537: notices must use notices-aurora_home_supply_co@example.test; R537 record states REV-2025.3 is the later effective revision | E178: receipt used archive-in_re_residential_fixture_pricing@example.test — noncompliant address; operating extract cites REV-2024.2 | Fail — operations cite superseded REV-2024.2 against controlling REV-2025.3 | Willa Novak (active / 4 / 2026-09-04) | 33 (input, not a disposition) | Evidence hold | Effective revision — operations cite superseded REV-2024.2 against controlling REV-2025.3; notice re-issue to required address also pending | 010 txt; 022 xml; 034 txt; 046 xml; 058 txt; 070 xml; 082 txt; 094 xml |
| CBP-031-11 | Custodian omission | ENT-031-1010 vs ENT-031-2010 | Fail — entity collision, no approved crosswalk revision resolves it | R976: population 98 (rev. REV-2025.4) | E151: certification covers 61 — shortfall 37 | Pass — Owen Delgado active, capacity 3 | Owen Delgado (active / 3 / 2026-09-03) | 55 (input, not a disposition) | Evidence hold | Immutable identity — ENT-031-1010/ENT-031-2010 collision unresolved; quantified shortfall 61 of 98 cured or disclosed | 011 eml; 023 html; 035 eml; 047 html; 059 eml; 071 html; 083 eml; 095 html |
| CBP-031-12 | Common-interest support gap | ENT-031-1011 | Pass — REV-2025.5 crosswalk, domain/legal/native key agree, nearby alias excluded | R908: open common-interest support gap blocks completion (rev. REV-2025.5) | E253: status open and unresolved | Pass — Priya Raman active, capacity 1 | Priya Raman (active / 1 / 2026-09-02) | 85 (input, not a disposition) | Evidence hold | Current operations — status open and unresolved; operative authority states blocks completion | 012 csv; 024 pdf; 036 csv; 048 pdf; 060 csv; 072 pdf; 084 csv; 096 pdf |

Hold count: 6. Supported count: 6. Latest supported action finishes by 2026-09-03 (CBP-031-02, next internal control date 2026-09-03).

## Sequencing of the six supported actions (all before the 2026-09-05 matter date)

| Order | Key | Next internal control date | Owner |
|---|---|---|---|
| 1 | CBP-031-09 | 2026-08-27 | Jonas Feld |
| 2 | CBP-031-08 | 2026-08-28 | Maya Ellison |
| 3 | CBP-031-07 | 2026-08-29 | Henry Cho |
| 4 | CBP-031-06 | 2026-08-30 | Leona Park |
| 5 | CBP-031-04 | 2026-09-01 | Farah Ibrahim |
| 6 | CBP-031-02 | 2026-09-03 | Talia Brooks |

## Cure requirements (holds only)

| Hold key | Cure before certification |
|---|---|
| CBP-031-01 | Reassign ownership from Samuel Kim (pending/inactive/0), then cure or disclose the 180-of-215 shortfall; obtain effective approval |
| CBP-031-03 | Approved crosswalk revision resolving ENT-031-1002/2002 collision; closure evidence for the open/unresolved request-response mismatch status |
| CBP-031-05 | Reassign ownership from Dominic Alvarez (pending/inactive/0); closure evidence for open/unresolved status; obtain effective approval |
| CBP-031-10 | Controlling-revision determination reconciling REV-2024.2 citations to REV-2025.3; re-issue notice to notices-aurora_home_supply_co@example.test |
| CBP-031-11 | Approved crosswalk revision resolving ENT-031-1010/2010 collision; cure or disclose the 61-of-98 shortfall |
| CBP-031-12 | Closure evidence for open/unresolved common-interest support gap status |

## Hold release triggers

| Hold key | Release trigger |
|---|---|
| CBP-031-01 | Owner approval reactivating Samuel Kim or an approved reassignment to an active owner with capacity; alternatively a revised operative order changing the certification population (215) for Bates-range overlap |
| CBP-031-03 | An approved crosswalk revision resolving the ENT-031-1002/ENT-031-2002 collision |
| CBP-031-05 | Owner approval reactivating Dominic Alvarez or an approved reassignment to an active owner with capacity |
| CBP-031-10 | A controlling-revision determination for REV-2024.2 vs REV-2025.3 |
| CBP-031-11 | An approved crosswalk revision resolving the ENT-031-1010/ENT-031-2010 collision |
| CBP-031-12 | Closure evidence showing the common-interest support gap status is closed |

Provenance: synthetic CounselBench-100 matter; all people, entities, amounts, and addresses are fictitious; not legal advice. Reviewer relied only on the attached source exports; no external facts assumed. Every entity, reference, figure, and date in this register was re-read in the cited source file before recording.
