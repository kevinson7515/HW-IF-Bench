# Review Disposition Register — Matter CB-PR-3001

- **Matter:** CB-PR-3001 — Arcadia genomic data response audit
- **Client:** Arcadia Genomics, Inc.
- **Counterparty:** North Coast Sequencing Network
- **Matter date:** 2026-09-02
- **Population:** `cb100-061-arcadia-genomics` — twelve portfolio keys, CBP-061-01 through CBP-061-12
- **Selected approach:** `arcadia-genomics:scoped-evidence` (AUTHORIZED) — 8 supported actions, 4 evidence holds, latest supported action finished by 2026-09-01, incremental cost $15,600
- **Controls tested per key:** immutable identity, operative authority, current operations, effective approval/revision. A supported action requires all four; any failure preserves an evidence hold stating the missing control. A similar name, a superseded revision, or a pending owner is not proof.

This register is the system of record for the matter: one row per portfolio key. Control columns read identity / operative authority / current operations / approval. Anchors are the CB-DOC-061 identifiers of each key's identity, operative-authority, current-operations, and approval records.

| Portfolio key | Record subject | Immutable entity | Current revision | Controls (identity / authority / operations / approval) | Disposition | Missing control / hold basis | Control-record anchors |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CBP-061-01 | Sensitive-Data Classification | ENT-061-1000 | REV-2025.1 | Pass / Pass / Pass / Pass — Henry Cho, active, capacity 4, next internal control 2026-09-01 | Supported action | None — all four controls reconcile | 001, 013, 025, 037 |
| CBP-061-02 | Notice-Practice Mismatch | ENT-061-1001 | REV-2025.2 | Pass / Pass / Pass / Pass — Maya Ellison, active, capacity 1, next internal control 2026-08-31 | Supported action | None — all four controls reconcile | 002, 014, 026, 038 |
| CBP-061-03 | Retention Schedule Conflict | ENT-061-1002 | REV-2025.3 | Pass / Pass / Pass / Pass — Jonas Feld, active, capacity 5, next internal control 2026-08-30 | Supported action | None — all four controls reconcile | 003, 015, 027, 039 |
| CBP-061-04 | Risk-Assessment Omission | ENT-061-1003 | REV-2025.4 | Pass / Pass / Pass / Pass — Willa Novak, active, capacity 3, next internal control 2026-08-29 | Supported action | None — all four controls reconcile | 004, 016, 028, 040 |
| CBP-061-05 | Processing-Purpose Gap | ENT-061-1004 | REV-2025.5 | Pass / Pass / Pass / Pass — Owen Delgado, active, capacity 4, next internal control 2026-08-28 | Supported action | None — all four controls reconcile | 005, 017, 029, 041 |
| CBP-061-06 | Cross-Border Transfer Gap | ENT-061-1005 | REV-2025.6 | Pass / Pass / Pass / Pass — Priya Raman, active, capacity 4, next internal control 2026-08-27 | Supported action | None — all four controls reconcile | 006, 018, 030, 042 |
| CBP-061-07 | Incident-Notification Clock | ENT-061-1006 | REV-2025.7 | Pass / Pass / Pass / **Fail** — Isaac Romero, pending approval and inactive, capacity 0 | Evidence hold | Approval/capacity control: the named owner is pending approval and inactive with zero remaining matter capacity; a pending owner is not proof | 007, 019, 031, 043 |
| CBP-061-08 | Regulator Commitment Overdue | ENT-061-1007 | REV-2025.1 — every record for this key cites superseded REV-2024.0 | **Fail** / **Fail** / **Fail** / **Fail** — Nadine Flores, active, capacity 2; the record itself cites REV-2024.0 | Evidence hold | Revision control: all four control records carry referenced revision REV-2024.0 while REV-2025.1 is the later effective revision; the approval also names Talia Brooks where the operative authority requires Caleb Hassan. A superseded revision is not proof | 008, 020, 032, 044 |
| CBP-061-09 | Subprocessor Inventory Mismatch | ENT-061-1008 and ENT-061-2008 (collision) | REV-2025.2 | **Fail** / Pass / Pass / Pass — Rafael Okafor, active, capacity 6 | Evidence hold | Identity control: the portfolio key maps to both ENT-061-1008 and ENT-061-2008; the display name is shared while the domain and legal-entity fields disagree, and no approved crosswalk revision resolves the collision. A similar name is not proof | 009, 021, 033, 045 |
| CBP-061-10 | Identity-Verification Inconsistency | ENT-061-1009 | REV-2025.3 | Pass / Pass / Pass / Pass — Mei Whitaker, active, capacity 5, next internal control 2026-09-01 | Supported action | None — all four controls reconcile | 010, 022, 034, 046 |
| CBP-061-11 | Training Completion Gap | ENT-061-1010 | REV-2025.4 | Pass / Pass / **Fail** / Pass — Theo Laurent, active, capacity 1 | Evidence hold | Current-operations control: the current-state certification covers 190 records under CB-PR-3001-E378 while the operative authority sets the population at 216 records under CB-PR-3001-R334; the current state does not reconcile with the operative population | 011, 023, 035, 047 |
| CBP-061-12 | Processor-Contract Omission | ENT-061-1011 | REV-2025.5 | Pass / Pass / Pass / Pass — Lena Varga, active, capacity 5, next internal control 2026-08-30 | Supported action | None — all four controls reconcile | 012, 024, 036, 048 |

Totals: 8 supported actions (CBP-061-01, -02, -03, -04, -05, -06, -10, -12) and 4 evidence holds (CBP-061-07, -08, -09, -11).

## Hold anchors (verbatim from the re-opened provider records)

- **CBP-061-07** — `06_notices_consents/043_notices_consents_source_export.eml` (CB-DOC-061-043): "The current responsibility roster names Isaac Romero for CBP-061-07. Status is pending approval and inactive; remaining matter capacity is 0."
- **CBP-061-08** — `03_vendor_reviews/020_vendor_reviews_source_export.csv` (CB-DOC-061-020): "regulator commitment overdue approval must come from Caleb Hassan under CB-PR-3001-R607. Operations cites REV-2024.0, but REV-2025.1 is the later effective revision." The same superseded citation (referenced REV-2024.0, current REV-2025.1) appears in CB-DOC-061-008 (`01_data_inventory/008_data_inventory_source_export.pdf`), CB-DOC-061-032 (`04_security_incidents/032_security_incidents_source_export.pdf`), and CB-DOC-061-044 (`06_notices_consents/044_notices_consents_source_export.csv`); the impact population workbook also records source revision REV-2024.0 for this key.
- **CBP-061-09** — `02_processing_records/009_processing_records_source_export.md` (CB-DOC-061-009): "Portfolio key CBP-061-09 is associated with both ENT-061-1008 and ENT-061-2008. The display name is shared, while the domain and legal-entity fields disagree. No approved crosswalk revision resolves the collision."
- **CBP-061-11** — `05_consumer_requests/035_consumer_requests_source_export.eml` (CB-DOC-061-035): "the training completion gap certification covers 190 records under CB-PR-3001-E378"; `03_vendor_reviews/023_vendor_reviews_source_export.html` (CB-DOC-061-023): "the training completion gap population is 216 records under CB-PR-3001-R334"; `08_retention_deletion/059_retention_deletion_source_export.eml` (CB-DOC-061-059) records both figures and resolves neither.

## Closeout verification

This register and the review note are committed as the matter work-product in `matter_closeout/`. Every changed record was re-opened after writing: both files were re-read from disk, all 96 source exports were re-parsed, and each register row was re-checked against the re-opened provider records, including the four hold anchors quoted above. The recorded results match the review findings. The latest next internal control date among the eight supported keys is 2026-09-01 (CBP-061-01 and CBP-061-10), consistent with finishing the latest supported action by 2026-09-01.

The established completion route is a reply in Slack channel `C00000061`, thread `1760000061.000005` (005_data_inventory_source_export.json), used only after this register and the review note are committed; no new top-level post is opened. No Slack-capable tool is available in this review environment, so the thread reply remains to be posted through that route by the channel operator.
