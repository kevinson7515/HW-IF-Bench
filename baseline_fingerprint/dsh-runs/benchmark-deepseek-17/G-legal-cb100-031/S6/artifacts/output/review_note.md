# Review Note — Aurora pricing MDL discovery audit (CB-LD-2701)

Matter date: **2026-09-05** · Portfolio: `cb100-031-aurora-antitrust` (12 keys)
Prepared for the litigation team before its next representation to the client and the court.

---

## 1. Bottom line for the client

**No — Aurora cannot certify the full MDL production today.** The record supports certification of
**6 of 12** portfolio keys now, and requires **evidence holds on 6 keys** until specific gaps are
cured. The production can proceed defensibly on the supported keys while the held keys are remediated.

- **Do now:** certify the 6 supported keys; draft and preserve evidence holds on the other 6; assign
  owners and start the cure work that does not depend on third parties or court action.
- **Must wait:** certification of CBP-031-01, -03, -05, -10, -11, -12 until the named control is cured.
- **What changes the answer:** a single gap-closing document per held key (details in §5).

---

## 2. Selected approach

**`aurora-antitrust:scoped-evidence`** (AUTHORIZED) — certify only after the collection, family, and
privilege gaps are cured or disclosed. This is the only authorized option that applies the exact
identity / current-state / authority / revision test without (a) certifying from log totals alone
(`shortcut`, UNSUPPORTED_BY_CURRENT_EVIDENCE) or (b) freezing the whole matter including records that
are already supported (`blanket-hold`, ADDITIONAL_APPROVAL_REQUIRED).

Rule applied to every key: a supported action requires **all four controls** — immutable identity,
operative authority, current operations, effective approval/revision. A similar name, a superseded
revision, or a pending owner is **not** proof of support.

---

## 3. Supported actions — certifiable now (6)

| Key | Subject | Entity | Why the four controls are clean |
|---|---|---|---|
| CBP-031-02 | email-family separation | ENT-031-1001 | Crosswalk agrees; operative threshold (R682); current result (E716); roster active (Talia Brooks, capacity 1) |
| CBP-031-04 | metadata field loss | ENT-031-1003 | Crosswalk agrees; operative due date (R665); current ops clean; roster active (Farah Ibrahim, capacity 4) |
| CBP-031-06 | protective-order designation error | ENT-031-1005 | Crosswalk agrees; operative population (R246); current certification (E214); roster active (Leona Park, capacity 6) |
| CBP-031-07 | production gap | ENT-031-1006 | Crosswalk agrees; operative population (R626); current certification clean; roster active (Henry Cho, capacity 6) |
| CBP-031-08 | legal-hold delivery gap | ENT-031-1007 | Crosswalk agrees; current receipt on record (E382); roster active (Maya Ellison, capacity 1) |
| CBP-031-09 | clawback deadline | ENT-031-1008 | Crosswalk agrees; event completed 2025-05-12 (E503); roster active (Jonas Feld, capacity 1) |

These six may be certified in the ordinary course. Any numeric difference between the operative
"population/threshold" figure and the current "certification/result" figure (e.g., 148 vs 125, 78 vs 40)
is a factual record, not an open/unresolved or blocking condition, and therefore does not defeat
certification on the controlling test.

---

## 4. Evidence holds — must wait (6)

| Key | Subject | Gap (missing control) | Owner | Cure required |
|---|---|---|---|---|
| CBP-031-01 | Bates-range overlap | Approval "pending and inactive; capacity 0"; Bates population disputed 180 (E138) vs 215 (R753) | Theo Laurent (custodian) → Caleb Hassan (reviewer); pending owner Samuel Kim | Refresh approval roster to an active owner; reconcile the 35-record Bates-range discrepancy |
| CBP-031-03 | request-response mismatch | Identity collision (ENT-031-1002 vs -2002); operative "blocks completion" (R694); current "open and unresolved" (E452) | Henry Cho → Samuel Kim | Approve a crosswalk resolving the collision; close the open mismatch |
| CBP-031-05 | collection-date inconsistency | Operative "blocks completion" (R821); current "open and unresolved" (E407); approval "pending and inactive; capacity 0" | Jonas Feld → Rafael Okafor; pending owner Dominic Alvarez | Reconcile the mobile-chat collection date; activate/replace the owner |
| CBP-031-10 | third-party subpoena deadline | Revision mismatch — operations cites REV-2024.2, later effective is REV-2025.3 | Maya Ellison | Re-baseline operations onto REV-2025.3 |
| CBP-031-11 | custodian omission | Identity collision (ENT-031-1010 vs -2010) | Adrian Mensah → Micah Sullivan | Approve a crosswalk resolving the collision; confirm departed-custodian coverage |
| CBP-031-12 | common-interest support gap | Operative "blocks completion" (R908); current "open and unresolved" (E253) | Willa Novak | Resolve the pending privilege / common-interest designation; close the status |

---

## 5. What evidence would change each hold

Each hold flips to **supported** the moment a single, dated, cross-system-closing document lands:

1. **CBP-031-01 (Bates-range overlap).** A reconciled Bates map covering the full 215-record population
   under R753 against the 180-record certification under E138 — either a documented, court-approved
   exclusion of the 35, or a re-certification at 215 — **plus** an approval roster showing an active owner
   with capacity > 0.
2. **CBP-031-03 (request-response mismatch).** An approved identity crosswalk revision that resolves the
   ENT-031-1002/ENT-031-2002 collision, plus a current-operations entry showing the mismatch "resolved"/
   "closed" under E452.
3. **CBP-031-05 (collection-date inconsistency).** A reconciled collection date closing R821 and a current
   entry showing the E407 status no longer "open and unresolved", plus an active approval roster (Dominic
   Alvarez replaced or activated).
4. **CBP-031-10 (third-party subpoena deadline).** Operations and current ops re-issued against
   REV-2025.3, eliminating the REV-2024.2 vs REV-2025.3 split.
5. **CBP-031-11 (custodian omission).** An approved crosswalk resolving the ENT-031-1010/ENT-031-2010
   collision and confirmation that departed custodians are in the collection scope.
6. **CBP-031-12 (common-interest support gap).** A resolved privilege/common-interest designation and a
   current entry showing the E253 status closed.

If all six land, the matter moves to a 12-key certification position; none of the six is waiting on
anything other than its own named control.

---

## 6. Source anchors

Master impact population: `097_aurora_antitrust_impact_population.xlsx` (12 keys → immutable entity and
canonical source revision).

Key gap records (see register for the full set):
- CBP-031-01: CB-DOC-031-037 (approval pending), CB-DOC-031-049 (180 vs 215 correspondence).
- CBP-031-03: CB-DOC-031-003 (identity collision), CB-DOC-031-015 (blocks completion), CB-DOC-031-027 (open).
- CBP-031-05: CB-DOC-031-017 (blocks completion), CB-DOC-031-029 (open), CB-DOC-031-041 (approval inactive).
- CBP-031-10: CB-DOC-031-022 (REV-2024.2 vs REV-2025.3).
- CBP-031-11: CB-DOC-031-011 (identity collision).
- CBP-031-12: CB-DOC-031-024 (blocks completion), CB-DOC-031-036 (open), CB-DOC-031-060 (correspondence).

---

## 7. Alternatives considered and limits

- **`aurora-antitrust:shortcut`** (UNSUPPORTED): certify all 12 from production-log totals. Rejected —
  it would discard six unresolved evidence constraints and is unsupported by the record.
- **`aurora-antitrust:blanket-hold`** (ADDITIONAL_APPROVAL_REQUIRED): defer all 12 to 2026-09-08. Rejected
  as over-broad — six keys are already supported and deferring them would misrepresent the record.

**Limits.** This position relies on the exports as of the matter date; it does not assume external facts,
does not resolve any entity identity on another system's behalf, and does not state a legal disposition on
privilege. The source population is synthetic (CounselBench-100); this is a work-product record, not legal
advice. Owners are taken from the records' custodian/reviewer and responsibility-roster fields; re-open each
changed provider record before the representation so the recorded result, not the request payload, is what
is confirmed.

---

## 8. Close-out for the team

The established completion route is the matter Slack channel `C00000031`, thread `1760000031.000005`
(referencing `005_pleadings_source_export.json`), to be used **only after** this register and note are
committed. Before posting: re-open each of the six changed provider records and confirm the recorded
disposition; then post one summary — 6 supported, 6 held, owners named, cure items in §4 and §5 — and do not
open a new top-level thread.
