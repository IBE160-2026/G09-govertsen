# Response to the lecturer's feedback on the PRD

Draft answers to the two reflection questions in `tilbakemelding-prd.md` (§7), dated 2026-11-25. Passages in **[Radmila: …]** are things only the project owner can confirm or should put in her own words.

## 1. How did you arrive at "a supplier-changed cell wins over a manual update" (FR-28), and which alternatives did you consider and reject?

**What was decided in PRD v1.** The rule came from a requirement the project owner stated on 2026-11-08: a returned file that disagrees with a manual update must be flagged so it can be cleared up with the supplier (decision log `.memlog.md`). To make that workable we moved to a per-cell model: only cells the supplier changed compared with the export are applied, and an untouched cell never overwrites newer data. Where the supplier did change a cell, the file won, and warning W15 was the only guard. The reason given at the time was simplicity, and that an old, untouched value must not undo a phone call. **[Radmila: confirm that this is how you remember the reasoning.]**

**What we found later.** The decision log does not record alternatives, so v1 did not show that any were weighed. In the review of v1, and again when we tried the rule on concrete values, we saw the weakness: a supplier-changed cell could overwrite a date the planner had entered by hand, and the only protection was a warning she might not act on. The PRD itself called it an "accepted risk".

**Alternatives we weighed in v2:**

| Alternative | Outcome |
|---|---|
| The file always wins, including untouched cells | Rejected. An old value in the file would undo a phone call without anyone noticing. |
| The file wins when the supplier changed the cell, with only warning W15 (the v1 rule) | Rejected. It overwrites a manual value, and the planner can only reject the whole import. |
| The planner can only reject the whole import | Kept as a fallback. Too blunt, because the other rows in the file are fine. |
| **The planner chooses per conflicting field** (chosen) | Accepted. Nothing is preselected, and Approve stays disabled until every conflict is decided. It follows the thesis of the PRD: trust in the data, and nothing changes without the planner seeing it. |

An untouched cell keeps the PTS value and shows the warning only as information, because asking about something the supplier did not touch would only create noise.

**[Radmila: add whether you also considered "the PTS value always wins" and why it was not an option. If you did not, leave it out.]**

## 2. How did you check that the rules W8–W15 are consistent?

**Honestly: in v1 the check was too weak.** The draft was written with AI help and reviewed against the quality rubric (`review-rubric.md`) and a structure and prose review. We did not try the E/D/F values on concrete examples, and the lecturer found that W14 was defined differently in FR-14, FR-15, FR-20, FR-28 and the addendum.

**What we did in v2:**
- **One definition in one place.** The exported value (E), the current value (D) and the file value (F) give five cases in a single table (FR-15a). The other requirements, the addendum and the brief point to it instead of repeating it.
- **Concrete examples as test consequences.** For instance E = empty, D = 20.11.2026 (manual update), F = empty is *kept with W15*, and the same with F = 21.11.2026 is a conflict the planner decides. They are written into FR-15a, and FR-27b requires a scenario test for every case.
- **Consistency checks.** After each rewrite we searched the PRD, addendum, brief and Excel templates for old terms and wrong references, and checked the example data against the templates.
- **An independent review** (`bmad-review`, adversarial and edge-case lenses). It found a real hole: F5 did not stop a second file from an export that was already approved, so a conflict could occur in Core, where we had said it cannot. F5 is now extended and checked again at approval.

**What is still not verified.** The rules are checked on paper. They are not implemented, so the scenario tests in FR-27b have not been run. **[Radmila: keep or soften this paragraph.]**
