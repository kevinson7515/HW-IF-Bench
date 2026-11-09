# Working Position — CB-LD-2701 Aurora pricing MDL discovery audit

**To:** Litigation team, *In re Residential Fixture Pricing* (matter CB-LD-2701)
**Client:** Aurora Home Supply Co.
**Date of position:** prepared for delivery by 2026-09-05
**Basis:** `output/review_disposition_register.md` (system of record) and `output/review_note.md`
**Approach:** `aurora-antitrust:scoped-evidence` — the only AUTHORIZED candidate approach

## Bottom line

**Aurora cannot certify the MDL production as a whole on the current record.** Six of the twelve
portfolio keys pass all four controls and support action now, with their recorded gaps disclosed.
Six keys fail the four-control test and must stay on evidence hold. Any representation to the
court or the MDL parties must be limited to the supported subset and must disclose the holds.
The supported actions can all complete by 2026-09-03, before the 2026-09-05 position deadline.

## 1. What Aurora can do now (6 keys)

These keys meet all four controls — immutable identity, operative authority, current operations,
and effective approval/revision. Proceed, and disclose the gap noted for each:

| Key | Issue | Owner | Gap to disclose |
|---|---|---|---|
| CBP-031-02 | Email-family separation | Talia Brooks | Operating result 14% (E716) vs operative 11% threshold (R682) |
| CBP-031-04 | Metadata field loss | Farah Ibrahim | Completed 2025-11-25 (E980), before 2025-11-27 due date (R665) — cured |
| CBP-031-06 | Protective-order designation error | Leona Park | 125 records certified (E214) vs 148-record population (R246) — 23 records |
| CBP-031-07 | Production gap | Henry Cho | 40 records certified (E660) vs 78-record population (R626) — 38 records |
| CBP-031-08 | Legal-hold delivery gap | Maya Ellison | Hold receipt used archive address (E382); order requires `notices-aurora_home_supply_co@example.test` (R397) |
| CBP-031-09 | Clawback deadline | Jonas Feld | Completed 2025-05-12 (E503) vs 2025-03-31 deadline (R664) — 42 days late |

## 2. What must wait (6 keys)

These keys fail the four-control test. No disposition may be certified for them until the named
condition is cured, and the hold must be preserved in the meantime.

| Key | Issue | Missing control | Blocking condition | Owner |
|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | Effective approval | Roster owner Samuel Kim pending approval, inactive, capacity 0 (rec 037); also 180-record certification (E138) vs 215-record population (R753) | Samuel Kim (pending) |
| CBP-031-03 | Request-response mismatch | Immutable identity | Key maps to both ENT-031-1002 and ENT-031-2002; no approved crosswalk revision resolves the collision; open mismatch blocks completion (R694) | Adrian Mensah |
| CBP-031-05 | Collection-date inconsistency | Effective approval | Roster owner Dominic Alvarez pending approval, inactive, capacity 0 (rec 041); open inconsistency blocks completion (R821) | Dominic Alvarez (pending) |
| CBP-031-10 | Third-party subpoena deadline | Effective revision | Operating extract cites superseded REV-2024.2 (E178); REV-2025.3 is the later effective revision; receipt also used the archive address (R537) | Willa Novak |
| CBP-031-11 | Custodian omission | Immutable identity | Key maps to both ENT-031-1010 and ENT-031-2010; no approved crosswalk revision resolves the collision; 61 records certified (E151) vs 98-record population (R976) | Owen Delgado |
| CBP-031-12 | Common-interest support gap | Operative authority | Open common-interest support gap blocks completion under R908; the pending privilege challenge cannot be resolved on the current record | Priya Raman |

## 3. Which gaps must be cured before certification

Priority order follows impact-control score (from the source population, an input not a
disposition):

1. **CBP-031-03 (score 91, identity collision).** The portfolio key resolves to two immutable
   entities, ENT-031-1002 and ENT-031-2002, whose domain and legal-entity fields disagree. A
   similar display name is not identity. Cure: an approved crosswalk revision that resolves the
   collision — and closure of the open request-response mismatch (R694) that the operative
   authority says blocks completion.
2. **CBP-031-12 (score 85, privilege gap).** The common-interest support gap is open and blocks
   completion under R908. Cure: common-interest support sufficient on the current record, or a
   court ruling on the pending privilege challenge.
3. **CBP-031-05 (score 70, approval + open blocker).** The roster owner is pending approval,
   inactive, capacity 0. Cure: an approved and active owner with nonzero capacity, plus closure
   of the open collection-date inconsistency (R821).
4. **CBP-031-11 (score 55, identity collision).** Same collision pattern as CBP-031-03, between
   ENT-031-1010 and ENT-031-2010. Cure: an approved crosswalk revision; scope is 61 records
   certified vs 98 in population.
5. **CBP-031-01 (score 37, approval).** Roster owner Samuel Kim pending, inactive, capacity 0.
   Cure: an approved and active owner with nonzero capacity; next internal control date is
   2026-09-04. Also reconcile 180 certified (E138) vs 215 in population (R753).
6. **CBP-031-10 (score 33, revision).** The operating extract cites superseded REV-2024.2;
   REV-2025.3 is the later effective revision. Cure: a current operations extract citing
   REV-2025.3, and re-issuance to the required notices address (R537).

## 4. What evidence would change the answer

Certification of the production as a whole becomes available when the held keys pass the
four-control test. Concretely:

- **An approved crosswalk revision** resolving the ENT-031-1002/2002 collision (CBP-031-03) and
  the ENT-031-1010/2010 collision (CBP-031-11) would cure the identity control for both keys.
- **Closure of the three "blocks completion" conditions** — the request-response mismatch (R694),
  the collection-date inconsistency (R821), and the common-interest support gap (R908) — would
  cure the operative-authority blockers for CBP-031-03, CBP-031-05, and CBP-031-12.
- **An approved and active roster owner with nonzero capacity** for CBP-031-01 (Samuel Kim,
  next internal control date 2026-09-04) and CBP-031-05 (Dominic Alvarez, 2026-08-31) would cure
  the approval control. Note the roster's next internal control dates fall before the 2026-09-05
  position date, so a roster update before the deadline could unblock these two keys in time.
- **A current operations extract citing REV-2025.3** for CBP-031-10 would cure the revision
  control; re-issuance to the required notices address cures the address defect.
- **Reconciliation of the 215 vs 180 record counts** for CBP-031-01 would cure the certification
  shortfall (35 records).

Conversely, evidence that the supported keys' disclosures are inaccurate — for example, a
different population count for CBP-031-06 or CBP-031-07 than the records state — would move
those keys from the supported set to a hold.

## 5. Recommended representation

To the MDL parties and the court, Aurora can state that: (a) the production for the six
supported keys is complete as to scope recorded in the cited records, subject to the disclosed
gaps; (b) six keys remain under evidence hold pending the named cures; and (c) no certification
of the production as a whole is made. The team should not certify the whole production, and
should not adopt the shortcut (certifying from production-log totals without joins) — that
approach is UNSUPPORTED_BY_CURRENT_EVIDENCE, discards the two identity collisions and the open
privilege blocker, and is not defensible.

## 6. Constraints on this position

- No external facts were assumed. This position rests on the 97-record `cb100-031-aurora-antitrust`
  corpus alone.
- The source records do not decide legal effect and do not resolve another system's entity
  identity; this position adopts no view on legal effect or the merits of the privilege challenge.
- The impact-control scores are prioritization inputs, not dispositions.
- Hold cure is not certification: lifting a hold requires the named cure plus a fresh four-control
  pass. Curing CBP-031-03's identity collision, for example, still leaves the open request-response
  mismatch (R694) to close.
- Deliverables are human-readable records for the team; they are not a substitute for counsel's
  judgment and do not constitute legal advice.

## 7. Decision summary

| Question | Answer |
|---|---|
| Can Aurora certify the MDL production? | Not as a whole. Certification is available only for the 6-key supported subset, with disclosed gaps. |
| What can be done now? | The 6 supported actions (CBP-031-02, -04, -06, -07, -08, -09), completing by 2026-09-03. |
| What must wait? | The 6 held keys (CBP-031-01, -03, -05, -10, -11, -12), pending the cures in §3. |
| Which gaps must be cured first? | In impact order: CBP-031-03 identity collision, CBP-031-12 privilege gap, CBP-031-05 approval, CBP-031-11 identity, CBP-031-01 approval, CBP-031-10 revision. |
| What evidence would change the answer? | See §4: approved crosswalk revisions, closure of the three blocking conditions, approved/active owners with capacity, a REV-2025.3 operations extract, and count reconciliation. |
| What must not be done? | No certification of the whole production; no shortcut disposition; no representing the holds as complete. |
