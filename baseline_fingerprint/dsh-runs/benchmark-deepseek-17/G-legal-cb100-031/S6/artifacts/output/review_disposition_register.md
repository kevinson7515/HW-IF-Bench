# Review Disposition Register — CB-LD-2701 (Aurora pricing MDL discovery audit)

System of record: one row per portfolio key in `cb100-031-aurora-antitrust`.
Matter date: 2026-09-05. Prepared for the litigation team's next representation.

Four controls are reconciled per key before a disposition is chosen: **immutable identity**,
**operative authority**, **current operations**, and **effective approval/revision**. A supported
action requires all four controls. Otherwise the key is held and the missing control is stated.

| Portfolio key | Immutable entity | Subject | Disposition | Missing control(s) / gap | Owner (custodian → reviewer; pending owner) | Source anchor(s) |
|---|---|---|---|---|---|---|
| CBP-031-01 | ENT-031-1000 | Bates-range overlap | **HOLD** | Effective approval/revision — "pending approval and inactive; capacity 0"; Bates population disputed 180 (E138) vs 215 (R753) | Theo Laurent → Caleb Hassan; pending owner Samuel Kim | CB-DOC-031-037; CB-DOC-031-049 |
| CBP-031-02 | ENT-031-1001 | email-family separation | **SUPPORTED** | — | Amara Patel → Amara Patel | CB-DOC-031-002 / -014 / -026 / -038 |
| CBP-031-03 | ENT-031-1002 | request-response mismatch | **HOLD** | Identity collision (ENT-031-1002 vs ENT-031-2002); operative "blocks completion" (R694); current ops "open and unresolved" (E452) | Henry Cho → Samuel Kim | CB-DOC-031-003; -015; -027 |
| CBP-031-04 | ENT-031-1003 | metadata field loss | **SUPPORTED** | — | Talia Brooks → Nadine Flores | CB-DOC-031-004 / -016 / -028 / -040 |
| CBP-031-05 | ENT-031-1004 | collection-date inconsistency | **HOLD** | Operative "blocks completion" (R821); current ops "open and unresolved" (E407); approval "pending and inactive; capacity 0" | Jonas Feld → Rafael Okafor; pending owner Dominic Alvarez | CB-DOC-031-017; -029; -041 |
| CBP-031-06 | ENT-031-1005 | protective-order designation error | **SUPPORTED** | — | Farah Ibrahim → Farah Ibrahim | CB-DOC-031-006 / -018 / -030 / -042 |
| CBP-031-07 | ENT-031-1006 | production gap | **SUPPORTED** | — | Owen Delgado → Dominic Alvarez | CB-DOC-031-007 / -019 / -031 / -043 |
| CBP-031-08 | ENT-031-1007 | legal-hold delivery gap | **SUPPORTED** | — | Lena Varga → Leona Park | CB-DOC-031-008 / -020 / -032 / -044 |
| CBP-031-09 | ENT-031-1008 | clawback deadline | **SUPPORTED** | — | Samuel Kim → Henry Cho | CB-DOC-031-009 / -021 / -033 / -045 |
| CBP-031-10 | ENT-031-1009 | third-party subpoena deadline | **HOLD** | Operative/authority revision mismatch — operations cites REV-2024.2, but REV-2025.3 is the later effective revision | Maya Ellison → Maya Ellison | CB-DOC-031-010; -022 |
| CBP-031-11 | ENT-031-1010 | custodian omission | **HOLD** | Identity collision (ENT-031-1010 vs ENT-031-2010) | Adrian Mensah → Micah Sullivan | CB-DOC-031-011 |
| CBP-031-12 | ENT-031-1011 | common-interest support gap | **HOLD** | Operative "blocks completion" (R908); current ops "open and unresolved" (E253) | Willa Novak | CB-DOC-031-024; -036; -060 |

**Result: 6 supported actions, 6 evidence holds** — consistent with the authorized
`aurora-antitrust:scoped-evidence` approach.

Supported keys (certifiable now): CBP-031-02, -04, -06, -07, -08, -09.
Held keys (must be cured before certification): CBP-031-01, -03, -05, -10, -11, -12.

Provenance: CounselBench-100 synthetic source records; people, entities, and amounts are fictitious.
This register is a matter work-product record, not legal advice.
