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
6. **Approve or reject the whole import.** Only after approval is the database updated.
7. **Follow up** from the dashboard: jobs on hold, ready for inspection, delayed, or affected by a new drawing revision.

### Drawing revisions

Drawings themselves live outside PTS. When a new drawing revision is approved for production, the internal user places it in the shared folder with the supplier and informs the project manager and job owner by email, as today. In addition, the user **updates the current revision on the job in PTS manually**. PTS then marks the job as *"new revision — send updated Excel to supplier"*, and flags any later import that still reports the old revision.

PTS stores only the **current** revision of each job, not a revision history. The import log still shows which revision each supplier file reported.

## The Excel File

Each export is a fixed template with locked and editable columns.

### Locked columns (visible to the supplier, not to be changed)

| Column | Notes |
|---|---|
| Export ID | Unique per exported file |
| Export date | Date the file was generated |
| Job ID | |
| Drawing number | |
| Revision | Current revision at the time of export |
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
| Expected completion date | Valid date |
| Comment / issue description | Free text (required when On hold reason is `Other`) |

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

Every row in an uploaded file is checked against these rules.

### Rejected (the row is not imported and the reason is shown)

1. Production status is not one of the allowed values.
2. Status is `On hold` without a reason, or the reason is `Other` without a comment.
3. Status is `Ready for inspection` without an inspection type.
4. Completed quantity is not a whole number, is negative, or is greater than the ordered quantity.
5. Expected completion date is not a valid date.
6. Job ID does not exist in PTS, or belongs to a different supplier.

### Warning (the row is imported on approval, but flagged for the user)

7. **Revision mismatch:** the revision in the file differs from the job's current revision in PTS, meaning the supplier may be working from an outdated drawing.
8. **Outdated file:** a newer export exists for the same supplier.
9. **Unexpected change:** a locked column has been changed by the supplier.
10. **Delay:** expected completion date is later than the due date.
11. **Status moved backwards**, e.g. from `Completed` to `In production`.

### Import rules

- **Nothing is written to the database without approval.**
- An import is approved or rejected **as a whole**. Rejected rows are never imported, even when the import is approved.
- **Only one pending import per supplier at a time.** Uploading a new file while another import from the same supplier is waiting is blocked, with a message asking the user to approve or reject the pending import first.
- Every approved or rejected import is logged with date, file, user and result.

## Who This Serves

**Primary user in v1:**
- **Production planner** (one internal role). Creates jobs, exports and imports Excel files, approves imports, registers new drawing revisions, and follows up from the dashboard.

In practice several internal employees may use PTS, but v1 has **one internal user** to keep the system simple. **No login** in v1; the system records a fixed user name on every approval so the import log remains traceable.

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
8. Uploading a second file for a supplier with a pending import is blocked with a clear message.
9. From the dashboard alone, the user can find all jobs that are on hold, ready for inspection, delayed, or affected by a new revision.

### Test files

The repository includes example Excel files with expected results, used both in automated tests and by anyone trying the app:

| File | Content | Expected result |
|---|---|---|
| `valid.xlsx` | Correct updates for several jobs | All rows accepted, changes shown |
| `invalid-status.xlsx` | Unknown status, On hold without reason | Rows rejected with error messages |
| `revision-mismatch.xlsx` | Old revision for a job with a newer revision in PTS | Row flagged as revision mismatch |
| `missing-fields.xlsx` | Ready for inspection without type, invalid quantity | Rows rejected with error messages |
| `locked-field-changed.xlsx` | Supplier changed due date and description | Rows flagged as unexpected change |

## Scope

### In v1

- Job register: create, view and edit jobs, including registering a new drawing revision manually
- Excel export per supplier, using the fixed template
- Excel import with validation, change view, warnings and rejected rows
- Approval or rejection of a whole import, with an import log
- Dashboard with job status, open issues, delays, inspection requests and revision warnings
- Inspection **requests** from suppliers (before painting / final) shown on the dashboard
- Seed data and example Excel files with fictional data, so the app can be run and tried locally

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
