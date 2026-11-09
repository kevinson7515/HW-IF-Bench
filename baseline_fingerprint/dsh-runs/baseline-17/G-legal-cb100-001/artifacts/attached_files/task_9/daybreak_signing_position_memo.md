# Project Daybreak (CB-MA-2401) — Signing / Close Operating Position

**To:** Deal team · **Matter:** CB-MA-2401 — Project Daybreak battery acquisition
**Position date:** 2026-09-04 · **Author:** Matter counsel (operating position)

---

## Bottom line

**Signing can proceed, but only after one signing-path item is cleared.** Nothing in the
record set blocks *signing* outright. The two gaps the team flagged — the **Nevada cathode
tooling** and the **automaker's indirect change-of-control termination right** — are
**closing conditions, not signing blockers**. They belong in the closing-conditions
schedule, not the signing path and not (yet) in a priced exception.

The one item that must be settled on the **signing path** is the **charter-authorization
mismatch** (CBP-001-01): the acquired entity's identity is unresolved and the signatory
authority is disputed. That is a gating condition to execution, and it is the only place the
record set leaves a genuine "missing authority" — it must be reconciled, not assumed.

---

## 1. Can signing proceed?

**Yes — conditionally.** Distinguish two classes in the operative-authority records:

- **"Blocks completion"** (permit transfer, revenue recognition, open-source copyleft) —
  these block *completion/closing*, not signing.
- **"Approval must come from [person]"** (change-of-control consent, anti-assignment,
  invention assignment, security incident) — these are consents/authorizations obtained as
  conditions to *closing*, not execution.

The only approval that gates **execution** is the charter-authorization mismatch, because
you cannot validly execute until you know (a) which entity is the signatory and (b) who has
authority to bind it.

### The signing-path item

| Item | Portfolio key | Operative authority | Dispute / gap |
|---|---|---|---|
| Charter authorization mismatch | CBP-001-01 (ENT-001-1000 **vs** ENT-001-2000) | "approval must come from **Maya Ellison** under **CB-MA-2401-R983**" (CB-DOC-001-013) | Identity collision unresolved ("no approved crosswalk revision resolves the collision," CB-DOC-001-001); operations cites **Jonas Feld** under **E257** (CB-DOC-001-025, -049) |

**Resolution rule (matter-level control):** *"The executed purchase terms and the latest
consent schedule control; seller summaries do not."* The R-series operative authority
(R983 → Maya Ellison) is the executed-terms position; the E-series operating extracts
(E257 → Jonas Feld) are seller summaries and do **not** control.

**Do not guess the entity:** no record resolves which of ENT-001-1000 vs ENT-001-2000 is the
acquired entity. That collision is a genuine open authority item to be resolved before
execution (crosswalk fix), not assumed.

---

## 2. The two flagged gaps → closing conditions

### (a) Customer-consent gap — automaker termination on indirect change of control

| Field | Value |
|---|---|
| Issue | **Change-of-Control Consent** (CBP-001-11) |
| Entity | ENT-001-1010 (crosswalk clean; alias ENT-001-2010 excluded, CB-DOC-001-011) |
| Operative authority | "change-of-control consent approval must come from **Talia Brooks** under **CB-MA-2401-R473**" (CB-DOC-001-023) |
| Operations view | Names **Caleb Hassan** under **E439** (CB-DOC-001-035); correspondence records both and says "must be reconciled" (CB-DOC-001-059) |
| Live status | "pending approval and **inactive**; remaining matter capacity **0**"; next internal control **2026-09-02** (CB-DOC-001-047) |
| Classification | **Closing condition** |

The automaker's right to terminate on an **indirect** change of control is triggered by this
acquisition (a change in the target's upstream ownership without a change in the contract
counterparty). The consent has **not** been obtained and is the tightest open item (capacity 0,
control date two days before the 2026-09-04 position deadline). Per the matter-level control,
the operative authority (R473 → Talia Brooks) is the position to follow; the E439 seller
summary does not control.

### (b) Tooling gap — cathode tooling in Nevada

| Field | Value |
|---|---|
| Issue | **Permit Transfer Restriction** (CBP-001-03) |
| Entity | ENT-001-1002 (crosswalk clean; alias ENT-001-2002 excluded, CB-DOC-001-003) |
| Operative authority | "**open permit transfer restriction blocks completion** under **CB-MA-2401-R164**" (CB-DOC-001-015) |
| Operations view | "status open and unresolved" under E368 (CB-DOC-001-027) |
| Live status | active; capacity 3; next internal control **2026-09-01** (CB-DOC-001-039) |
| Classification | **Closing condition** |

The cathode tooling is sited in Nevada, so transfer of the manufacturing business is gated by
transfer of the Nevada operating permits. The operative authority states the restriction
**blocks completion** — that is definitionally a closing condition. There is no record
evidence that the tooling itself is owned by the automaker rather than the carve-out
manufacturer, so no separate tooling-*ownership* consent is evidenced; the evidenced gap is the
permit transfer.

---

## 3. Full classification (all 12 portfolio keys)

| Key | Issue | Operative-authority verb | Classification |
|---|---|---|---|
| CBP-001-01 | Charter authorization mismatch | approval (Maya Ellison, R983) + unresolved entity collision | **Signing path** |
| CBP-001-02 | Financial covenant breach | threshold **7%** (R158) | Priced exception |
| CBP-001-03 | Permit transfer restriction | **blocks completion** (R164) | **Closing condition** (tooling) |
| CBP-001-04 | Revenue recognition exception | **blocks completion** (R532) | **Closing condition** |
| CBP-001-05 | Most-favored-customer exposure | threshold **13%** (R572) | Priced exception |
| CBP-001-06 | Unreported security incident | approval (Theo Laurent, R990) | Closing condition (remedial) |
| CBP-001-07 | Claims-made insurance tail | due **2025-08-05** (R611) — lapsed | Priced exception |
| CBP-001-08 | Anti-assignment restriction | approval (Owen Delgado, R293); **REV-2025.1 controls over REV-2024.0** | **Closing condition** |
| CBP-001-09 | Open-source copyleft exposure | **blocks completion** (R971) | **Closing condition** |
| CBP-001-10 | Sales-tax nexus gap | limited to **Washoe County, NV** (R710) | Priced exception |
| CBP-001-11 | Change-of-control consent | approval (Talia Brooks, R473) | **Closing condition** (customer consent) |
| CBP-001-12 | Invention assignment defect | approval (Caleb Hassan, R433) | Closing condition (IP) |

**Closing conditions (seven):** permit transfer (03), revenue recognition (04), unreported
security incident (06), anti-assignment (08), open-source copyleft (09), change-of-control
consent (11), invention assignment (12).

**Priced exceptions (four):** financial covenant (02, 7%), MFC exposure (05, 13%),
claims-made insurance tail (07, lapsed), sales-tax nexus (10, Washoe County only).

**Signing path (one):** charter authorization mismatch (01).

---

## 4. Reconciliation principle applied throughout

Every operative-authority record carries the same matter-level control: **"The executed
purchase terms and the latest consent schedule control; seller summaries do not."** Applied:

- **R-series** references (R983, R473, R164, R293, R611, etc.) = executed-terms / consent-schedule
  authority → **controls**.
- **E-series** references (E257, E439, E368, E341, E921, etc.) = operating extracts / seller
  summaries / population inputs → **do not control**.
- **Anti-assignment (08)** additionally carries a revision conflict: operations cites
  REV-2024.0, but **REV-2025.1 is the later effective revision** and controls (CB-DOC-001-020).

The impact-population spreadsheet (`097_helios_forge_impact_population.xlsx`) and the
"impact-control score" fields are explicitly **inputs, not dispositions** — they do not move
the classification.

---

## 5. Open items — do not guess

1. **Entity identity for the charter (CBP-001-01).** ENT-001-1000 vs ENT-001-2000 is an
   unresolved collision with no approved crosswalk. Signing cannot be finalized until the
   correct acquired entity is pinned. *(All other 11 keys crosswalk cleanly to ENT-001-10xx,
   with the 2xxx alias excluded.)*
2. **The tooling-ownership question is not independently evidenced.** The records establish a
   permit-transfer gap in Nevada; they do not evidence an automaker-owned-tooling claim. If the
   team needs a tooling-*ownership* position, that is a separate diligence request, not
   inferable from this set.

---

## 6. Timing note

The change-of-control consent next internal control date (**2026-09-02**) and the permit
transfer date (**2026-09-01**) both land inside the 2026-09-04 position window. The
change-of-control consent is the critical-path closing condition: it is "pending approval and
inactive" with zero remaining capacity, and the automaker's termination right is the
highest-consequence exposure in the set.

---

## 7. Reliance limits

All source records are synthetic CounselBench-100 records; this is an operating position, not
legal advice. Each record's own reliance-limit language is preserved: these records supply
evidence for a portfolio key and do not themselves decide legal effect or select among
candidate responses. The classification above is the matter-level operating position derived
from the operative-authority records and the stated matter-level control.
