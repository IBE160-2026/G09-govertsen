# Reconciliation: Product Brief v3 → PRD

- **Input:** `.docs/planning-artifacts/briefs/PRODUCT_BRIEF.md` (v3, 2026-11-08)
- **Checked against:** `prd.md`, `addendum.md` (this folder)
- **Date:** 2026-11-08
- **Result:** Coverage is high. All 12 success criteria map to SM-1…SM-12, every rule (F1–F4, 1–14) keeps its ID, all 8 test files are carried over, and every scope and non-goal item appears. The gaps listed below are small. Most of the divergences are decisions documented after the brief was written, and the brief has not caught up with them yet.

## 1. Gaps (brief content dropped, weakened or contradicted)

### Medium

- **Open issues / comment not on the dashboard.**
  - Brief: "What the system shows per job" lists "Open issues and warnings", and Scope v1 lists "Dashboard with … open issues". Success criterion 1 requires *all* of these fields on the dashboard.
  - PRD: FR-23 lists the fields but leaves out Comment / issue description. FR-24 flags cover delay, revision mismatch, on hold and inspection, but not free-text issues. SM-1 is tied to FR-23, so criterion 1 is weakened.
  - Fix: add the comment / issue description, or an "open issue" indicator, to FR-23.
- **Long-term vision and business-effect measurement dropped.**
  - Brief: the Vision section gives the full pipeline (Engineering → … → Internal Assembly → **Final Approval**). It also lists "measuring business effects (less time on manual follow-up, fewer errors from outdated revisions) once baseline numbers are available".
  - PRD: §1 Vision covers only v1. §7.2 lists some later items (roles/Entra ID, inspection results, row approval, notifications). Business-effect measurement and the long-term pipeline are not mentioned anywhere, and there are no deferred secondary metrics.
  - This is intent the lecturer asked to be kept in the Vision (brief v2 change log).
- **Example file coverage of F1–F4 is inconsistent with the brief's test set.**
  - PRD FR-12 says "Each of F1–F4 is covered by an example file". The brief's test files, and PRD FR-27, include only `wrong-template.xlsx` (F2, F3).
  - No example file exists for F1 (not .xlsx / unreadable) or F4 (no job rows).
  - Fix: either add the files to FR-27 and the brief, or relax FR-12 to "example file or automated test".

### Low

- **"Send updated Excel" call to action weakened.**
  - Brief (Drawing revisions): PTS marks the job *"new revision — send updated Excel to supplier"*.
  - PRD: FR-3 and FR-24 have only a *New revision* flag. The reminder to act ("send file") is implied, not required. Worth keeping as label intent for UX.
- **`Not started` meaning shifted.**
  - Brief: "Sent to supplier, work not started".
  - PRD: FR-1 gives every new job `Not started` before any export, so a job that has never been sent looks the same as one that has. The PRD has no "not yet sent" state or flag.
- **W9 condition blurred by FR-20 and UJ-5.**
  - Brief rule 9: W9 applies whenever a newer export exists for the supplier, whether or not anything has been approved.
  - PRD FR-14 matches the brief. FR-20 adds "if the approved import came from a newer export, the other imports also get W9", which implies W9 depends on approval.
  - UJ-5 gives Monday's file W9 after Tuesday's "corrected file". A corrected file would normally reuse the same Export ID, so W9 would not apply.
  - Fix: align FR-20 and UJ-5 with rule 9.
- **Revision note `[ASSUMPTION]` silently resolved.**
  - Brief: marks the Revision note column behaviour as `[ASSUMPTION]`.
  - PRD: FR-10 states it as a firm requirement and does not list it in §11. Either confirm it, or keep the tag.

## 2. PRD ahead of brief (documented divergences; brief should be updated per project rule)

- **Manual update of supplier-reported fields (FR-28) with job history (glossary, NFR-1, NFR-2, SM-15).**
  - Brief: "Only after approval is the database updated". It gives the planner no way to change status by hand.
  - PRD: lets the planner change these fields directly, recorded in the job history (resolved in §10).
- **W14 extended to manual updates** (FR-14, FR-20). Brief rule 14 and success criterion 8 cover only another approved import.
- **Norwegian UI; supplier file stays English** (NFR-10, §10). The brief has no language requirement.
- **Text dates accepted** in `dd.mm.yyyy` and `yyyy-mm-dd` (FR-13 / R5). Brief: "valid date" only.
- **Empty expected completion date allowed** (FR-13, `[ASSUMPTION]`). The brief does not say.
- **Open job = any status other than `Completed`** (glossary, §10). The brief uses "open jobs" without defining it.
- **W12 status order fixed:** Not started → In production / On hold → Ready for inspection → Completed (FR-14, §10). The brief gives only an example.
- **Locked-column changes never applied** (FR-14, `[ASSUMPTION]`). The brief only says they give a warning.
- **Revision mismatch as a persistent dashboard flag** based on the last approved import, cleared by a later matching import (FR-24, `[ASSUMPTION]`). The brief defines mismatch only as an import warning.
- **Supplier management** (FR-4, `[ASSUMPTION]`): create and list suppliers, names unique, no delete while the supplier has jobs.
- **Supplier file details beyond the brief:**
  - editable columns pre-filled with current values (FR-8)
  - instructions sheet (FR-7)
  - sheet protection without password
  - red highlighting of missing conditional fields (FR-9)
  - no file created for a supplier with no open jobs (FR-6)
- **NFRs not in the brief:**
  - 5 MB upload limit
  - `.xlsm` rejected by F1
  - 200 rows in under 5 s
  - Chrome or Edge desktop only
  - upload retention rule
- **Job edit rules:** quantity cannot be set below completed quantity (FR-2). An import cannot be decided twice (FR-18).
- **Additional success metrics:**
  - SM-13 to SM-15
  - counter-metrics SM-C1 and SM-C2
  - "PTS does not plan production" non-goal (§6)
