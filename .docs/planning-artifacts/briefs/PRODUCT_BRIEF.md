# Product Brief: Production Tracking System (PTS)

## Executive Summary

A mid-sized engineering and production company in Agder designs and delivers marine products for its customers. Production is carried out both internally and through external suppliers, such as machining and welding workshops.

The company needs a better way to track production jobs as they move from engineering and purchasing, through supplier production, inspection, and delivery, to internal assembly. Today, information is spread across Excel files, emails, and individual follow-ups, making it difficult to maintain a clear and reliable overview.

The Production Tracking System (PTS) will provide an internal web application for tracking this information. External suppliers exchange updates through controlled Excel files rather than accessing the company's internal systems directly, since a level of classified documentation adds another layer of complexity.

**All data in this project is fictional.** The case is based on a real type of company, but no real company data, drawings, or supplier information is stored in the repository.

## The Problem

The company may have many production jobs running at the same time, often involving several suppliers and internal departments.

A typical job moves through:

**Engineering → Supplier → Production → Inspection → Delivery → Internal Assembly**

At each stage, employees need to know the status, expected delivery date, inspection status, and whether any problems have occurred — for example, wrong measurements on a drawing, which must be captured by engineering and result in a new drawing revision.

When this information is managed through separate Excel files, emails, and manual follow-ups, it becomes difficult to know which information is current and accurate. Issues such as drawing problems, missing materials, production delays, or revision mismatches can also be hard to identify and follow up on.

The company also operates in a controlled IT environment, meaning external suppliers should not have direct access to internal systems or databases.

## The Solution

PTS gives the internal user one overview of production jobs and their current status, and a controlled way to exchange updates with suppliers through Excel.

### What the system shows per job

- Job ID
- Drawing number and current revision
- Description
- Quantity
- Supplier
- Production status (and On hold reason, if any)
- Inspection request (type), if any
- Completed quantity
- Due date and the supplier's expected completion date
- Open issues and warnings (delay, revision mismatch)

### The internal user's workflow

1. **Create jobs** in PTS with drawing number, revision, quantity, supplier and due date.
2. **Download an Excel file** for one supplier, containing that supplier's open jobs.
3. **Send the file to the supplier** by email or through a shared folder. This transfer happens outside PTS and is done manually.
4. **Receive the updated file** from the supplier (email or shared folder) and **upload it** to PTS.
5. **Review the import.** PTS validates every row and shows, per job, what changed compared to the database, which rows were rejected and why, and which rows carry warnings.
6. **Approve or reject the whole import.** Only after approval is the database updated with the file's contents.
7. **Follow up** from the dashboard: jobs on hold, ready for inspection, delayed, or affected by a new drawing revision.
8. **Record phone calls.** When a supplier phones in a change, the user records it as a **manual update** of the supplier-reported fields. Every manual update is stored in the job's history with date, user, old and new value.

A job **closes** automatically when its status becomes `Completed`. The user can also close a job by hand, for example when an order is cancelled, and reopen it. Only open jobs are included in supplier files.

**Language:** everything users and suppliers see is in Norwegian, including the Excel file's column names, values and instructions. This brief, the PRD and the code are in English. The Norwegian labels are listed in the PRD (§3.1).

### Drawing revisions

Drawings themselves live outside PTS. When a new drawing revision is approved for production, the internal user places it in the shared folder with the supplier and informs the project manager and job owner by email, as today. In addition, the user **updates the current revision on the job in PTS manually**. PTS then marks the job as *"new revision — send updated Excel to supplier"*, and flags any later import that still reports the old revision.

The new revision is marked clearly in three places:

- **Dashboard:** the job shows a visible *New revision* badge until the supplier has been sent an updated file.
- **Excel file:** in the next export to the supplier, the Revision cell of the job is highlighted and the Revision note column says `NEW REVISION`, so the supplier sees which drawings have changed.
- **Clearing the mark:** the dashboard badge is removed automatically when a new export for that supplier, containing the job, has been downloaded.

PTS stores only the **current** revision of each job, not a revision history. The import log still shows which revision each supplier file reported.

## The Excel File

Each export is a fixed template with locked and editable columns. The column names and values are shown in English here, and the file itself uses Norwegian labels.

### Locked columns (visible to the supplier, not to be changed)

| Column | Notes |
|---|---|
| Export ID | Unique per exported file |
| Export date | Date the file was generated |
| Job ID | |
| Drawing number | |
| Revision | Current revision at the time of export; highlighted when it changed since the previous export to this supplier |
| Revision note | `NEW REVISION` when the revision changed since the previous export to this supplier, otherwise empty `[ASSUMPTION]` |
| Description | |
| Quantity | Ordered quantity |
| Supplier | |
| Due date | The company's required date |

### Editable columns (filled in by the supplier)

| Column | Allowed values |
|---|---|
| Production status | `Not started`, `In production`, `On hold`, `Ready for inspection`, `Completed` |
| On hold reason | `Drawing issue`, `Missing material`, `Check requested`, `Other` (required when status is `On hold`) |
| Inspection type | `Before painting`, `Final` (required when status is `Ready for inspection`) |
| Completed quantity | Whole number from 0 to ordered quantity |
| Expected completion date | Valid date (real Excel date, or text as `dd.mm.yyyy` or `yyyy-mm-dd`) |
| Comment / issue description | Free text (required when On hold reason is `Other`) |

**Dropdowns:** Production status, On hold reason and Inspection type are dropdown lists in the Excel file (Excel data validation), so the supplier picks from the allowed values instead of typing them. Completed quantity and Expected completion date use Excel data validation for whole numbers and dates. Because suppliers can still paste values or use other spreadsheet programs, PTS validates every row on import regardless of the dropdowns.

Internal-only information, such as inspection results and delivery status, is not included in the file.

### Production statuses

| Status | Meaning |
|---|---|
| `Not started` | Sent to supplier, work not started |
| `In production` | Supplier is working on the job |
| `On hold` | Stopped — the supplier must give a reason, e.g. a drawing issue, missing material, or a request for the company to come and check something |
| `Ready for inspection` | Supplier requests inspection, either before painting (surface treatment) or final inspection |
| `Completed` | Production finished |

## Validation Rules

Every uploaded file is first checked as a whole, then every row is checked against the rules below.

### File rejected (nothing is imported and the reason is shown)

- **F1.** The file is not an `.xlsx` file, or cannot be read.
- **F2.** One or more required columns from the template are missing or renamed.
- **F3.** The Export ID is missing or was not generated by PTS.
- **F4.** The file contains no job rows.

### Row rejected (the row is not imported and the reason is shown)

1. Production status is not one of the allowed values.
2. Status is `On hold` without a reason, or the reason is `Other` without a comment.
3. Status is `Ready for inspection` without an inspection type.
4. Completed quantity is not a whole number, is negative, or is greater than the ordered quantity.
5. Expected completion date is not a valid date.
6. Job ID does not exist in PTS, or belongs to a different supplier.
7. **Duplicate Job ID:** the same Job ID appears more than once in the file. All rows with that Job ID are rejected.

### Warning (the row is imported on approval, but flagged for the user)

8. **Revision mismatch:** the revision in the file differs from the job's current revision in PTS, meaning the supplier may be working from an outdated drawing.
9. **Outdated file:** a newer export exists for the same supplier.
10. **Unexpected change:** a locked column has been changed by the supplier.
11. **Delay:** expected completion date is later than the due date.
12. **Status moved backwards**, e.g. from `Completed` to `In production`.
13. **Missing job:** an open job that was included in the export is missing from the uploaded file. The job is left unchanged.
14. **Job changed by another import:** after the export, another approved import changed a field of this job, and this file changes the same field to a different value.
15. **Conflict with manual update:** after the export, the user changed a field of this job by a manual update, and the file's value for that field differs from it. The planner clears this up with the supplier before deciding.

### Import rules

- **Nothing is written to the database without approval.**
- An import is approved or rejected **as a whole**. Rejected rows are never imported, even when the import is approved.
- **Only cells the supplier changed are applied.** A cell whose value equals the value in the export is never applied, so an old, untouched value cannot undo newer information, such as a manual update. When the supplier did change a cell, the file wins on approval, also over a manual update. Warnings 14 and 15 show such conflicts before approval.
- **Several pending imports are allowed**, also for the same supplier. Every pending import is always shown against the current database, so the user never approves against stale values.
- Every approved or rejected import is logged with date, file, user and result.

## Who This Serves

**Primary user in v1:**
- **Production planner** (one internal role). Creates jobs, exports and imports Excel files, approves imports, registers new drawing revisions, and follows up from the dashboard.

In practice several internal employees may use PTS, but v1 has **one internal user** to keep the system simple. **No login** in v1; the system records a fixed user name on every approval, rejection and manual update so the import log and job history remain traceable.

**Indirect user:**
- **External suppliers** never access PTS. They only receive and return the Excel file.

**Later versions:** project and engineering personnel, and quality and inspection personnel, as separate roles.

Success means the internal user can quickly answer a basic question: *"Where is this job, and is there anything we need to act on?"*

## Success Criteria

All criteria below can be checked by testing v1.

1. A job can be created and is shown on the dashboard with all fields listed under "What the system shows per job".
2. An Excel file can be downloaded for one supplier, containing only that supplier's open jobs, with a unique Export ID and the current revision of each job.
3. An uploaded file is validated, and every rejected row is shown with an understandable error message that names the rule that was broken.
4. Before approval, the user can see exactly what changed per job compared to the database.
5. **No import ever changes the database before it is approved** — verified by tests.
6. A file reporting an older revision than the job's current revision is flagged as a revision mismatch.
7. A job whose expected completion date is later than its due date is flagged as delayed on the dashboard.
8. When two pending imports contain the same job and one is approved, the other import shows the updated values, and is flagged as *job changed by another import* where it would overwrite them.
9. From the dashboard alone, the user can find all jobs that are on hold, ready for inspection, delayed, or affected by a new revision.
10. In an exported file, Production status, On hold reason and Inspection type are dropdown lists containing only the allowed values.
11. A job with a new revision is marked in the dashboard and in the next export to its supplier, and the dashboard mark disappears once that export has been downloaded.
12. A file that is not a valid PTS export (wrong file type, missing columns, unknown Export ID or no rows) is rejected as a whole with a clear message.

### Test files

The repository includes example Excel files with expected results, used both in automated tests and by anyone trying the app:

| File | Content | Expected result |
|---|---|---|
| `valid.xlsx` | Correct updates for several jobs | All rows accepted, changes shown |
| `invalid-status.xlsx` | Unknown status, On hold without reason | Rows rejected with error messages |
| `revision-mismatch.xlsx` | Old revision for a job with a newer revision in PTS | Row flagged as revision mismatch |
| `missing-fields.xlsx` | Ready for inspection without type, invalid quantity | Rows rejected with error messages |
| `locked-field-changed.xlsx` | Supplier changed due date and description | Rows flagged as unexpected change |
| `duplicate-job-id.xlsx` | The same Job ID on two rows | Both rows rejected as duplicates |
| `missing-job.xlsx` | One exported open job removed from the file | Warning: missing job |
| `wrong-template.xlsx` | A required column renamed and Export ID removed | Whole file rejected |

## Scope

### In v1

- Job register: create, view and edit jobs, register a new drawing revision manually, record manual updates with a job history, and close and reopen jobs
- Excel export per supplier, using the fixed template with dropdown lists and new revisions marked
- Excel import with file checks, row validation, change view, warnings and rejected rows
- Approval or rejection of a whole import, with several pending imports allowed and an import log
- Dashboard with job status, open issues, delays, inspection requests and a clear new-revision mark
- Inspection **requests** from suppliers (before painting / final) shown on the dashboard
- Seed data and example Excel files with fictional data, so the app can be run and tried locally
- A Norwegian user interface and supplier file

The PRD divides v1 into **Core** (create job → export → import → change view → approve → dashboard), which must be finished and stable first, and **Extension** (manual updates, closing jobs, supplier management and some warnings).

### Out of scope for v1

- Recording inspection results, delivery, internal assembly and final approval
- Multiple roles and login
- Revision history
- Approving or rejecting individual rows in an import
- Sending email or integrating with shared folders — file transfer is manual
- Replacing the company's ERP, PDM, PLM, MES, or quality systems
- Storing engineering drawings as the authoritative source
- Automatically approving technical or quality decisions
- Giving suppliers direct access to the internal network
- Becoming a complete warehouse, logistics, or financial system

PTS is an information and tracking tool that helps the internal user maintain an accurate overview and identify problems early — not a system of record for engineering or finance.

## Vision

The long-term vision is a practical production tracking system that follows a job through the company's wider production process:

**Engineering → Supplier Production → Inspection → Delivery → Internal Assembly → Final Approval**

Possible later steps:

- Several internal users with **Windows / Microsoft Entra ID sign-in**, and separate roles for project, engineering, production and quality personnel
- Recording inspection results, delivery and internal assembly
- Automatic notification of project manager and job owner when a drawing revision changes
- Approving individual rows in an import
- Measuring business effects, such as less time spent on manual follow-up with suppliers and fewer errors caused by outdated drawing revisions, once baseline numbers are available

The system should remain simple and focused: helping people make better decisions by providing the right production information at the right time, without duplicating the company's existing ERP, PDM, or quality systems.

## Change Log

### Version 4 — 2026-11-08

Updated while writing the PRD (`.docs/planning-artifacts/prds/prd-PTS-2026-11-08/prd.md`, §0.1), so that the brief and the PRD agree.

| Change | Reason |
|---|---|
| The user can record manual updates of supplier-reported fields, stored in a job history (workflow step 8) | Suppliers often phone in changes |
| New warning 15, *Conflict with manual update*. Warning 14 redefined as *Job changed by another import* | Conflicts between a returned file and newer information must be visible so they can be cleared up |
| Only cells the supplier changed are applied. Where the supplier did change a cell, the file wins | Untouched, old values must not undo newer information |
| Jobs close automatically when `Completed`, and can be closed and reopened by hand | Cancelled or wrongly created jobs need an exit |
| Everything users and suppliers see is in Norwegian | Users and suppliers are Norwegian |
| Text dates accepted in `dd.mm.yyyy` and `yyyy-mm-dd` | Suppliers type dates in different ways |
| v1 divided into Core and Extension | Lecturer feedback: finish the core flow first |
| Success criterion 8 reworded to match warning 14 | Consistency |

### Version 3 — 2026-11-08

| Change | Reason |
|---|---|
| Production status, On hold reason and Inspection type are dropdown lists in the Excel file; quantity and date use Excel data validation. PTS still validates every row | Fewer typing errors from suppliers |
| Added file-level checks (F1–F4), a duplicate Job ID rule (7) and a missing job warning (13); warnings renumbered 8–14 | Validation rules had to cover whole files and the whole export, not only single rows |
| New revisions are marked in the dashboard and in the next Excel export (highlighted cell and Revision note column); the dashboard mark is cleared when that export has been downloaded | The revision warning had to be visible to both the internal user and the supplier |
| Several pending imports are now allowed. Approving one recalculates the change view of other pending imports with the same jobs and flags them (warning 14), so the last approved import wins | One pending import per supplier blocked normal work when suppliers sent several files |
| Success criterion 8 rewritten and criteria 10–12 added; three new example test files | Keep the new rules testable |

### Version 2 — 2026-11-07

Updated after feedback from the IBE160 lecturer (2026-10-06) on version 1 (commit `cb4be4a`).

| Change | Reason (feedback) |
|---|---|
| Success criteria rewritten as nine testable, functional criteria; business targets with placeholders moved to the Vision | Placeholder business goals could not be measured in the course |
| Added the Excel template with locked and editable columns, production statuses, On hold reasons and inspection types | The import is the core of the app and needed concrete rules |
| Added validation rules: six that reject a row and five that give a warning, plus import rules | Revision mismatch and unexpected change had to be defined |
| Defined how revision mismatches arise: the user registers a new revision manually, and PTS stores only the current revision | Same as above |
| Added a rule allowing only one pending import per supplier, and approval of whole imports | Conflicts between two imports for the same job had to be described |
| Narrowed v1 to one internal user (production planner) with no login; Windows / Entra ID sign-in moved to the Vision | Users, roles and login had to be decided for v1 |
| Narrowed v1 to the core flow; inspection results, delivery and internal assembly moved out of scope | Scope risk for the semester |
| Clarified that file transfer (email or shared folder) happens outside PTS | "Sending" Excel files should mean downloading a file, not sending email |
| Described the internal user's workflow step by step | The Solution section should describe the user experience |
| Stated that all data is fictional, and added five example test files with expected results | Security and testability |

### Version 1 — commit `cb4be4a`

First version of the product brief.
