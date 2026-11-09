# Review Note — CB-LD-2701 Aurora pricing MDL discovery audit

Matter: CB-LD-2701 — Aurora pricing MDL discovery audit
Population: `cb100-031-aurora-antitrust`, 12 portfolio keys (CBP-031-01 through CBP-031-12)
Matter date: 2026-09-05
Companion file: `output/review_disposition_register.md` (system of record, one row per portfolio key)

This note is the human-readable record required by the matter work-product protocol
(CB-DOC-031-089, lines 80–101). It records the selected approach, the supported actions, the
evidence holds, source anchors, the alternatives considered, and the limits of the review.

## 1. Selected approach

**`aurora-antitrust:scoped-evidence`** — Authority: AUTHORIZED.

Under this approach, certification is available only for the supported subset, after supported
collection, family, and privilege gaps are cured or disclosed. The protocol's outcome for this
approach is: commit 6 supported actions, preserve 6 evidence holds, and finish the latest
supported action by 2026-09-03. Incremental cost: $20,000. No external facts were assumed.

## 2. Supported actions (6) — what can be done now

These keys meet all four controls and support immediate action, with the recorded gap disclosed
rather than concealed. The latest completion date is 2026-09-03, ahead of the 2026-09-05 matter
date.

| Key | Issue | Action and disclosure |
|---|---|---|
| CBP-031-02 | Email-family separation | Proceed; disclose that the operating result is 14% (E716) against the operative 11% threshold (R682) — a 3-point exceedance. Owner Talia Brooks (active). |
| CBP-031-04 | Metadata field loss | Proceed; event completed 2025-11-25 (E980), before the 2025-11-27 due date (R665). Record as cured. Owner Farah Ibrahim (active). |
| CBP-031-06 | Protective-order designation error | Proceed; disclose the 125-record certification (E214) against the 148-record population (R246) — 23 records. Owner Leona Park (active). |
| CBP-031-07 | Production gap | Proceed; disclose the 40-record certification (E660) against the 78-record population (R626) — 38 records. Owner Henry Cho (active). |
| CBP-031-08 | Legal-hold delivery gap | Proceed; disclose that the hold receipt used the archive address (E382) where the operative order requires `notices-aurora_home_supply_co@example.test` (R397); re-issue to the required address. Owner Maya Ellison (active). |
| CBP-031-09 | Clawback deadline | Proceed; disclose that the clawback completed 2025-05-12 (E503) against the 2025-03-31 deadline (R664) — 42 days late. Owner Jonas Feld (active). |

## 3. Evidence holds (6) — what must wait

These keys fail the four-control test. Each hold preserves the evidence and names the missing
control. No disposition may be certified for these keys until the named condition is cured.

| Key | Issue | Missing control | Cure condition |
|---|---|---|---|
| CBP-031-01 | Bates-range overlap | Effective approval | Roster owner Samuel Kim is pending approval and inactive, capacity 0 (rec 037); next internal control date 2026-09-04. Also reconcile the 180-record certification (E138) against the 215-record population (R753). |
| CBP-031-03 | Request-response mismatch | Immutable identity | Portfolio key maps to both ENT-031-1002 and ENT-031-2002; domain and legal-entity fields disagree; no approved crosswalk revision resolves the collision. Operative authority adds that the open mismatch blocks completion (R694). |
| CBP-031-05 | Collection-date inconsistency | Effective approval | Roster owner Dominic Alvarez is pending approval and inactive, capacity 0 (rec 041); next internal control date 2026-08-31. Operative authority adds that the open inconsistency blocks completion (R821). |
| CBP-031-11 | Custodian omission | Immutable identity | Portfolio key maps to both ENT-031-1010 and ENT-031-2010; domain and legal-entity fields disagree; no approved crosswalk revision resolves the collision. Scope is 61 records certified (E151) vs 98 in population (R976). |
| CBP-031-10 | Third-party subpoena deadline | Effective revision | The operating extract cites superseded REV-2024.2 (E178) where REV-2025.3 is the later effective revision. Receipt also used the archive address rather than the required notices address (R537). |
| CBP-031-12 | Common-interest support gap | Operative authority | The open common-interest support gap blocks completion under R908; the pending privilege challenge cannot be resolved on the current record. |

## 4. Source anchors

Primary anchors per key (all from the `cb100-031-aurora-antitrust` source corpus at
`attached_files/task_10/`):

- Identity crosswalk: CB-DOC-031-001 through 012 (folder `01_pleadings`)
- Operative authority: CB-DOC-031-013 through 024 (folders `02_orders`, `03_requests_responses`)
- Current operations: CB-DOC-031-025 through 036 (folders `04_custodian_files`, `05_email_families`, `06_chat_exports`)
- Approval and capacity: CB-DOC-031-037 through 048 (folders `05_email_families`, `06_chat_exports`)
- Correspondence: CB-DOC-031-049 through 060 (folder `07_correspondence_log`)
- Financial or population support: CB-DOC-031-061 through 072 (folder `08_financial_records`)
- Chronology and custody: CB-DOC-031-073 through 084 (folder `09_custody_chains`)
- Independent counterrecord: CB-DOC-031-085 through 096 (folders `10_third_party_logs`, `11_debates`, `12_case_management`)
- Impact-control scores: `12_case_management/097_aurora_antitrust_impact_population.xlsx` (12 rows; all labeled "retained source population; not a legal disposition")

Additional decisive anchors:

- CB-DOC-031-089 (`12_case_management/089_case_management_source_export.md`), lines 80–101: matter work-product protocol, candidate approaches, register and note requirements, completion route.
- CB-DOC-031-061 (financial support role): the impact-control score is an input, not a disposition.

## 5. Alternatives considered

| Approach | Disposition | Why rejected |
|---|--- |--- |
| `aurora-antitrust:shortcut` | Same-day disposition for all 12 keys from production-log totals without joins; cost $0 | Authority: UNSUPPORTED_BY_CURRENT_EVIDENCE. It discards 6 unresolved constraints, including two identity collisions and an open privilege blocker, and certifies totals the source records do not support. Not defensible. |
| `aurora-antitrust:blanket-hold` | Freeze the entire population; defer all 12 keys to 2026-09-08; cost $29,600 | Authority: ADDITIONAL_APPROVAL_REQUIRED. It over-holds the 6 keys that pass all four controls, misses the 2026-09-05 position deadline (deferred past it to 2026-09-08), and costs more. |

The scoped-evidence approach is the only AUTHORIZED option and the only one that both meets the
deadline and preserves the unresolved constraints.

## 6. Limits of this review

- This is a records review of the provided corpus only. No external facts were assumed and no facts outside the corpus were relied on.
- The source records do not decide legal effect. Per the records' own reliance limits, they "do not decide legal effect, select among candidate responses, resolve another system's entity identity, or establish that its cited revision is controlling." This note and the register adopt no position on legal effect.
- The impact-control scores are prioritization inputs only; per the source population's own label they are "not a legal disposition," and per CB-DOC-031-061 a score "is an input, not a disposition." They did not determine any disposition.
- The independent counterrecords (CB-DOC-031-085 through 096) confirm raw activity but assign no legal consequence; confirmation of activity is not confirmation of compliance.
- A similar entity name is not evidence of identity. CBP-031-03 and CBP-031-11 are held precisely because a shared display name coexists with conflicting domain and legal-entity fields.
- Hold cure is not certification. Lifting a hold requires the named cure condition, then a fresh four-control pass; a cured identity collision, for example, still leaves CBP-031-03's open request-response mismatch (R694) to close.
- Population counts in this note are as recorded in the cited records; where an operations extract and an operative record disagree (e.g., 180 vs 215 for CBP-031-01), both values are recorded rather than reconciled, because the records themselves state they must be reconciled.
- This review does not opine on privilege doctrine; CBP-031-12's hold reflects that the common-interest support gap is open and blocks completion under R908, not a judgment on the privilege challenge's merits.

## 7. Reproduction

- Corpus root: `attached_files/task_10/` (96 records in 12 folders, 8 formats each, plus the XLSX population file).
- Record numbering: record N maps to portfolio key `CBP-031-((N-1) mod 12)+1` and evidence role `ROLE[(N-1)//12+1]`.
- XLSX read via openpyxl; PDF text recovered from raw zlib-inflated content streams (no PDF library was available in the sandbox).
