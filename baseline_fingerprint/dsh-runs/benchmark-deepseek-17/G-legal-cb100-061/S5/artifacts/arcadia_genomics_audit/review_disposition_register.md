# Review Disposition Register — Arcadia Genomics, Inc.

**Matter:** CB-PR-3001 — Arcadia genomic data response audit
**Portfolio:** `cb100-061-arcadia-genomics` (12 portfolio keys)
**Matter date:** 2026-09-02
**Selected approach:** `arcadia-genomics:scoped-evidence` (AUTHORIZED)

One row per portfolio key. For each key the four controls are reconciled before a
disposition is chosen: **immutable identity** (identity_crosswalk), **operative authority**
(operative_authority), **current operations** (current_operations), and **effective
approval/revision** (approval_and_capacity). A supported action requires all four controls;
otherwise the key is held with the exact missing control named.

Legend — Identity / Operative / Current / Approval = ✓ (clean) or ✗ (missing).
Disposition = **SUPPORTED** (4 ✓) or **EVIDENCE HOLD** (≥1 ✗). Impact-control score is an
input, not a disposition.

| Key | Topic | Entity | Rev | Id | Op | Cur | App | Disposition | Missing control (named) |
|---|---|---|---|---|---|---|---|---|---|
| CBP-061-01 | Sensitive-data classification | ENT-061-1000 | 2025.1 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (disclose completed 2025-09-17 vs due 2025-08-24) |
| CBP-061-02 | Notice-practice mismatch | ENT-061-1001 | 2025.2 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (receipt used `notices-arcadia_genomics_inc@example.test`) |
| CBP-061-03 | Retention schedule conflict | ENT-061-1002 | 2025.3 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (open conflict escalated within access/deletion work) |
| CBP-061-04 | Risk-assessment omission | ENT-061-1003 | 2025.4 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (open omission escalated within access/deletion work) |
| CBP-061-05 | Processing-purpose gap | ENT-061-1004 | 2025.5 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (open gap escalated within access/deletion work) |
| CBP-061-06 | Cross-border transfer gap | ENT-061-1005 | 2025.6 | ✓ | ✗ | ✓ | ✓ | **EVIDENCE HOLD** | Operative authority — cross-border transfer authority limited to CPPA (escalate transfer gap) |
| CBP-061-07 | Incident-notification clock | ENT-061-1006 | 2025.7 | ✓ | ✓ | ✓ | ✗ | **EVIDENCE HOLD** | Effective approval — pending owner |
| CBP-061-08 | Regulator commitment overdue | ENT-061-1007 | 2024.0→2025.1 | ✓ | ✗ | ✗ | ✓ | **EVIDENCE HOLD** | Effective revision — superseded revision |
| CBP-061-09 | Subprocessor inventory mismatch | ENT-061-1008/2008 | 2025.2 | ✗ | ✗ | ✗ | ✓ | **EVIDENCE HOLD** | Immutable identity — similar name (+ operative + current) |
| CBP-061-10 | Identity-verification inconsistency | ENT-061-1009 | 2025.3 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (open inconsistency escalated within access/deletion work) |
| CBP-061-11 | Training completion gap | ENT-061-1010 | 2025.4 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (disclose certification 190 records vs population 216) |
| CBP-061-12 | Processor-contract omission | ENT-061-1011 | 2025.5 | ✓ | ✓ | ✓ | ✓ | **SUPPORTED** | — (open omission escalated within access/deletion work) |

**Result: 8 SUPPORTED, 4 EVIDENCE HOLD.**

Impact-control scores (input only, from financial/population support records):
01=81 · 02=55 · 03=37 · 04=53 · 05=79 · 06=76 · 07=72 · 08=44 · 09=58 · 10=89 · 11=70 · 12=46.

The four holds and their source anchors:

- **CBP-061-06** — operative authority limited to CPPA (cross-border transfer gap).
  Anchors: CB-DOC-061-006, -018, -030, -042, -054, -066.
- **CBP-061-07** — "pending approval and inactive; remaining matter capacity is 0" (pending owner).
  Anchors: CB-DOC-061-007, -019, -031, -043, -055, -067.
- **CBP-061-08** — operations cite REV-2024.0, but REV-2025.1 is the later effective revision.
  Anchors: CB-DOC-061-008, -020, -032, -044, -056, -068.
- **CBP-061-09** — entity collision ENT-061-1008 vs ENT-061-2008; no approved crosswalk resolves it.
  Anchors: CB-DOC-061-009, -021, -033, -045, -057, -069.
