# Product Brief: Production Tracking System (PTS)

## Executive Summary

A mid-sized engineering and production company in Agder designs and delivers marine products for its customers. Production is carried out both internally and through external suppliers, such as machining and welding workshops.

The company needs a better way to track production jobs as they move from engineering and purchasing, through supplier production, inspection, and delivery, to internal assembly. Today, information is spread across Excel files, emails, and individual follow-ups, making it difficult to maintain a clear and reliable overview.

The Production Tracking System (PTS) will provide an internal web application for tracking this information. External suppliers will exchange updates through controlled Excel files rather than accessing the company's internal systems directly, since a level of classified documentation adds another layer of complexity.

## The Problem

The company may have many production jobs running at the same time, often involving several suppliers and internal departments.

A typical job moves through:

**Engineering → Supplier → Production → Inspection → Delivery → Internal Assembly**

At each stage, employees need to know the status, expected delivery date, inspection status, and whether any problems have occurred — for example, wrong measurements on a drawing, which must be captured by engineering and result in a new drawing revision.

When this information is managed through separate Excel files, emails, and manual follow-ups, it becomes difficult to know which information is current and accurate. Issues such as drawing problems, missing materials, production delays, or revision mismatches can also be hard to identify and follow up on.

The company also operates in a controlled IT environment, meaning external suppliers should not have direct access to internal systems or databases.

## The Solution

PTS will give employees and project engineers one internal overview of production jobs and their current status.

For each job, the system can show information such as:

- Job ID
- Drawing number and revision
- Description
- Quantity
- Supplier
- Production status
- Due date
- Inspection status
- Delivery status
- Open issues

Suppliers receive a controlled Excel file containing the jobs relevant to them. They can update defined fields — production status, completed quantity, inspection requests, and issues.

When the file is returned, the system validates the information, compares it with existing data, and shows the changes to an internal user. The database is only updated after the import has been reviewed and approved.

## What Makes This Different

PTS is designed around the practical needs of an engineering and production company rather than trying to become a complete ERP or production management system.

The key focus is the connection between internal production control and external suppliers: suppliers can provide production updates without direct access to the company's internal network or database, while the company gets a structured and controlled way to receive, validate, and approve those updates.

The system also helps identify issues such as invalid statuses, unexpected changes, and drawing revision mismatches — problems that are easy to miss in an Excel-and-email workflow.

## Who This Serves

**Primary users:**
- **Project and production personnel** need a quick overview of where jobs are and whether anything requires attention.
- **Engineering personnel** need to identify problems related to drawings, revisions, or production requirements.

**Secondary users:**
- **Quality and inspection personnel** need to see which jobs are ready for inspection and record inspection results.
- **External suppliers** need a simple way to provide production updates and report problems without accessing the company's internal systems.

Success means employees can quickly answer a basic question: *"Where is this job, and is there anything we need to act on?"*

## Success Criteria

**User success signals:**
- An employee can answer "where is this job, and is there anything to act on?" from the dashboard alone, without emailing or calling anyone — target: under 1 minute per job. *[target to confirm with users]*
- Internal reviewers can see exactly what changed in a supplier's Excel return before approving it, with zero unreviewed writes to the database.
- Drawing revision mismatches are flagged by the system before they cause a production error, not discovered after the fact.

**Business objectives:**
- Reduce time spent on manual status follow-up (email/phone) with suppliers and between departments by *[target, e.g. 50%]*. *[target to confirm with stakeholders]*
- Reduce production errors or rework caused by using an outdated drawing revision or status to *[target, e.g. near zero per quarter]*. *[target to confirm with stakeholders]*
- All supplier data imports are validated and require internal approval before reaching the database — 100% of imports, no exceptions.

*Note: the bracketed targets above are placeholders — replace with real numbers once baseline data (current follow-up time, current error rate) is available.*

## Scope

The first version covers **job tracking end to end through the supplier Excel exchange**: creating and viewing jobs, sending controlled Excel files to suppliers, validating and reviewing what comes back, and giving internal staff a single dashboard to see status and open issues. It does not touch drawings, quality decisions, or any other company system directly.

**Out of scope:**
- Replacing the company's ERP, PDM, PLM, MES, or quality systems
- Storing engineering drawings as the authoritative source
- Automatically approving technical or quality decisions
- Giving suppliers direct access to the internal network
- Becoming a complete warehouse, logistics, or financial system

PTS is primarily an information and tracking tool that helps employees maintain an accurate overview and identify problems early — not a system of record for engineering or finance.

## Vision

The long-term vision is a practical production tracking system that follows a job through the company's wider production process:

**Engineering → Supplier Production → Inspection → Delivery → Internal Assembly → Final Approval**

The system should give project, engineering, production, and quality personnel a shared view of progress and outstanding issues, without duplicating the company's existing ERP, PDM, or quality systems.

It should remain simple and focused: helping people make better decisions by providing the right production information at the right time.
