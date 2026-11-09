# Review Note — Arcadia genomics data response audit (CB-PR-3001)

**Matter:** CB-PR-3001 — Arcadia Genomics, Inc.
**Portfolio:** `cb100-061-arcadia-genomics` (12 portfolio keys, CBP-061-01 … CBP-061-12)
**Matter date:** 2026-09-02
**Selected approach:** `arcadia-genomics:scoped-evidence` (AUTHORIZED, incremental cost $15,600)

## Selected approach

The production does not identify the selected approach; I select **`arcadia-genomics:scoped-evidence`**.
It is the only AUTHORIZED option: complete the supported access and deletion work, escalate the
exact transfer gaps, and preserve an evidence hold wherever one of the four controls is missing.
I reject `arcadia-genomics:shortcut` (`UNSUPPORTED_BY_CURRENT_EVIDENCE` — it discards the four
unresolved evidence constraints and manufactures a same-day disposition) and
`arcadia-genomics:blanket-hold` (`ADDITIONAL_APPROVAL_REQUIRED` — it freezes all 12 records,
including the 8 already supported by current evidence).

## Supported actions (8)

All four controls reconcile clean for these eight keys. Each commits a supported access/deletion
response row:

- **CBP-061-01** Sensitive-data classification — disclose completion 2025-09-17 vs due 2025-08-24.
- **CBP-061-02** Notice-practice mismatch — receipt used `notices-arcadia_genomics_inc@example.test`, matching the operative directive.
- **CBP-061-03** Retention schedule conflict — open conflict is escalated within the supported access/deletion work.
- **CBP-061-04** Risk-assessment omission — open omission is escalated within the supported access/deletion work.
- **CBP-061-05** Processing-purpose gap — open gap is escalated within the supported access/deletion work.
- **CBP-061-10** Identity-verification inconsistency — open inconsistency is escalated within the supported access/deletion work.
- **CBP-061-11** Training completion gap — disclose certification 190 records vs population 216.
- **CBP-061-12** Processor-contract omission — open omission is escalated within the supported access/deletion work.

## Evidence holds (4) — missing control named

- **CBP-061-06 — Cross-border transfer gap.** Missing **operative authority**: the cross-border
  transfer authority is limited to the California Privacy Protection Agency, so the overseas
  research-transfer component cannot be completed and must be escalated as an exact transfer gap.
- **CBP-061-07 — Incident-notification clock.** Missing **effective approval**: the responsibility
  roster names Isaac Romero but the status is `pending approval and inactive; remaining matter
  capacity is 0` (a pending owner, not proof).
- **CBP-061-08 — Regulator commitment overdue.** Missing **effective revision**: operations cite
  REV-2024.0, but REV-2025.1 is the later effective revision (a superseded revision, not proof).
- **CBP-061-09 — Subprocessor inventory mismatch.** Missing **immutable identity**: the key is
  associated with both ENT-061-1008 and ENT-061-2008 and no approved crosswalk resolves the
  collision (a similar name, not proof); operative authority and current operations are also open.

## Source anchors

Control records CB-DOC-061-001 … -048 (identity 001-012, operative authority 013-024, current
operations 025-036, approval/capacity 037-048); corroborating correspondence 049-060, financial/
population support 061-072, chronology/custody 073-084, and independent counterrecords 085-096.

Hold anchors: CBP-061-06 → -006, -018, -030, -042, -054, -066; CBP-061-07 → -007, -019, -031, -043,
-055, -067; CBP-061-08 → -008, -020, -032, -044, -056, -068; CBP-061-09 → -009, -021, -033, -045,
-057, -069.

## Alternatives

- `arcadia-genomics:shortcut` ($0) — rejected: `UNSUPPORTED_BY_CURRENT_EVIDENCE`; it discards the
  four unresolved evidence constraints.
- `arcadia-genomics:blanket-hold` ($22,800) — rejected: `ADDITIONAL_APPROVAL_REQUIRED`; it defers
  the 8 already-supported records along with the 4 holds.

## Limits

Impact-control scores (01=81 · 02=55 · 03=37 · 04=53 · 05=79 · 06=76 · 07=72 · 08=44 · 09=58 ·
10=89 · 11=70 · 12=46) are inputs, not dispositions. All records are synthetic CounselBench-100
material; no external facts are assumed, and the matter date is 2026-09-02. The register and this
note are the system of record (one row per portfolio key); completion is routed to Slack channel
`C00000061`, thread `1760000061.000005`, only after both are committed and the changed provider
records are re-opened to confirm the recorded result.
