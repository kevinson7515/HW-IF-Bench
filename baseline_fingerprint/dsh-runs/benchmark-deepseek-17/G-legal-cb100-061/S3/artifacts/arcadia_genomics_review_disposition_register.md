# Review Disposition Register — CB-PR-3001 (Arcadia genomic data response audit)

Matter date: 2026-09-02. Portfolio: `cb100-061-arcadia-genomics`. One row per portfolio key.

**Selected approach:** `arcadia-genomics:scoped-evidence` (Authority: AUTHORIZED).
Reconciled the four controls per key — immutable identity, operative authority, current operations, and effective approval/revision. A supported action requires all four controls; otherwise the key is preserved on an evidence hold with the missing control stated.

| Portfolio key | Subject | Immutable entity | Revision (ref → cur) | Disposition | Missing control (if hold) |
|---|---|---|---|---|---|
| CBP-061-01 | Sensitive-Data Classification | ENT-061-1000 | REV-2025.1 → REV-2025.1 | Supported | — |
| CBP-061-02 | Notice-Practice Mismatch | ENT-061-1001 | REV-2025.2 → REV-2025.2 | Supported | — |
| CBP-061-03 | Retention Schedule Conflict | ENT-061-1002 | REV-2025.3 → REV-2025.3 | Supported | — |
| CBP-061-04 | Risk-Assessment Omission | ENT-061-1003 | REV-2025.4 → REV-2025.4 | Supported | — |
| CBP-061-05 | Processing-Purpose Gap | ENT-061-1004 | REV-2025.5 → REV-2025.5 | Supported | — |
| CBP-061-06 | Cross-Border Transfer Gap | ENT-061-1005 | REV-2025.6 → REV-2025.6 | Supported | — |
| CBP-061-07 | Incident-Notification Clock | ENT-061-1006 | REV-2025.7 → REV-2025.7 | Evidence hold | Effective approval — pending owner |
| CBP-061-08 | Regulator Commitment Overdue | ENT-061-1007 | REV-2024.0 → REV-2025.1 | Evidence hold | Effective revision — superseded |
| CBP-061-09 | Subprocessor Inventory Mismatch | ENT-061-1008 | REV-2025.2 → REV-2025.2 | Evidence hold | Immutable identity — collision |
| CBP-061-10 | Identity-Verification Inconsistency | ENT-061-1009 | REV-2025.3 → REV-2025.3 | Supported | — |
| CBP-061-11 | Training Completion Gap | ENT-061-1010 | REV-2025.4 → REV-2025.4 | Supported | — |
| CBP-061-12 | Processor-Contract Omission | ENT-061-1011 | REV-2025.5 → REV-2025.5 | Evidence hold | Operative authority — duplicated reference |

# Review note

**Selected approach.** `arcadia-genomics:scoped-evidence` — complete supported access and deletion work and escalate exact transfer gaps (Authority: AUTHORIZED). Outcome: commit 8 supported actions, preserve 4 evidence holds, and finish the latest supported action by 2026-09-01. Incremental cost $15,600.

**Supported actions (8).** CBP-061-01 (Sensitive-Data Classification), CBP-061-02 (Notice-Practice Mismatch), CBP-061-03 (Retention Schedule Conflict), CBP-061-04 (Risk-Assessment Omission), CBP-061-05 (Processing-Purpose Gap), CBP-061-06 (Cross-Border Transfer Gap), CBP-061-10 (Identity-Verification Inconsistency), CBP-061-11 (Training Completion Gap). Each reconciles all four controls: identity resolves to a single entity ("the nearby alias is excluded"), operative authority states a governing requirement (R-code), current operations show a completed/occurred/receipt/certification state or a clearly identified open gap, and approval is active with an effective (non-superseded) revision.

**Evidence holds (4), with the missing control.**

1. CBP-061-07 — Incident-Notification Clock. Missing control: **effective approval**. The responsibility roster names Isaac Romero with "Status is pending approval and inactive; remaining matter capacity is 0" (043_notices_consents_source_export.eml). A pending owner is not proof of approval.
2. CBP-061-08 — Regulator Commitment Overdue. Missing control: **effective revision**. Operative authority cites REV-2024.0 while REV-2025.1 is the later effective revision ("Operations cites REV-2024.0, but REV-2025.1 is the later effective revision", 020_vendor_reviews_source_export.csv). A superseded revision is not proof.
3. CBP-061-09 — Subprocessor Inventory Mismatch. Missing control: **immutable identity**. The identity crosswalk associates CBP-061-09 with both ENT-061-1008 and ENT-061-2008; "the domain and legal-entity fields disagree. No approved crosswalk revision resolves the collision" (009_processing_records_source_export.md). A similar name is not proof.
4. CBP-061-12 — Processor-Contract Omission. Missing control: **operative authority**. Its authority (R173) and event (E104) references duplicate CBP-061-04's references (024_vendor_reviews_source_export.pdf, 036_consumer_requests_source_export.csv; compare 016 and 028 for CBP-061-04). The legal basis cannot be uniquely established for this key.

**Source anchors.** Identity crosswalk: 001–012 (01_data_inventory, 02_processing_records). Operative authority: 013–024 (02_processing_records, 03_vendor_reviews). Current operations: 025–036 (04_security_incidents, 05_consumer_requests). Approval and capacity: 037–048 (05_consumer_requests, 06_notices_consents). Supporting: correspondence 049–060, financial/population support 061–072, chronology and custody 073–084, independent counterrecords 085–096, impact population 097_arcadia_genomics_impact_population.xlsx.

**Alternatives.** `arcadia-genomics:shortcut` — REJECTED (Authority: UNSUPPORTED_BY_CURRENT_EVIDENCE). `arcadia-genomics:blanket-hold` — REJECTED (Authority: ADDITIONAL_APPROVAL_REQUIRED).

**Limits.** This review decides the disposition of the twelve portfolio keys only. It does not decide legal effect, select a response for any other matter, resolve another system's entity identity, or establish a cited revision as controlling. The impact-control scores are inputs, not dispositions. Matter date is 2026-09-02; no external facts are assumed.
