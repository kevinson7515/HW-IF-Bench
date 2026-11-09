# Aurora MDL Production — Working Position

**Matter:** CB-LD-2701 · Aurora pricing MDL discovery audit
**Client:** Aurora Home Supply Co.
**Counterparty:** In re Residential Fixture Pricing
**Position due to team:** 2026-09-05
**Prepared from:** 96 source records (12 defect populations × 8 evidence roles) plus the impact-population workbook (`097_aurora_antitrust_impact_population.xlsx`)

---

## 1. Bottom line

**Aurora cannot certify the MDL production on the current record.** Eleven of twelve defect populations fail their operative requirement. One population (CBP-031-04, metadata field loss) is compliant on its face. Certification of the production as a whole is blocked until the populations below are cured or resolved by the court.

The controlling measure is the matter-level control in the record set: the operative discovery order and certification population govern completeness and privilege treatment. Under that measure:

- **133 records** sit inside operative populations but outside the certified populations (CBP-031-01: 35; CBP-031-06: 23; CBP-031-07: 38; CBP-031-11: 37).
- **Three populations carry operative "blocks completion" language** (CBP-031-03 request-response mismatch under R694; CBP-031-05 collection-date inconsistency under R821; CBP-031-12 common-interest support gap under R908).
- **Two populations have unresolved entity-identity collisions** with no approved crosswalk revision (CBP-031-03, CBP-031-11).
- **Two populations delivered notices to the wrong channel** (CBP-031-08, CBP-031-10), and one of those also relies on a superseded revision.
- **One population completed late** (CBP-031-09, clawback: 42 days past the operative deadline) — a historical fact that cannot be cured retroactively, only disclosed or excused.
- **The two owners of record at the center of the question — Samuel Kim (CBP-031-01) and Dominic Alvarez (CBP-031-05) — are pending approval, inactive, and have zero remaining matter capacity.** No one with functional authority is currently driving the two populations the client asked about first.

Every correspondence record shows the counterparty already citing the operative R-reference against the client's E-reference position. These gaps are noticed; none can be cured quietly.

### The representation the team can make now

> Aurora cannot certify the production today. Certification is withheld pending cure of quantified, record-supported gaps. The gaps, their operative measures, and their owners are identified; the cures are defined and mostly within Aurora's control.

That is a defensible position. Representing completion — or certifying with current populations — is not.

---

## 2. What can be done now vs. what must wait

### Can proceed now (this week, before 2026-09-05)

1. **Record the position and the gap register.** This memo and the companion reconciliation file (`output/aurora_mdl_reconciliation.json`) do that. Owners, holds, and operative measures are recorded in the workspace.
2. **Escalate the two dead ownership lines.** Samuel Kim (CBP-031-01) and Dominic Alvarez (CBP-031-05) are pending approval, inactive, capacity 0. Both populations need a functioning owner before any cure work proceeds. Active owners with capacity exist on the roster (Leona Park 6, Henry Cho 6, Adrian Mensah 4, Farah Ibrahim 4, Willa Novak 4) and are candidates to absorb or supervise the orphaned populations.
3. **Reissue the wrong-channel notices.** CBP-031-08 and CBP-031-10 delivered to `archive-in_re_residential_fixture_pricing@example.test` where the operative records require `notices-aurora_home_supply_co@example.test`. Reissuance needs no court action — only proof of delivery to the correct address.
4. **Fix the superseded-revision reliance.** CBP-031-10's operations extract cites REV-2024.2; the operative record states REV-2025.3 is the later effective revision. The record set itself resolves this — the fix is operational, not adjudicative.
5. **Confirm and document the compliant population.** CBP-031-04 (metadata field loss) was completed 2025-11-25, two days before the 2025-11-27 operative deadline (R665). It can be certified as complete with its supporting records cited.
6. **Quantify and disclose the shortfall populations.** The 133-record shortfall is already computed from the record set. Drafting the cure plan and the production-log work to close the deltas can start immediately under the active owners (Leona Park, Henry Cho, Owen Delgado, and a re-owned CBP-031-01 line).
7. **Open the crosswalk-revision process** for the two entity collisions (CBP-031-03, CBP-031-11). Filing the revision request or initiating reconciliation is within Aurora's control; the *outcome* is not (see "must wait").
8. **Prepare the lateness disclosure** for CBP-031-09 (clawback completed 2025-05-12 against a 2025-03-31 deadline under R664). The fact cannot be changed; the disclosure and any excuse motion can be prepared now.

### Must wait (cannot be completed by 2026-09-05)

1. **An approved crosswalk revision resolving ENT-031-1002 vs ENT-031-2002 (CBP-031-03) and ENT-031-1010 vs ENT-031-2010 (CBP-031-11).** The record states no approved revision resolves either collision. Until one exists, custodian scope and production boundaries for those populations cannot be certified.
2. **Closure of the three "open and unresolved" statuses** (CBP-031-03 under R694; CBP-031-05 under R821; CBP-031-12 under R908). Each operative record states the open status blocks completion. Closure requires the underlying operational fix *and* a record showing the status is no longer open.
3. **Production of the 133 shortfall records** and updated logs evidencing them. Producing takes time; evidencing takes longer.
4. **Approval/activation of the two inactive owners.** Samuel Kim's and Dominic Alvarez's approval status is an internal-governance event the team can trigger but not complete on demand.
5. **Any court determination** on the clawback lateness (CBP-031-09) and, if challenged, on privilege treatment for CBP-031-12 — where the common-interest support gap is the basis for privilege treatment. Privilege certification for that population waits on the support gap closing or the court ruling.

---

## 3. Gap register — what must be cured before certification, with owners and holds

Each population below lists the operative requirement (R-reference), the current operations position (E-reference, non-authoritative), the gap, the owner of record from the capacity roster, and the hold. Every current-operations extract states it does not state a legal disposition; the R-reference governs.

| # | Population / issue | Operative requirement | Current position | Gap before certification | Owner of record (status, capacity, next control) | Hold |
|---|---|---|---|---|---|---|
| 1 | **CBP-031-01** Bates-range overlap | R753: population is 215 records | E138: certified 180 | Produce and certify the 35-record delta (215−180); reconcile the 180-vs-215 family overlap in a manifest | **Samuel Kim** (pending approval, inactive, 0; next 2026-09-04) | Ownership dead; certification of this population blocked until re-owned |
| 2 | **CBP-031-02** Email-family separation | R682: threshold is 11% | E716: result is 14% | Result exceeds threshold by 3 pts — bring separation within 11% or obtain relief | **Talia Brooks** (active, 1; next 2026-09-03) | Exceeds operative threshold |
| 3 | **CBP-031-03** Request-response mismatch | R694: open mismatch **blocks completion** | E452: open and unresolved | Close the mismatch and obtain a record showing closed status | **Adrian Mensah** (active, 4; next 2026-09-02) | Blocks completion + entity collision (ENT-031-1002/2002) |
| 4 | **CBP-031-04** Metadata field loss | R665: due 2025-11-27 | E980: completed 2025-11-25 | None — compliant | **Farah Ibrahim** (active, 4; next 2026-09-01) | — |
| 5 | **CBP-031-05** Collection-date inconsistency (mobile chats) | R821: open inconsistency **blocks completion** | E407: open and unresolved | Verify and reconcile chat collection dates; close the open status | **Dominic Alvarez** (pending approval, inactive, 0; next 2026-08-31) | Blocks completion + ownership dead |
| 6 | **CBP-031-06** Protective-order designation error | R246: population is 148 records | E214: certified 125 | Cure the 23-record designation delta (148−125) | **Leona Park** (active, 6; next 2026-08-30) | 23-record shortfall |
| 7 | **CBP-031-07** Production gap | R626: population is 78 records | E660: certified 40 | Produce the 38-record delta (78−40) | **Henry Cho** (active, 6; next 2026-08-29) | 38-record shortfall |
| 8 | **CBP-031-08** Legal-hold delivery gap (departed custodians) | R397: notices to `notices-aurora_home_supply_co@example.test` | E382: receipt from `archive-in_re_residential_fixture_pricing@example.test` | Reissue notices to the required address; obtain proof of delivery | **Maya Ellison** (active, 1; next 2026-08-28) | Wrong delivery channel |
| 9 | **CBP-031-09** Clawback deadline (privilege challenge) | R664: due 2025-03-31 | E503: completed 2025-05-12 | Lateness is historical — cannot be cured; disclose and seek excuse | **Jonas Feld** (active, 1; next 2026-08-27) | 42 days late; not retroactively curable |
| 10 | **CBP-031-10** Third-party subpoena deadline | R537: notices to `notices-aurora_home_supply_co@…`; REV-2025.3 controls | E178: receipt from archive address; cites REV-2024.2 | Reissue notices to the required address; restate reliance under REV-2025.3 | **Willa Novak** (active, 4; next 2026-09-04) | Wrong delivery channel + superseded revision |
| 11 | **CBP-031-11** Custodian omission (departed custodians) | R976: population is 98 records | E151: certified 61 | Cure the 37-record delta (98−61) | **Owen Delgado** (active, 3; next 2026-09-03) | 37-record shortfall + entity collision (ENT-031-1010/2010) |
| 12 | **CBP-031-12** Common-interest support gap (privilege challenge) | R908: open gap **blocks completion** | E253: open and unresolved | Close the common-interest support gap with documentary support | **Priya Raman** (active, 1; next 2026-09-02) | Blocks completion; privilege treatment cannot be certified while open |

**Uncertified-record total (operative population minus certified):** 35 + 23 + 38 + 37 = **133 records**.

### Hard holds (no certification until these clear)

1. **H1 — Entity collisions (CBP-031-03, CBP-031-11).** No approved crosswalk revision resolves ENT-031-1002 vs ENT-031-2002 or ENT-031-1010 vs ENT-031-2010. Records: CB-DOC-031-003, CB-DOC-031-011.
2. **H2 — "Blocks completion" statuses (CBP-031-03, -05, -12).** Open under R694, R821, R908 respectively.
3. **H3 — Population shortfalls (CBP-031-01, -06, -07, -11).** 133 records uncertified in aggregate.
4. **H4 — Wrong-channel notice delivery (CBP-031-08, -10).** Counterparty archive address used where the client notices address is required (R397, R537).
5. **H5 — Ownership vacuum (CBP-031-01, -05).** Owners of record pending approval, inactive, zero capacity.
6. **H6 — Superseded revision reliance (CBP-031-10).** REV-2024.2 cited; REV-2025.3 controls per the operative record itself.
7. **H7 — Historical lateness (CBP-031-09).** Clawback completed 42 days after the R664 deadline; not curable retroactively — disclose or seek excuse.

### Prioritization

Impact-control scores are inputs, not dispositions, and are used here only to sequence work. Ranked by impact: CBP-031-03 (91), CBP-031-02 (89), CBP-031-12 (85), CBP-031-06 (82), CBP-031-05 (70), CBP-031-09 (61), CBP-031-07 (58), CBP-031-08 (57), CBP-031-11 (55), CBP-031-04 (45), CBP-031-01 (37), CBP-031-10 (33). The three highest-impact populations are all hard holds.

---

## 4. What evidence would change the answer

Certification becomes supportable when the record set shows these. Each item maps to a specific hold above.

1. **An approved crosswalk revision** resolving ENT-031-1002 vs ENT-031-2002 (CBP-031-03) and ENT-031-1010 vs ENT-031-2010 (CBP-031-11). *(Clears H1.)*
2. **Updated current-operations records showing closed status** for the three "open and unresolved" populations — the operative records themselves would need to show the blocking status closed under R694, R821, and R908. *(Clears H2.)*
3. **Production logs and certification records covering the full operative populations** — 215 (CBP-031-01), 148 (CBP-031-06), 78 (CBP-031-07), 98 (CBP-031-11) — evidencing the 133-record delta produced, plus a manifest reconciling the 180-vs-215 Bates family overlap. *(Clears H3.)*
4. **Reissued notices with proof of delivery to `notices-aurora_home_supply_co@example.test`** for CBP-031-08 and CBP-031-10, and operations records restated under REV-2025.3 for CBP-031-10. *(Clears H4, H6.)*
5. **Approved, activated ownership for CBP-031-01 and CBP-031-05**, or a documented reassignment to an active owner with capacity. *(Clears H5.)*
6. **A court order excusing the CBP-031-09 clawback lateness**, or an operative record resetting the deadline. *(Clears H7.)*
7. **Evidence the 14% email-family separation result is within threshold** — either a corrected separation result under 11% (R682, CBP-031-02) or an operative revision of the threshold.

Conversely, the answer would harden against certification if: the counterparty's position in any correspondence record ripens into a motion; the entity collisions spread to other populations; or the 133-record shortfall is litigated rather than cured.

---

## 5. Method and reliance limits

- Each of the 12 defect populations carries 8 records in fixed evidence roles: identity crosswalk, operative authority, current operations, approval and capacity, correspondence, financial or population support, chronology and custody, and an independent counterrecord. The chronology-and-custody records independently confirm which record is operative for each population.
- The R-reference is the requirement (authoritative); the E-reference is the internal operating extract (non-authoritative, and stated in each record not to be a legal disposition). Where revisions conflicted (CBP-031-10), the operative record itself states REV-2025.3 is the later effective revision.
- Every record carries reliance limits: no legal effect decided, no revision priority established by internal extracts, no resolution of another system's entity identity. This memo respects those limits — it is a working position on what the record set supports, not a legal opinion.
- The 88 stray `ENT-031-2xxx` row-level values across native-row tables are a systematic data-quality artifact distinct from the two genuine crosswalk collisions; they are flagged in the reconciliation file but do not independently block certification.
- **Source records are synthetic CounselBench-100 data.** This analysis is not legal advice and covers the twelve defect populations evidenced in the CB-LD-2701 record set, not an audit of the entire production.

**Companion file:** `output/aurora_mdl_reconciliation.json` — the machine-readable reconciliation (all 12 populations, records, references, owners, holds, and impact scores) recording the outcome, holds, and owners in the workspace.
