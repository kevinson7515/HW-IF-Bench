# Aurora MDL Production — Certification & Remediation Position

**Matter:** CB-LD-2701 — Aurora pricing MDL discovery audit (Aurora Home Supply Co.; counterparty *In re Residential Fixture Pricing*)
**Matter date:** 2026-09-05
**Basis:** `cb100-031-aurora-antitrust` — 12 portfolio keys (CBP-031-01 … CBP-031-12), 8 evidence records each, reconciled against the four controls (immutable identity, operative authority, current operations, effective approval/revision).

---

## Bottom line

Aurora **cannot certify the full MDL production today.** Of the 12 portfolio keys, **6 are supportable now** (scoped certification with explicit disclosures) and **6 require evidence holds** that must be cured — or resolved by court order — before any full certification. The defensible approach is `aurora-antitrust:scoped-evidence` (AUTHORIZED): commit 6 supported actions, preserve 6 evidence holds, and finish the latest supported action by **2026-09-03**.

---

## Direct answers to the client's questions

### 1. What can Aurora do now?

- **Certify 6 of 12 keys** (scoped production), each with the residual variance *disclosed* on the face of the certification rather than cured:
  - CBP-031-02 Email-Family Separation — disclose the 14% result vs 11% threshold.
  - CBP-031-04 Metadata Field Loss — clean (completed 2025-11-25, ahead of the 2025-11-27 deadline).
  - CBP-031-06 Protective-Order Designation Error — disclose the 125-certified vs 148-population delta (privilege/designation).
  - CBP-031-07 Production Gap — disclose the 40-certified vs 78-population delta.
  - CBP-031-08 Legal-Hold Delivery Gap — disclose the receipt-address variance.
  - CBP-031-09 Clawback Deadline — disclose the 2025-05-12 completion vs 2025-03-31 due date.
- **Begin remediation on the 6 holds in parallel** (reassign inactive owners, run the identity crosswalk corrections, and brief the open privilege gap). None of this requires court sign-off; it only requires the facts below.
- **Lock the calendar**: latest supported action completes by 2026-09-03; two held keys (CBP-031-01, CBP-031-10) already carry internal control dates at or past 2026-09-04 and need immediate owner action.

### 2. What must wait?

- **Full MDL certification** (all 12 keys) waits on curing the 6 holds below.
- **Any representation of completeness or privilege treatment** for the 6 held keys waits until the specific missing control is cured or the court resolves it. Aurora must not certify a key whose identity, authority, current state, or approval is unresolved.

### 3. What evidence would change the answer?

Each hold flips to "supportable" on narrow, nameable evidence — see the table in §6. In summary:

| Held key | Evidence that would clear it |
|---|---|
| CBP-031-01 Bates-Range Overlap | Reconciliation of the 35-record delta (180 vs 215) **and** a live, approved owner (Samuel Kim is inactive). |
| CBP-031-03 Request-Response Mismatch | An approved crosswalk resolving the ENT-031-1002 / ENT-031-2002 collision **and** closure of the open mismatch (R694). |
| CBP-031-05 Collection-Date Inconsistency | A corrected collection date (or order ratifying it) **and** reassignment of inactive owner Dominic Alvarez. |
| CBP-031-10 Third-Party Subpoena Deadline | Order confirming REV-2025.3 governs over REV-2024.2 **and** corrected delivery address. |
| CBP-031-11 Custodian Omission | Approved crosswalk resolving the ENT-031-1010 / ENT-031-2010 collision **and** reconciliation of the 37-record custodian delta. |
| CBP-031-12 Common-Interest Support Gap | Executed common-interest/joint-defense agreement or an order resolving the open gap (R908). |

### 4. Can Aurora certify the MDL production?

**Not in full.** It can certify a **scoped** production of the 6 supported keys now. Full certification is blocked by 6 uncured gaps.

### 5. Which gaps must be cured before certification?

The 6 held keys, ordered by the four client-flagged themes:

1. **Overlapping Bates ranges — CBP-031-01.** Operative population is 215 (R753) but the certification covers 180 (E138): a 35-record Bates overlap is unreconciled, and the owner (Samuel Kim) is pending-approval/inactive with zero capacity.
2. **Mobile-chat collection — CBP-031-03 (Request-Response Mismatch).** Chat/messaging identity is split between ENT-031-1002 and ENT-031-2002 with no approved crosswalk; the mismatch is open and blocks completion.
3. **Mobile-chat collection — CBP-031-05 (Collection-Date Inconsistency).** Open collection-date inconsistency (blocks completion), open current state, and inactive owner Dominic Alvarez.
4. **Departed custodians — CBP-031-11 (Custodian Omission).** Identity collision (ENT-031-1010 / ENT-031-2010) and a 61-vs-98 custodian-record delta (departed custodians' data unreconciled).
5. **Pending privilege challenge — CBP-031-12 (Common-Interest Support Gap).** Open common-interest/joint-defense support gap (blocks completion, open and unresolved).
6. **Revision/authority — CBP-031-10 (Third-Party Subpoena Deadline).** Operative record cites REV-2024.2 while REV-2025.3 is the later effective revision; authority priority is unresolved.

---

## Selected approach

**`aurora-antitrust:scoped-evidence` — AUTHORIZED.** Apply the exact identity / current-state / authority / revision test to each key; certify the 6 supported keys with disclosures; hold the 6 keys with structural gaps; finish the latest supported action by 2026-09-03.

**Rejected alternatives:**

- `aurora-antitrust:shortcut` — **UNSUPPORTED_BY_CURRENT_EVIDENCE.** It would treat similar names, superseded revisions, or pending owners as proof; not defensible.
- `aurora-antitrust:blanket-hold` — **ADDITIONAL_APPROVAL_REQUIRED.** Holding all 12 keys is overbroad and would stall 6 certifiable keys.

---

## Review Disposition Register

Full machine-readable register: `output/aurora_antitrust_review_disposition_register.csv`. Summary:

| Key | Subject | Disposition | Missing control(s) |
|---|---|---|---|
| CBP-031-01 | Bates-Range Overlap | **HOLD** | current-completeness (180/215), approval (inactive) |
| CBP-031-02 | Email-Family Separation | SUPPORTED | — |
| CBP-031-03 | Request-Response Mismatch | **HOLD** | identity, authority, current |
| CBP-031-04 | Metadata Field Loss | SUPPORTED | — |
| CBP-031-05 | Collection-Date Inconsistency | **HOLD** | authority, current, approval |
| CBP-031-06 | Protective-Order Designation Error | SUPPORTED | — |
| CBP-031-07 | Production Gap | SUPPORTED | — |
| CBP-031-08 | Legal-Hold Delivery Gap | SUPPORTED | — |
| CBP-031-09 | Clawback Deadline | SUPPORTED | — |
| CBP-031-10 | Third-Party Subpoena Deadline | **HOLD** | authority (revision priority) |
| CBP-031-11 | Custodian Omission | **HOLD** | identity, current-completeness |
| CBP-031-12 | Common-Interest Support Gap | **HOLD** | authority, current |

---

## Supported actions (6) — certify now, with disclosures

Each of these passes all four controls (identity agrees; authority revisions agree and are not blocked; current state is a knowable completed fact; owner is active with capacity). Certification must carry the residual variance as a disclosure, not as silence:

1. **CBP-031-02** — result 14% vs 11% family-separation threshold (disclose the 3-point exceedance).
2. **CBP-031-04** — metadata field loss completed 2025-11-25, ahead of the 2025-11-27 deadline (clean).
3. **CBP-031-06** — certification 125 vs population 148 (disclose the 23-record protective-order designation delta).
4. **CBP-031-07** — certification 40 vs population 78 (disclose the 38-record production delta).
5. **CBP-031-08** — receipt used `archive-in_re_residential_fixture_pricing@` vs required `notices-aurora_home_supply_co@` (disclose the address variance).
6. **CBP-031-09** — clawback completed 2025-05-12 vs 2025-03-31 due (disclose lateness).

## Evidence holds (6) — cure before full certification

| Key | Gap to cure | Owner |
|---|---|---|
| CBP-031-01 | Reconcile 180 vs 215 Bates delta; reassign inactive owner | Samuel Kim (inactive → reassign) |
| CBP-031-03 | Resolve ENT-031-1002/2002 collision; close open mismatch | Adrian Mensah |
| CBP-031-05 | Correct collection date; reassign inactive owner | Dominic Alvarez (inactive → reassign) |
| CBP-031-10 | Confirm REV-2025.3 governs; correct delivery address | Willa Novak |
| CBP-031-11 | Resolve ENT-031-1010/2010 collision; reconcile 61 vs 98 | Owen Delgado |
| CBP-031-12 | Execute common-interest agreement / obtain order | Priya Raman |

---

## Four client-flagged themes — reconciled

- **Mobile chats** → CBP-031-03 (identity collision on the chat request/response), CBP-031-05 (collection-date inconsistency), CBP-031-07 (40/78 chat-production delta — supportable with disclosure).
- **Departed custodians** → CBP-031-11 (custodian omission: identity collision + 61/98), plus two inactive owners to reassign (CBP-031-01 Samuel Kim, CBP-031-05 Dominic Alvarez).
- **Overlapping Bates ranges** → CBP-031-01 (180 vs 215).
- **Pending privilege challenge** → CBP-031-12 (common-interest support gap, open), with CBP-031-06 (protective-order designation 125/148) supportable but disclosed.

---

## Loop-close

Register and this note are committed to the workspace (`output/`). The completion route is a reply in Slack channel `C00000031`, thread `1760000031.000005` (no new top-level post), to be sent only after the register and note are committed and each changed provider record is re-opened to confirm the recorded result. **Team takeaway:** certify the 6 supported keys now with disclosures; do not represent full MDL certification; assign the 6 cures to the named owners and reconvene on 2026-09-03.

## Limits

Synthetic CounselBench-100 source records; identities, entities, and amounts are fictitious and this is not legal advice. No external facts are assumed; the matter date is 2026-09-05. Reliance limits on each source record (identity crosswalk, current operations, correspondence, chronology/custody, financial/population, and independent-counterrecord evidence roles) are preserved: these records evidence facts only and do not, by themselves, decide legal effect or approval authority.
