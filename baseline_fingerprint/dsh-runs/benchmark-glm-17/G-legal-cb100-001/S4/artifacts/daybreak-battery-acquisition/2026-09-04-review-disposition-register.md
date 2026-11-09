# Project Daybreak — Review Disposition Register

**Matter:** CB-MA-2401 — Project Daybreak battery acquisition (Helios Forge, Inc. / BluePeak Battery Systems LLC)
**Register date:** 2026-09-04 (matter date)
**Selected approach:** `helios-forge:scoped-evidence` (AUTHORIZED, incremental cost $18,200)
**Role:** system of record, one row per portfolio key, per the matter work-product protocol (CB-DOC-001-089). Companion note: `2026-09-04-review-note.md`.

---

## Legend

Id / Op / Cur / App are the four controls each key must reconcile before a disposition: immutable identity (identity_crosswalk), operative authority (operative_authority), current operations (current_operations), and effective approval/revision (approval_and_capacity). Each is ✓ (clean) or ✗ (missing). Disposition is **ACT** (four ✓ — commit the supported action) or **HOLD** (at least one ✗ — preserve the evidence hold and name the missing control). ACT rows typed "closing condition" are the closing-condition rows the selected approach requires for each supported blocker. Impact-control scores are inputs, never dispositions. R- references (e.g. CB-MA-2401-R473) are operative; E- references (e.g. CB-MA-2401-E439) are operating extracts that state no legal disposition.

## Register

| Key | Topic | Entity | Rev | Id | Op | Cur | App | Disposition | Action / missing control |
|---|---|---|---|---|---|---|---|---|---|
| CBP-001-01 | Charter authorization mismatch | ENT-001-1000/2000 | 2025.1 | ✗ | ✓ | ✗ | ✓ | **HOLD** | Identity: 1000/2000 collision, no approved crosswalk. Current: Feld E257 vs Ellison R983 |
| CBP-001-02 | Financial covenant breach | ENT-001-1001 | 2025.2 | ✓ | ✓ | ✓ | ✓ | ACT — disclosure | Result 13% (E738) vs 7% covenant (R158): disclose and price |
| CBP-001-03 | Permit transfer restriction | ENT-001-1002 | 2025.3 | ✓ | ✓ | ✓ | ✓ | ACT — closing condition | Blocks completion (R164); open and unresolved (E368) |
| CBP-001-04 | Revenue recognition exception | ENT-001-1003 | 2025.4 | ✓ | ✓ | ✓ | ✓ | ACT — closing condition | Blocks completion (R532); open and unresolved (E548) |
| CBP-001-05 | Most-favored-customer exposure | ENT-001-1004 | 2025.5 | ✓ | ✓ | ✓ | ✓ | ACT — closing condition | Exposure 18% (E921) vs 13% limit (R572): condition or priced exception |
| CBP-001-06 | Unreported security incident | ENT-001-1005 | 2025.6 | ✓ | ✓ | ✓ | ✓ | ACT — approval | Obtain Theo Laurent's approval (R990; E311 names the same approver) |
| CBP-001-07 | Claims-made insurance tail | ENT-001-1006 | 2025.7 | ✓ | ✓ | ✓ | ✓ | ACT — disclosure | Bound 2025-09-02 (E341) vs due 2025-08-05 (R611): disclose late binding |
| CBP-001-08 | Anti-assignment restriction | ENT-001-1007 | 2024.0→2025.1 | ✓ | ✓ | ✗ | ✓ | **HOLD** | Current: Flores E111 on superseded REV-2024.0 vs Delgado R293 on REV-2025.1 |
| CBP-001-09 | Open-source copyleft exposure | ENT-001-1008 | 2025.2 | ✓ | ✓ | ✓ | ✓ | ACT — closing condition | Blocks completion (R971); open and unresolved (E945) |
| CBP-001-10 | Sales-tax nexus gap | ENT-001-1009 | 2025.3 | ✓ | ✓ | ✓ | ✓ | ACT — closing condition | Delaware activity (E877) beyond Washoe-County authority (R710): condition or indemnity |
| CBP-001-11 | Change-of-control consent | ENT-001-1010 | 2025.4 | ✓ | ✓ | ✗ | ✗ | **HOLD** | Current: Hassan E439 vs Brooks R473. Approval: owner pending, inactive, capacity 0 |
| CBP-001-12 | Invention assignment defect | ENT-001-1011 | 2025.5 | ✓ | ✓ | ✗ | ✓ | **HOLD** | Current: Novak E278 vs Hassan R433 |

**Result: 8 ACT, 4 HOLD** — exactly the `helios-forge:scoped-evidence` outcome: commit 8 supported actions, preserve 4 evidence holds, and finish the latest supported action by 2026-09-03.

## Impact-control scores (inputs only; CB-DOC-001-097 population and per-key support records)

01=80 · 02=77 · 03=52 · 04=85 · 05=76 · 06=69 · 07=36 · 08=81 · 09=89 · 10=72 · 11=93 · 12=59

## Action and cure owners (current responsibility roster)

- CBP-001-01 — Elliot Mercer (active; next control 2026-09-03) — hold cure owner
- CBP-001-02 — Sofia Bennett (active; 2026-09-02)
- CBP-001-03 — Micah Sullivan (active; 2026-09-01)
- CBP-001-04 — Nora Chen (active; 2026-08-31)
- CBP-001-05 — Caleb Hassan (active; 2026-08-30)
- CBP-001-06 — Amara Patel (active; 2026-08-29)
- CBP-001-07 — Samuel Kim (active; 2026-08-28)
- CBP-001-08 — Talia Brooks (active; 2026-08-27) — hold cure owner
- CBP-001-09 — Adrian Mensah (active; 2026-08-26)
- CBP-001-10 — Farah Ibrahim (active; 2026-09-03)
- CBP-001-11 — Dominic Alvarez (pending approval and inactive; capacity 0; 2026-09-02) — must be activated or replaced before this key leaves hold
- CBP-001-12 — Leona Park (active; 2026-09-01) — hold cure owner

## Source anchors (native records CB-DOC-001-NNN)

- CBP-001-01: 001, 013, 025, 037, 049, 073
- CBP-001-02: 002, 014, 026, 038, 050
- CBP-001-03: 003, 015, 027, 039, 051
- CBP-001-04: 004, 016, 028, 040, 052, 064, 076
- CBP-001-05: 005, 017, 029, 041, 053, 065, 077, 089
- CBP-001-06: 006, 018, 030, 042, 054, 066, 090
- CBP-001-07: 007, 019, 031, 043, 055, 067, 079, 091
- CBP-001-08: 008, 020, 032, 044, 056, 068, 092
- CBP-001-09: 009, 021, 033, 045, 057, 069, 093
- CBP-001-10: 010, 022, 034, 046, 058, 070, 094
- CBP-001-11: 011, 023, 035, 047, 059, 071, 095
- CBP-001-12: 012, 024, 036, 048, 060, 072, 096

## Reliance limits

Synthetic CounselBench-100 source records; all people, entities, events, and amounts are fictitious; this register is not legal advice. No source record decides legal effect, selects among candidate responses, resolves another system's entity identity, or establishes that its cited revision is controlling; dispositions here rest only on the four-control reconciliation. Roster facts are current as of the 2026-09-04 matter date, and no external facts are assumed.
