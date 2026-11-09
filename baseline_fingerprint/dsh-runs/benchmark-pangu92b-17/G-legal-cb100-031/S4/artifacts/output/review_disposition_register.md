# Review Disposition Register — Aurora Pricing MDL (CB-LD-2701)

Matter date: 2026-09-05 · Portfolio: cb100-031-aurora-antitrust · System of record: this register (one row per portfolio key).

Test applied (scoped-evidence): a supported action requires all four controls —
immutable identity, operative authority, current operations, and effective approval/revision.
Any missing control preserves an evidence hold. Similar names, superseded revisions, and
inactive/pending owners are not treated as proof.

| Portfolio key | Disposition | Owner (current responsibility roster) | Identity | Authority | Current operations | Approval / revision | Missing control |
|---|---|---|---|---|---|---|---|
| CBP-031-01 | HOLD | Samuel Kim | OK (REV-2025.1) | OK (215 records, R753) | OK (180 records, E138) | FAIL — pending approval, inactive, capacity 0 | Effective approval |
| CBP-031-02 | SUPPORTED | Talia Brooks | OK (REV-2025.2) | OK (11% threshold, R682) | OK (14% result, E716) | OK — active, capacity 1 | — |
| CBP-031-03 | HOLD | Adrian Mensah | FAIL — collision ENT-031-1002 / ENT-031-2002 | FAIL — open, blocks completion (R694) | FAIL — open and unresolved (E452) | OK — active, capacity 4 | Resolved identity |
| CBP-031-04 | SUPPORTED | Farah Ibrahim | OK (REV-2025.4) | OK (due 2025-11-27, R665) | OK (completed 2025-11-25, E980) | OK — active, capacity 4 | — |
| CBP-031-05 | HOLD | Dominic Alvarez | OK (REV-2025.5) | FAIL — open, blocks completion (R821) | FAIL — open and unresolved (E407) | FAIL — pending approval, inactive, capacity 0 | Effective approval; open authority/current state |
| CBP-031-06 | SUPPORTED | Leona Park | OK (REV-2025.6) | OK (148 records, R246) | OK (125 records, E214) | OK — active, capacity 6 | — |
| CBP-031-07 | SUPPORTED | Henry Cho | OK (REV-2025.7) | OK (78 records, R626) | OK (40 records, E660) | OK — active, capacity 6 | — |
| CBP-031-08 | SUPPORTED | Maya Ellison | OK (REV-2025.1) | OK (notices email, R397) | OK (receipt email, E382) | OK — active, capacity 1 | — |
| CBP-031-09 | SUPPORTED | Jonas Feld | OK (REV-2025.2) | OK (due 2025-03-31, R664) | OK (completed 2025-05-12, E503) | OK — active, capacity 1 | — |
| CBP-031-10 | HOLD | Willa Novak | OK (REV-2025.3) | OK (R537; cites REV-2024.2 vs REV-2025.3) | FAIL — operating extract cites superseded REV-2024.2 | OK — active, capacity 4 | Current revision |
| CBP-031-11 | HOLD | Owen Delgado | FAIL — collision ENT-031-1010 / ENT-031-2010 | OK (98 records, R976) | OK (61 records, E151) | OK — active, capacity 3 | Resolved identity |
| CBP-031-12 | HOLD | Priya Raman | OK (REV-2025.5) | FAIL — open, blocks completion (R908) | FAIL — open and unresolved (E253) | OK — active, capacity 1 | Open authority/current state |

## Source anchors (record IDs)

Per key N (01–12): identity `CB-DOC-031-0N`, authority `CB-DOC-031-0(N+12)`,
current operations `CB-DOC-031-0(N+24)`, approval/capacity `CB-DOC-031-0(N+36)`,
correspondence `CB-DOC-031-0(N+48)`.

- CBP-031-01: 001 / 013 / 025 / 037 / 049
- CBP-031-02: 002 / 014 / 026 / 038 / 050
- CBP-031-03: 003 / 015 / 027 / 039 / 051
- CBP-031-04: 004 / 016 / 028 / 040 / 052
- CBP-031-05: 005 / 017 / 029 / 041 / 053
- CBP-031-06: 006 / 018 / 030 / 042 / 054
- CBP-031-07: 007 / 019 / 031 / 043 / 055
- CBP-031-08: 008 / 020 / 032 / 044 / 056
- CBP-031-09: 009 / 021 / 033 / 045 / 057
- CBP-031-10: 010 / 022 / 034 / 046 / 058
- CBP-031-11: 011 / 023 / 035 / 047 / 059
- CBP-031-12: 012 / 024 / 036 / 048 / 060

## Summary

- Supported (commit): 6 — CBP-031-02, 04, 06, 07, 08, 09.
- Evidence holds (preserve): 6 — CBP-031-01, 03, 05, 10, 11, 12.
- Latest supported action control date: CBP-031-02 = 2026-09-03 (meets the 2026-09-03 deadline).