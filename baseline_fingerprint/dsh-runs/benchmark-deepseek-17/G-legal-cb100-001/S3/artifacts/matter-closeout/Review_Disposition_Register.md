# Review Disposition Register — CB-MA-2401 Project Daybreak (Helios Forge)

System of record: `cb100-001-helios-forge`. One row per portfolio key. Matter date 2026-09-04.
Selected approach: `helios-forge:scoped-evidence` (AUTHORIZED).

| Portfolio key | Concern | Immutable entity | Revision | Disposition | Missing control (holds) / closing condition (supported) |
|---|---|---|---|---|---|
| CBP-001-01 | Charter authorization mismatch | ENT-001-1000 (collides with ENT-001-2000) | REV-2025.1 | **Evidence hold** | Identity collision unresolved; approval owner disputed (Jonas Feld E257 vs Maya Ellison R983) |
| CBP-001-02 | Financial covenant breach | ENT-001-1001 | REV-2025.2 | Supported — closing condition | Cure or waive breach: result 13% exceeds threshold 7% (E738 / R158) |
| CBP-001-03 | Permit transfer restriction | ENT-001-1002 | REV-2025.3 | Supported — closing condition | Obtain permit-transfer consent; open item blocks completion (E368 / R164) |
| CBP-001-04 | Revenue recognition exception | ENT-001-1003 | REV-2025.4 | Supported — closing condition | Cure open/unresolved revenue recognition exception (E548 / R532) |
| CBP-001-05 | Most-favored-customer exposure | ENT-001-1004 | REV-2025.5 | Supported — closing condition | Resolve MFC exposure: result 18% exceeds threshold 13% (E921 / R572) |
| CBP-001-06 | Unreported security incident | ENT-001-1005 | REV-2025.6 | Supported — closing condition | Complete incident review/report; approver consistent (Theo Laurent, E311 / R990) |
| CBP-001-07 | Claims-made insurance tail | ENT-001-1006 | REV-2025.7 | Supported — closing condition | Procure/confirm tail; due 2025-08-05, event completed 2025-09-02 (E341 / R611) |
| CBP-001-08 | Anti-assignment restriction | ENT-001-1007 | REV-2024.0 (current REV-2025.1) | **Evidence hold** | Superseded revision: operations cite REV-2024.0, REV-2025.1 is the later effective revision (R293) |
| CBP-001-09 | Open-source copyleft exposure | ENT-001-1008 | REV-2025.2 | Supported — closing condition | Clear open/unresolved copyleft; blocks completion (E945 / R971) |
| CBP-001-10 | Sales-tax nexus gap | ENT-001-1009 | REV-2025.3 | Supported — closing condition | Resolve nexus scope: activity asserted in Delaware (E877) vs authority limited to Washoe County, Nevada (R710) |
| CBP-001-11 | Change-of-control consent | ENT-001-1010 | REV-2025.4 | **Evidence hold** | Approval owner disputed (Caleb Hassan E439 vs Talia Brooks R473) |
| CBP-001-12 | Invention assignment defect | ENT-001-1011 | REV-2025.5 | **Evidence hold** | Approval owner disputed (Willa Novak E278 vs Caleb Hassan R433) |

## Totals

- Supported actions (closing conditions): **8** — CBP-001-02, -03, -04, -05, -06, -07, -09, -10.
- Evidence holds: **4** — CBP-001-01, -08, -11, -12.

## Source anchors

- Identity: `identity_crosswalk` records (001/009/010/011/012; 002/003/004/005).
- Authority: `operative_authority` records (013, 017, 018, 019, 020, 021, 022, 023, 024).
- Operations: `current_operations` records (025–036).
- Approval/capacity: `approval_and_capacity` records (037–048).
- Impact population: `097_helios_forge_impact_population.xlsx` (12 keys; scores are inputs, not dispositions).
