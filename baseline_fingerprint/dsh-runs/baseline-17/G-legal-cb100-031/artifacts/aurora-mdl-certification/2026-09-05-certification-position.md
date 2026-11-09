# Aurora MDL Production — Certification Position

**Matter:** CB-LD-2701 — Aurora pricing MDL discovery audit (Aurora Home Supply Co. v. In re Residential Fixture Pricing)
**Prepared for:** Litigation team, before the next representation
**Position date:** 2026-09-05 (matter date)
**Selected approach:** `aurora-antitrust:scoped-evidence` (AUTHORIZED)

---

## 1. Bottom line

**Aurora cannot certify the full MDL production today.** It can certify 6 of the 12 portfolio
keys now; the other 6 must be held and cured before certification. This is the "scoped-evidence"
route the matter protocol authorizes — certify what the four controls support, and hold the rest
with the exact missing control named.

- **Do now (certify):** 6 supported keys — CBP-031-02, -04, -06, -07, -08, -09.
  Finish the latest supported action by **2026-09-03**.
- **Must wait (hold):** 6 keys with a missing control — CBP-031-01, -03, -05, -10, -11, -12.
  Do not certify these until the named gap is cured.
- **Evidence that changes the answer:** for each hold, the specific cure listed in §4. Once that
  evidence lands, the key flips from hold to certify.

The two rejected routes: `shortcut` (certify from log totals without the custodian/overlap joins)
is **unsupported by current evidence**; `blanket-hold` (freeze all 12, defer the 6 already
supportable) is **additional-approval required** and needlessly delays certifiable work.

---

## 2. Governing rule (from the matter protocol, CB-DOC-031-089)

For each portfolio key, reconcile **four controls** before choosing a disposition:

1. **Immutable identity** (identity_crosswalk)
2. **Operative authority** (operative_authority)
3. **Current operations** (current_operations)
4. **Effective approval/revision** (approval_and_capacity)

> A supported action requires all four controls. Otherwise preserve an evidence hold and state
> the missing control; do not turn a **similar name**, a **superseded revision**, or a
> **pending owner** into proof.

The operative discovery order and certification population (the "R-" references) govern
completeness and privilege treatment. Correspondence, financial/population support, chronology,
and the independent counterrecord corroborate but do not, by themselves, set a disposition.

---

## 3. Review Disposition Register (one row per portfolio key)

Legend — Identity / Operative / Current / Approval = ✓ (clean) or ✗ (missing). Disposition is
**CERTIFY** (4 ✓) or **HOLD** (≥1 ✗). Impact-control score is an input, not a disposition.

| Key | Topic | Entity | Rev | Id | Op | Cur | App | Disposition | Missing control (named) |
|---|---|---|---|---|---|---|---|---|---|
| CBP-031-01 | Bates-Range Overlap | ENT-031-1000 | 2025.1 | ✓ | ✓ | ✓ | ✗ | **HOLD** | Effective approval — pending owner |
| CBP-031-02 | Email-Family Separation | ENT-031-1001 | 2025.2 | ✓ | ✓ | ✓ | ✓ | CERTIFY | — |
| CBP-031-03 | Request-Response Mismatch | ENT-031-1002/2002 | 2025.3 | ✗ | ✗ | ✗ | ✓ | **HOLD** | Identity (similar name) + operative + current |
| CBP-031-04 | Metadata Field Loss | ENT-031-1003 | 2025.4 | ✓ | ✓ | ✓ | ✓ | CERTIFY | — |
| CBP-031-05 | Collection-Date Inconsistency | ENT-031-1004 | 2025.5 | ✓ | ✗ | ✗ | ✗ | **HOLD** | Operative + current + approval (pending owner) |
| CBP-031-06 | Protective-Order Designation Error | ENT-031-1005 | 2025.6 | ✓ | ✓ | ✓ | ✓ | CERTIFY | — (disclose 125 vs 148) |
| CBP-031-07 | Production Gap | ENT-031-1006 | 2025.7 | ✓ | ✓ | ✓ | ✓ | CERTIFY | — (disclose 40 vs 78) |
| CBP-031-08 | Legal-Hold Delivery Gap | ENT-031-1007 | 2025.1 | ✓ | ✓ | ✓ | ✓ | CERTIFY | — (disclose receipt domain) |
| CBP-031-09 | Clawback Deadline | ENT-031-1008 | 2025.2 | ✓ | ✓ | ✓ | ✓ | CERTIFY | — (disclose 2025-05-12 vs 2025-03-31) |
| CBP-031-10 | Third-Party Subpoena Deadline | ENT-031-1009 | 2024.2→2025.3 | ✗ | ✗ | ✓ | ✓ | **HOLD** | Effective revision — superseded revision |
| CBP-031-11 | Custodian Omission | ENT-031-1010/2010 | 2025.4 | ✗ | ✓ | ✓ | ✓ | **HOLD** | Identity — similar name |
| CBP-031-12 | Common-Interest Support Gap | ENT-031-1011 | 2025.5 | ✓ | ✗ | ✗ | ✓ | **HOLD** | Operative + current (blocks completion) |

**Result: 6 CERTIFY, 6 HOLD.**

Impact-control scores (input only): 01=37 · 02=89 · 03=91 · 04=45 · 05=70 · 06=82 · 07=58 ·
08=57 · 09=61 · 10=33 · 11=55 · 12=85.

---

## 4. The six holds — gap, owner, and evidence that changes the answer

### HOLD 1 — CBP-031-01 · Bates-Range Overlap (overlapping Bates ranges)
- **Missing control:** effective approval/revision — "pending owner."
- **Owner:** Samuel Kim (current responsibility roster, `pending approval and inactive; capacity 0`).
- **Substance:** certification covers **180** records (E138) vs. operative population **215** (R753);
  35 records sit in overlapping Bates ranges. Impact score 37.
- **Evidence that changes the answer:** (a) an approved, **active** ownership assignment (capacity > 0);
  (b) a reconciled Bates-range map that assigns the 35 disputed records to single, non-overlapping ranges.
- **Anchors:** CB-DOC-031-001, -013, -025, -037, -049, -061.

### HOLD 2 — CBP-031-03 · Request-Response Mismatch
- **Missing controls:** immutable identity ("similar name"), operative authority ("blocks completion"),
  current operations ("open and unresolved").
- **Owner:** Adrian Mensah (roster, active).
- **Substance:** entity collision ENT-031-1002 vs ENT-031-2002 with no approved crosswalk;
  open mismatch "blocks completion" (R694) / "open and unresolved" (E452). Impact score 91.
- **Evidence that changes the answer:** an approved crosswalk resolving the 1002/2002 collision to a
  single entity, plus a reconciled request↔response pairing.
- **Anchors:** CB-DOC-031-003, -015, -027, -039, -051, -063.

### HOLD 3 — CBP-031-05 · Collection-Date Inconsistency (mobile collection)
- **Missing controls:** operative authority ("blocks completion"), current operations ("open and
  unresolved"), approval ("pending owner").
- **Owner:** Dominic Alvarez (roster, `pending approval and inactive; capacity 0`).
- **Substance:** open collection-date inconsistency blocks completion (R821 / E407); impact score 70.
- **Evidence that changes the answer:** reconciled collection dates for the mobile collection, plus an
  approved active owner.
- **Anchors:** CB-DOC-031-005, -017, -029, -041, -053, -065, -089.

### HOLD 4 — CBP-031-10 · Third-Party Subpoena Deadline
- **Missing control:** effective revision — "superseded revision."
- **Owner:** Willa Novak (roster, active).
- **Substance:** operations cite REV-2024.2, but REV-2025.3 is the later effective revision; notice
  receipt used `archive-in_re_residential_fixture_pricing@example.test` (E178) instead of
  `notices-aurora_home_supply_co@example.test` (R537). Impact score 33.
- **Evidence that changes the answer:** confirmation that REV-2025.3 is operative, and a corrected
  notice record using the `notices-aurora_home_supply_co@example.test` address.
- **Anchors:** CB-DOC-031-010, -022, -034, -046, -058, -070.

### HOLD 5 — CBP-031-11 · Custodian Omission (departed custodians)
- **Missing control:** immutable identity — "similar name."
- **Owner:** Owen Delgado (roster, active).
- **Substance:** entity collision ENT-031-1010 vs ENT-031-2010; certification covers **61** records
  (E151) vs. population **98** (R976) — 37 records from an omitted (departed) custodian. Impact score 55.
- **Evidence that changes the answer:** an approved crosswalk resolving the 1010/2010 collision, plus
  collection of the 37 omitted records from the departed custodian (61 → 98).
- **Anchors:** CB-DOC-031-011, -023, -035, -047, -059, -071.

### HOLD 6 — CBP-031-12 · Common-Interest Support Gap (pending privilege challenge)
- **Missing controls:** operative authority ("blocks completion"), current operations ("open and
  unresolved").
- **Owner:** Priya Raman (roster, active).
- **Substance:** open common-interest support gap blocks completion (R908 / E253). Impact score 85.
- **Evidence that changes the answer:** an executed common-interest / joint-defense agreement and
  privilege-log support that closes the common-interest gap.
- **Anchors:** CB-DOC-031-012, -024, -036, -048, -060, -072.

---

## 5. The four client concerns → keys

| Client concern | Keys | Status |
|---|---|---|
| Mobile chats / mobile collections | CBP-031-05 (collection-date) · CBP-031-07 (production gap) | -05 **HOLD**; -07 CERTIFY with 40-of-78 disclosure |
| Departed custodians | CBP-031-11 (custodian omission) | **HOLD** |
| Overlapping Bates ranges | CBP-031-01 (Bates-range overlap) | **HOLD** |
| Pending privilege challenge | CBP-031-12 (common-interest gap) · CBP-031-06 (protective-order error) | -12 **HOLD**; -06 CERTIFY with 125-of-148 disclosure |

---

## 6. What is resolved, what waits

**Resolved (can be certified now, latest by 2026-09-03):**
- CBP-031-02 Email-Family Separation — all four controls clean (disclose result 14% vs threshold 11%).
- CBP-031-04 Metadata Field Loss — completed 2025-11-25, ahead of the 2025-11-27 due date.
- CBP-031-06 Protective-Order Designation Error — disclose 125 certified vs 148 asserted.
- CBP-031-07 Production Gap — disclose 40 certified vs 78 asserted.
- CBP-031-08 Legal-Hold Delivery Gap — disclose the `archive-in_…` vs `notices-aurora_…` receipt domain.
- CBP-031-09 Clawback Deadline — disclose completion 2025-05-12 vs deadline 2025-03-31.

**Held (must wait for cure before any representation of completeness):**
- CBP-031-01, -03, -05, -10, -11, -12 — per §4.

**Owners** are the current responsibility-roster names (§4); remediation owners for the two
"pending owner" holds are Samuel Kim (01) and Dominic Alvarez (05), who must be moved to active
with capacity, or replaced, before those keys certify.

---

## 7. Completion route (for the team)

Record one row per portfolio key in the matter's Review Disposition Register, with selected
approach, supported actions, evidence holds, source anchors, alternatives, and limits. The
protocol completion route is the Slack thread `C00000031` / `1760000031.000005`
(005_pleadings_source_export.json); do not open a new top-level post, and re-open each changed
provider record so the recorded result — not the request payload — is confirmed before finishing.

No external facts are assumed beyond the 2026-09-05 matter date.
