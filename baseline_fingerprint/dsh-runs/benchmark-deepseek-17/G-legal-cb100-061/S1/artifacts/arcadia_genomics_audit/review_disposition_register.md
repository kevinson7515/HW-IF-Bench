# Arcadia Genomics — Review Disposition Register

**Matter:** CB-PR-3001 — Arcadia genomic data response audit (Arcadia Genomics, Inc.)
**Register date:** 2026-09-02 (matter date)
**Selected approach:** `arcadia-genomics:scoped-evidence` (AUTHORIZED)

One row per portfolio key in `cb100-061-arcadia-genomics`. A supported action requires all four
controls to reconcile: **immutable identity**, **operative authority**, **current operations**, and
**effective approval/revision**. Any key failing one control is preserved as an **evidence hold**
with the missing control named.

Legend — Id / Op / Cur / App = ✓ (clean) or ✗ (missing). Disposition is **SUPPORTED** (4 ✓) or
**EVIDENCE HOLD** (≥ 1 ✗). The impact-control score is an input, not a disposition.

| Key | Topic | Entity | Rev (cited) | Id | Op | Cur | App | Disposition | Missing control (named) |
|---|---|---|---|---|---|---|---|---|---|
| CBP-061-01 | Sensitive-Data Classification | ENT-061-1000 | 2025.1 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-02 | Notice-Practice Mismatch | ENT-061-1001 | 2025.2 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-03 | Retention Schedule Conflict | ENT-061-1002 | 2025.3 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-04 | Risk-Assessment Omission | ENT-061-1003 | 2025.4 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-05 | Processing-Purpose Gap | ENT-061-1004 | 2025.5 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-06 | Cross-Border Transfer Gap | ENT-061-1005 | 2025.6 | ✓ | ✗ | ✓ | ✓ | EVIDENCE HOLD | Operative authority — cross-border transfer authorization scope (California-only) |
| CBP-061-07 | Incident-Notification Clock | ENT-061-1006 | 2025.7 | ✓ | ✓ | ✓ | ✗ | EVIDENCE HOLD | Effective approval — owner pending approval and inactive (capacity 0) |
| CBP-061-08 | Regulator Commitment Overdue | ENT-061-1007 | 2024.0 (effective 2025.1) | ✓ | ✓ | ✓ | ✗ | EVIDENCE HOLD | Effective revision — superseded version (REV-2024.0 vs REV-2025.1) |
| CBP-061-09 | Subprocessor Inventory Mismatch | ENT-061-1008 / ENT-061-2008 | 2025.2 | ✗ | ✓ | ✓ | ✓ | EVIDENCE HOLD | Immutable identity — similar-name entity collision |
| CBP-061-10 | Identity-Verification Inconsistency | ENT-061-1009 | 2025.3 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-11 | Training Completion Gap | ENT-061-1010 | 2025.4 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |
| CBP-061-12 | Processor-Contract Omission | ENT-061-1011 | 2025.5 | ✓ | ✓ | ✓ | ✓ | SUPPORTED | — |

**Summary:** 8 SUPPORTED · 4 EVIDENCE HOLD.

Supported keys (commit access/deletion work now): CBP-061-01, -02, -03, -04, -05, -10, -11, -12.
Evidence-hold keys (preserve until the named gap is cured): CBP-061-06, -07, -08, -09.

Control-source anchors (the native record that establishes each disposition):

- **CBP-061-06** — operative authority `CB-DOC-061-018` (018_vendor_reviews_source_export.txt):
  "cross-border transfer gap authority is limited to California Privacy Protection Agency under
  CB-PR-3001-R637." The transfer authorization scope does not cover the cross-border transfer.
- **CBP-061-07** — approval/capacity `CB-DOC-061-043` (043_notices_consents_source_export.eml):
  "The current responsibility roster names Isaac Romero … Status is pending approval and inactive;
  remaining matter capacity is 0."
- **CBP-061-08** — operative authority `CB-DOC-061-020` (020_vendor_reviews_source_export.csv):
  "Operations cites REV-2024.0, but REV-2025.1 is the later effective revision." Identity
  (`CB-DOC-061-008`) and current operations (`CB-DOC-061-032`) cite the same superseded revision.
- **CBP-061-09** — identity crosswalk `CB-DOC-061-009` (009_processing_records_source_export.md):
  "Portfolio key CBP-061-09 is associated with both ENT-061-1008 and ENT-061-2008 … No approved
  crosswalk revision resolves the collision."
