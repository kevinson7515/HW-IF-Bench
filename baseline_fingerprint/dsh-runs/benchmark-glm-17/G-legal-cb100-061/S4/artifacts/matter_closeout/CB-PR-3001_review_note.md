# Review Note — CB-PR-3001 (Arcadia Genomics, Inc.) Genomic-Data Response Audit

Matter date: 2026-09-02. Client Arcadia Genomics, Inc.; counterparty North Coast Sequencing Network. This note accompanies the Review Disposition Register at `matter_closeout/CB-PR-3001_review_disposition_register.md`, which is the system of record for the one-row-per-portfolio-key dispositions.

## Selected approach

`arcadia-genomics:scoped-evidence` — complete the supported access and deletion work and escalate the exact transfer gaps. Authority: AUTHORIZED under the approach protocol in CB-DOC-061-089. Incremental cost: $15,600. Completion target for the latest supported action: 2026-09-01. The alternatives `arcadia-genomics:shortcut` ($0, UNSUPPORTED_BY_CURRENT_EVIDENCE) and `arcadia-genomics:blanket-hold` ($22,800, ADDITIONAL_APPROVAL_REQUIRED) were not selected.

## Method

The 96 source exports across folders 01–12 were parsed and joined on portfolio key (CBP-061-01 through CBP-061-12); each key carries exactly eight format variants. Each key's four control records were identified by evidence role and native-record content:

1. Immutable identity — an approved crosswalk revision maps the portfolio key to one immutable entity without collision.
2. Operative authority — a current operative record (CB-PR-3001-R###) states the controlling requirement and the effective revision.
3. Current operations — an operating extract (CB-PR-3001-E###) cites the same effective revision with facts consistent with the operative authority.
4. Effective approval — the responsibility roster shows active status with remaining matter capacity above zero.

## Supported actions (8)

| Key | Subject | Effective revision | Operative / operations refs | Approval record |
|---|---|---|---|---|
| CBP-061-01 | Sensitive-data classification | REV-2025.1 | R870 (CB-DOC-061-013) / E674 (025) | 037 — Henry Cho, active, capacity 4 |
| CBP-061-02 | Notice-practice mismatch | REV-2025.2 | R888 (014) / E728 (026) | 038 — Maya Ellison, active, capacity 1 |
| CBP-061-03 | Retention schedule conflict | REV-2025.3 | R844 (015) / E567 (027) | 039 — Jonas Feld, active, capacity 5 |
| CBP-061-04 | Risk-assessment omission | REV-2025.4 | R173 (016) / E104 (028) | 040 — Willa Novak, active, capacity 3 |
| CBP-061-05 | Processing-purpose gap | REV-2025.5 | R422 (017) / E754 (029) | 041 — Owen Delgado, active, capacity 4 |
| CBP-061-06 | Cross-border transfer gap | REV-2025.6 | R637 (018) / E449 (030) | 042 — Priya Raman, active, capacity 4 |
| CBP-061-10 | Identity-verification inconsistency | REV-2025.3 | R266 (022) / E798 (034) | 046 — Mei Whitaker, active, capacity 5 |
| CBP-061-12 | Processor-contract omission | REV-2025.5 | R173 (024) / E104 (036) | 048 — Lena Varga, active, capacity 5 |

All four controls pass for these keys. For CBP-061-06 the operative authority is limited to the California Privacy Protection Agency and the operating extract places the activity in California; the transfer gap is escalated as an exact gap within that scope rather than treated as resolved.

## Evidence holds (4)

CBP-061-07 (incident-notification clock, ENT-061-1006): the responsibility roster shows "pending approval and inactive" with remaining matter capacity 0 (CB-DOC-061-043). Effective approval fails; no response step is taken.

CBP-061-08 (regulator commitment overdue, ENT-061-1007): the operating extract cites superseded REV-2024.0 while the operative authority states REV-2025.1 is the later effective revision (CB-DOC-061-032 vs 020). The approver named in operations (Talia Brooks) also differs from the approver the operative authority requires (Caleb Hassan). Revision and approval controls fail.

CBP-061-09 (subprocessor inventory mismatch): the crosswalk maps CBP-061-09 to both ENT-061-1008 and ENT-061-2008 with disagreeing domain and legal-entity fields, and no approved crosswalk revision resolves the collision (CB-DOC-061-009). Identity control fails.

CBP-061-11 (training completion gap, ENT-061-1010): the operative authority states a population of 216 records (CB-DOC-061-023) while the operating extract states the certification covers 190 records (CB-DOC-061-035). Current-operations control fails on unreconciled facts.

Each hold key's response row carries an identity or legal-basis hold and takes no disposition.

## Source anchors

- Approach protocol with candidate approaches and completion route: `attached_files/task_11/12_remediation/089_remediation_source_export.md`
- Impact population (input only, not a disposition): `attached_files/task_11/12_remediation/097_arcadia_genomics_impact_population.xlsx`
- Control records per key: the identity, operative-authority, current-operations, and approval records listed in the register, drawn from the 96 exports in `attached_files/task_11/` folders 01–12.

## Alternatives considered and rejected

- `arcadia-genomics:shortcut` — create an unsupported same-day disposition for all 12 records, discarding the 4 unresolved evidence constraints. Rejected: UNSUPPORTED_BY_CURRENT_EVIDENCE; it uses one source without completing the controlling joins and turns similar names, superseded revisions, and pending owners into proof.
- `arcadia-genomics:blanket-hold` — defer all 12 records to 2026-09-05. Rejected: ADDITIONAL_APPROVAL_REQUIRED, and it defers 8 records already supported by current evidence.

## Limits

- Each source record's reliance limits apply: no single record decides legal effect, selects among candidate responses, resolves another system's entity identity, or establishes that its cited revision is controlling. Dispositions rest on the join across each key's four control records.
- Impact-control scores from the population export are inputs, not dispositions.
- No external facts are assumed beyond the records and the matter date 2026-09-02.
- The Slack completion route named in the approach protocol (channel `C00000061`, thread `1760000061.000005`) has no corresponding tool in this session and was not executed; the register and note are committed and re-read to confirm the recorded content.
- Synthetic CounselBench-100 data; not legal advice.
