# Arcadia Genomics, Inc. — Genomic Data Response Audit Closeout

Matter: CB-PR-3001 · Date: 2026-09-02 · Approach: `arcadia-genomics:scoped-evidence` (AUTHORIZED)

## Review Disposition Register (one row per portfolio key)

| Key | Subject | Disposition | Missing control |
|---|---|---|---|
| CBP-061-01 | Sensitive-Data Classification | Supported | — |
| CBP-061-02 | Notice-Practice Mismatch | Supported | — |
| CBP-061-03 | Retention Schedule Conflict | Supported | — |
| CBP-061-04 | Risk-Assessment Omission | Evidence hold | identity (similar name: shares R173/E104 with CBP-061-12) |
| CBP-061-05 | Processing-Purpose Gap | Supported | — |
| CBP-061-06 | Cross-Border Transfer Gap | Supported | — |
| CBP-061-07 | Incident-Notification Clock | Evidence hold | authority (pending owner: approval pending and inactive, capacity 0) |
| CBP-061-08 | Regulator Commitment Overdue | Evidence hold | revision (superseded: cited REV-2024.0 vs current REV-2025.1) |
| CBP-061-09 | Subprocessor Inventory Mismatch | Supported | — |
| CBP-061-10 | Identity-Verification Inconsistency | Supported | — |
| CBP-061-11 | Training Completion Gap | Supported | — |
| CBP-061-12 | Processor-Contract Omission | Evidence hold | identity (similar name: shares R173/E104 with CBP-061-04) |

## Review note

Selected approach: `arcadia-genomics:scoped-evidence` — complete supported access/deletion work and
escalate exact transfer gaps. Applied the identity, authority, current-operations, and revision test to
all twelve keys. Result: 8 supported actions, 4 evidence holds.

Evidence holds and missing controls: CBP-061-04 and CBP-061-12 share the authority reference
CB-PR-3001-R173 and event reference CB-PR-3001-E104 (similar-name collision); CBP-061-07 shows a pending
owner (approval pending and inactive, capacity 0); CBP-061-08 cites superseded revision REV-2024.0 where
REV-2025.1 is current.

Rejected alternatives: `arcadia-genomics:shortcut` (unsupported by current evidence — would discard the 4
unresolved constraints) and `arcadia-genomics:blanket-hold` (additional approval required — would freeze
the 8 supported records).

Limits: source exports are identity-crosswalk/counterrecord evidence only; they do not decide legal effect.
No external facts assumed beyond the matter date 2026-09-02.
