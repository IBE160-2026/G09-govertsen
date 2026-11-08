# Reconciliation: PRD vs. Lecturer Feedback (2026-10-06)

- **Input:** IBE160 lecturer feedback on the product brief, dated 2026-10-06. It includes concrete suggestions and the part 1 grading criteria.
- **Checked against:** `prd.md` and `addendum.md` (draft, 2026-11-08).
- **Verdict:** the PRD addresses almost all of the lecturer's content points well: functional success criteria, a concrete rule list, one role with no login, the fixed template, fictional data and the pending-import conflict. The main gaps are in **prioritisation and scope control**, **examiner runnability details**, and **test data / repo layout**. These gaps weaken the downstream stories, and they map to criteria 1, 2, 6 and 7.

## 1. Concrete suggestions

| # | Lecturer suggestion | Addressed? | Where / comment |
|---|---|---|---|
| S1 | Replace placeholder business goals with functional, testable success criteria | Yes | §8 SM-1…SM-15, each linked to the FRs it validates |
| S2 | Make validation rules concrete: editable fields, valid statuses, what "revision mismatch" and "unexpected change" mean | Yes | §3 Glossary, FR-7, FR-12–14 (F1–F4, R1–R7, W8–W14) |
| S3 | Settle users, roles and login for v1 | Yes | §2.2, FR-22, §7.2 |
| S4 | Use fictional data only | Yes | NFR-8, §9, §0 |
| S5 | "Sending" Excel means downloading a file, not emailing it | Yes | FR-6, UJ-1, §6 |
| S6 | Describe what happens when two imports for the same job conflict | Yes | FR-19, FR-20, UJ-5, W14 |
| S7 | Say that an import never writes directly to the database | Yes | FR-17, NFR-1, addendum A2 (staging vs. job data) |
| S8 | **Finish the core flow before adding more** (create jobs → export → import → validation/changes → approve → dashboard) | **Partly** | §9 states it as a constraint, but nothing in §4/§7 marks which FRs are core and which extend it. Every FR has the same weight. See Gap 1. |
| S9 | v1 = Supplier → Production → Inspection request; one internal role; inspection results, delivery and assembly later | Yes | §7.1, §7.2 |
| S10 | A fixed template with locked and editable columns, and the rules written as a list in the PRD | Yes | FR-7, FR-9, addendum A1, `pts-supplier-template.xlsx` |
| S11 | Describe the internal user's steps and how deviations are shown | Yes | UJ-1…UJ-5, FR-15, addendum A3 |
| S12 | Choose one primary user and say which other groups use v1 | Yes | §2.2, §2.3 |
| S13 | List v1 functions as bullets and say whether inspection and delivery are included | Yes | §7.1, §7.2 |
| S14 | Make 4–5 example files with expected results (valid, invalid status, wrong revision, missing field, changed locked field) | Yes, with gaps | FR-27 lists 8 files. Coverage gaps are under Gap 3. |
| S15 | Keep the architecture simple: one web app and one local database | Partly | This is only a "hint" in addendum A2, not a constraint in §9 |
| S16 | Seed data and example Excel files so the examiner can try the import | Partly | FR-26, FR-27, NFR-3, SM-14. Reset and README content are not specified (Gap 2). |
| S17 | A dedicated folder for test files and fictional data, and a plan for secrets and docs | Partly | `testdata/` appears only as an "e.g." in A2. There is no plan for secrets, `.env` or stored uploads (Gap 4). |
| S18 | Sketch the dashboard and the import approval screen | Partly | The change view is sketched (A3). The dashboard has no sketch (Gap 5). |
| S19 | Update the brief in the repo so the history shows how the plan evolved | Partly | Brief v3 exists. But FR-28 (manual update + job history) and NFR-10 (Norwegian UI) are new in the PRD and are not in the brief. CLAUDE.md requires the brief/PRD chain to stay in sync (Gap 1b). |

## 2. Grading criteria (part 1)

| Criterion (weight) | Addressed? | Comment |
|---|---|---|
| 1. Process & AI steering (30%) | Yes, minor gap | Strong traceability: UJ → FR → SM, stable rule IDs shared by brief, PRD, stories and tests, an `[ASSUMPTION]` index. Weak point: the PRD adds scope that is not in the brief (FR-28, job history, Norwegian UI) without a brief update or a change note. That breaks the brief→PRD trace the examiner follows. |
| 2. Functionality & scope (20%) | **Partly** | The core flow is described. But v1 has grown since the brief, which the lecturer already rated "risk": manual updates, job history, recalculation of several pending imports (FR-20), W9/W12/W13/W14 and a revision-mismatch flag. There is no MoSCoW, release slice or cut line that says what to drop if time runs out. |
| 3. QA & testing (15%) | Yes, with gaps | NFR-7, FR-17 tests and the FR-27 table are good. There are no example files for F1, F4, R5, R6, W9, W11, W12 or W14, yet FR-12 claims "each of F1–F4 is covered by an example file". Expected results are per file, not per row, so tests cannot assert exact outcomes from the PRD. There is no test-level split (unit/integration/E2E) or demo test script. |
| 4. Design & UX (10%) | Partly | The UJs are vivid and the change view has a sketch. There is no dashboard sketch and no screen inventory or navigation map (dashboard, job register/form, import upload, pending list, change view, import log, job history). |
| 5. Code quality & architecture (10%) | Partly | "One web app + one local DB" is only a hint. It is not a constraint `bmad-architecture` must respect. |
| 6. README & runnability (10%) | Partly | NFR-3 and SM-14 exist. Missing: a seed/reset command (the demo state changes once the examiner approves `valid.xlsx`, and that changes the results of the other files through W9/W14); a default user name for FR-22; what the README must contain (setup, seed, where example files are, a walkthrough of UJ-1/UJ-2). |
| 7. Repo tidiness (5%) | Partly | There is no required folder layout for example files, seed data and uploaded files, and no rule that runtime uploads/DB are gitignored. `make_template.py` and the template live in the PRD folder, so their home in the codebase is undecided. A copy of the lecturer feedback (`tilbakemelding-product-brief.md`) sits in the repo root rather than under `.docs/`. |

## 3. Key gaps (prioritised)

1. **No priority tiers, so the core flow is not enforced (S8, criterion 2).** Mark each FR as *Core* or *Extension*. *Core* is the lecturer's chain: FR-1, FR-2, FR-4, FR-6–9, FR-11–13, FR-15, FR-17, FR-18, FR-21–23, FR-26, FR-27. *Extension* covers FR-3/FR-10/W8 (revisions), FR-19/20/W9/W14 (several pending imports), FR-28 + job history, W12/W13 and FR-25 counts. Add a cut line in §7, so `bmad-create-epics-and-stories` puts the core flow in epic 1 and the extensions later.
   - **1b.** Trace or backport the new scope (FR-28, job history, NFR-10) to the brief, or add a "changes since brief" note in §0.
2. **Examiner runnability is not specified enough (criterion 6).** Add an FR/NFR for a single seed/reset command that restores a known state, including the stored exports that the example files reference. State that example files are valid against a freshly seeded database. Give FR-22 a default user name. List the required README sections.
3. **The example-file set does not cover the rules NFR-7 requires (criterion 3).** Either add files (e.g. `not-xlsx.txt`/`.xlsm` for F1, `no-rows.xlsx` for F4, `bad-date.xlsx` for R5, `unknown-job.xlsx` for R6, `delay.xlsx` for W11, `status-backwards.xlsx` for W12) and multi-step scenarios for W9/W14, or reword FR-12 to say which rules are tested by unit tests without files. Specify per-row expected results (e.g. a sidecar expected-results file per example).
4. **Repo layout for test data, seed data and uploads is not a requirement (criterion 7).** Promote `testdata/` (example files + expected results) and the seed location from hint to requirement. Require runtime uploads and the local DB to be gitignored, and say that v1 has no secrets.
5. **Dashboard sketch is missing (criterion 4).** Add a low-fidelity dashboard sketch with flags and filter counts next to A3, plus a short screen list for `bmad-ux`.
