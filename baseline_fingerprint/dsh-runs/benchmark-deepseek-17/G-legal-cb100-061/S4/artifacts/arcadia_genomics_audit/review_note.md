# Arcadia Genomics Response Audit — Review Note

**Matter:** CB-PR-3001 — Arcadia genomic data response audit
**Position date:** 2026-09-02 (matter date)

## Selected approach

`arcadia-genomics:scoped-evidence` (AUTHORIZED). Complete the 8 supported access/deletion
actions, escalate the exact transfer gap, and preserve evidence holds for the four records
missing a control. Latest supported action finishes by 2026-09-01.

## Supported actions (8)

CBP-061-01, -02, -03, -04, -05, -10, -11, -12. All four controls (immutable identity,
operative authority, current operations, effective approval/revision) reconcile cleanly.
Anchors: CB-DOC-061-001…012, 013…024, 025…036, 037…048 (per-key +12 spacing across the
identity/operative/current/approval records).

## Evidence holds (4)

1. **CBP-061-06 — Cross-Border Transfer Gap.** Missing control: operative authority. The
   operative record limits transfer authorization to the California Privacy Protection Agency,
   so the overseas research transfer has no in-scope authority. Cure: a transfer mechanism with
   jurisdiction beyond California. Anchors: CB-DOC-061-006, -018, -030, -042, -054, -066, -078, -090.
2. **CBP-061-07 — Incident-Notification Clock.** Missing control: approval. Responsibility
   roster is `pending approval and inactive; capacity 0`. Cure: an approved, active owner.
   Anchors: CB-DOC-061-007, -019, -031, -043, -055, -067, -079, -091.
3. **CBP-061-08 — Regulator Commitment Overdue.** Missing control: effective revision.
   Operations cite REV-2024.0; REV-2025.1 is the later effective revision. Cure: re-baseline
   to REV-2025.1. Anchors: CB-DOC-061-008, -020, -032, -044, -056, -068, -080, -092.
4. **CBP-061-09 — Subprocessor Inventory Mismatch.** Missing control: immutable identity.
   ENT-061-1008 vs ENT-061-2008 share a display name with no approved crosswalk. Cure: an
   approved crosswalk resolving the collision. Anchors: CB-DOC-061-009, -021, -033, -045, -057, -069, -081, -093.

## Alternatives (rejected)

- `arcadia-genomics:shortcut` — UNSUPPORTED_BY_CURRENT_EVIDENCE (deletes matched names and
  discloses unverified research data).
- `arcadia-genomics:blanket-hold` — ADDITIONAL_APPROVAL_REQUIRED (freezes all 12, including
  the 8 already supported).

## Limits

No external facts assumed beyond the 2026-09-02 matter date. The impact-population workbook
(097_arcadia_genomics_impact_population.xlsx) is empty and contributes no control scores; the
disposition rests on the 96 source exports. Local register/note committed and read back; the
external matter system (Slack thread) was not opened.
