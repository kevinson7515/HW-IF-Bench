# Aurora MDL Production — Working Position (close-the-loop)

To: Litigation team · Matter `CB-LD-2701` · Position date target: **2026-09-05**
From: Discovery audit · Approach: **`aurora-antitrust:scoped-evidence`** (AUTHORIZED)

## Bottom line

Aurora **cannot certify the full MDL production today**, and it should not represent that it can. The population splits cleanly into **6 records Aurora can act on now** and **6 records that must wait** for a specific control to be cured. The defensible course is scoped certification, not a blanket certification and not a blanket freeze.

- **Certify now (6):** CBP-031-02, 04, 06, 07, 08, 09 — all four controls (identity, authority, operations, approval/revision) are satisfied. Four of them carry a numeric/delivery discrepancy that must be **disclosed** in the certification, not asserted clean.
- **Hold (6):** CBP-031-01, 03, 05, 10, 11, 12 — each is missing at least one of the four controls. No representation may be made that these are complete until the missing control is cured.

## What Aurora can do now

1. **Adopt `scoped-evidence`.** It is AUTHORIZED — no additional approval is required, and it preserves the defensible record. Reject `shortcut` (certifying from production-log totals) as unsupported by the evidence, and do not escalate to `blanket-hold` (which would over-defer the 6 already-supported records and needs additional approval).
2. **Certify the 6 supported records**, disclosing the residual gaps: family separation 14% vs 11% (02); designation undercount 125/148 (06); production undercount 40/78 (07); wrong hold-delivery address (08); clawback completed late (09).
3. **Start the curable remediation now**, in priority order:
   - Activate the two pending owners — CBP-031-01 (Samuel Kim) and CBP-031-05 (Dominic Alvarez) — both "pending approval and inactive, capacity 0."
   - Re-key CBP-031-10 from the superseded REV-2024.2 to the later effective REV-2025.3.
   - Correct the wrong notice address on CBP-031-08 and CBP-031-10.
4. **Commit the Review Disposition Register and this note** (both under `output/`), then **close the loop in Slack** — reply in channel `C00000031`, thread `1760000031.000005` (the `005_pleadings_source_export.json` record); do **not** open a new top-level post. Re-open each changed provider record afterward so the recorded result (not just the request payload) is confirmed.

## What must wait

1. **Certification of the 6 held records** until the specific control is cured:
   - CBP-031-01 — pending owner; overlapping Bates count (180 vs 215).
   - CBP-031-03 — identity collision (ENT-1002/ENT-2002) plus blocked/open request-response mismatch.
   - CBP-031-05 — open collection-date inconsistency on the mobile chats, plus pending owner.
   - CBP-031-10 — superseded revision (REV-2024.2).
   - CBP-031-11 — identity collision (ENT-1010/ENT-2010) plus custodian-omission count (61 vs 98).
   - CBP-031-12 — pending privilege challenge (common-interest support gap, blocked/open).
2. **Any representation that the production is complete as a whole**, including a single "all 12 done" certification from log totals.
3. **Deciding the 6 genuinely ambiguous records by analogy to the clean ones** — the protocol forbids turning a similar name, a superseded revision, or a pending owner into proof.

## What evidence would change the answer

Each hold flips to "certifiable" only on the specific, traceable evidence below (owner named from the responsibility roster):

| Hold | Evidence that changes the disposition | Owner |
|---|---|---|
| CBP-031-01 | Active owner on CBP-031-01 **and** a single reconciled Bates figure (180 vs 215, R753). | Samuel Kim |
| CBP-031-03 | An approved crosswalk resolving the ENT-031-1002/ENT-031-2002 collision **and** closure of the open request-response mismatch (R694 / E452). | Adrian Mensah |
| CBP-031-05 | Reconciled collection dates for the chat export **and** an active owner (R821 / E407). | Dominic Alvarez |
| CBP-031-10 | Re-key to the current effective revision REV-2025.3 (or a controlling-order showing REV-2024.2 is operative) **and** the correct notice address. | Willa Novak |
| CBP-031-11 | An approved crosswalk resolving the ENT-031-1010/ENT-031-2010 collision **and** a reconciled custodian count (61 vs 98, R976). | Owen Delgado |
| CBP-031-12 | Resolution of the privilege/common-interest challenge (closure of the "blocks completion" / "open and unresolved" state, R908 / E253). | Priya Raman |

## Which gaps must be cured before certification

These are the blocking gaps — a count across the 6 holds. They are the minimum that must be cured before full production certification, and each already has an owner above.

- **2 identity collisions** (CBP-031-03, CBP-031-11) — no approved crosswalk resolves the shared display name / divergent domain and legal entity.
- **3 blocked operative authorities** (CBP-031-03, CBP-031-05, CBP-031-12) — "open … blocks completion."
- **3 open/unresolved current operations** (CBP-031-03, CBP-031-05, CBP-031-12).
- **2 pending/inactive owners** (CBP-031-01, CBP-031-05) — "pending approval and inactive; capacity 0."
- **1 superseded revision** (CBP-031-10) — REV-2024.2 vs the later effective REV-2025.3.

The remaining discrepancies (Bates overlap 180/215; undercounts 125/148 and 40/78; custodian 61/98; wrong delivery address on 08/10; late clawback on 09) are **disclosable** for the supported records, but should be cured in the same remediation pass to make the scoped certification fully defensible.

## Authority, cost, and timing

- `scoped-evidence` — AUTHORIZED, incremental cost $20,000, latest supported action completed by **2026-09-03** (ahead of the 2026-09-05 matter date).
- `shortcut` — UNSUPPORTED_BY_CURRENT_EVIDENCE (rejected).
- `blanket-hold` — ADDITIONAL_APPROVAL_REQUIRED, $29,600 (only if the team later decides to freeze everything; not recommended now).

## Limits

This position reconciles the four controls from the native exports and the impact population (`097_aurora_antitrust_impact_population.xlsx`). It does not decide legal effect or privilege on the merits, does not resolve any third party's entity identity, and assumes no external facts beyond the matter date. All people, entities, and amounts are fictitious; this is not legal advice.

Source anchors: `output/aurora_antitrust_review_disposition_register.md` (register); native records `CB-DOC-031-001 … CB-DOC-031-096`; impact population `097_aurora_antitrust_impact_population.xlsx`.
