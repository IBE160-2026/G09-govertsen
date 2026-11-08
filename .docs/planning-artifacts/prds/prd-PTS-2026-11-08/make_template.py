"""Generate the PTS supplier Excel template (fictional example data) from product brief v3."""
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1]

STATUSES = ["Not started", "In production", "On hold", "Ready for inspection", "Completed"]
HOLD_REASONS = ["Drawing issue", "Missing material", "Check requested", "Other"]
INSPECTION_TYPES = ["Before painting", "Final"]

LOCKED = [
    ("Export ID", 20), ("Export date", 13), ("Job ID", 11), ("Drawing number", 16),
    ("Revision", 10), ("Revision note", 15), ("Description", 30), ("Quantity", 10),
    ("Supplier", 24), ("Due date", 13),
]
EDITABLE = [
    ("Production status", 21), ("On hold reason", 18), ("Inspection type", 17),
    ("Completed quantity", 12), ("Expected completion date", 14), ("Comment / issue description", 40),
]

EXPORT_ID = "EXP-20261108-0001"
EXPORT_DATE = date(2026, 11, 8)
SUPPLIER = "Supplier Alpha (fictional)"

# Fictional rows: (job, drawing, rev, new_rev, description, qty, due, status, reason, insp, done, expected, comment)
ROWS = [
    ("PTS-0001", "DRW-10001", "B", False, "Bracket, stainless steel", 12, date(2026, 12, 4), "In production", None, None, 4, date(2026, 12, 1), None),
    ("PTS-0002", "DRW-10002", "C", True, "Shaft housing, machined", 4, date(2026, 12, 11), "Not started", None, None, 0, None, None),
    ("PTS-0003", "DRW-10003", "A", False, "Welded frame, base", 2, date(2026, 11, 27), "On hold", "Missing material", None, 0, date(2026, 12, 9), None),
    ("PTS-0004", "DRW-10004", "A", False, "Cover plate", 20, date(2026, 11, 20), "Ready for inspection", None, "Before painting", 20, date(2026, 11, 19), None),
    ("PTS-0005", "DRW-10005", "D", False, "Flange, DN150", 8, date(2026, 12, 18), "Not started", None, None, 0, None, None),
]

GREY = PatternFill("solid", fgColor="E7E6E6")
HEAD_LOCKED = PatternFill("solid", fgColor="595959")
HEAD_EDIT = PatternFill("solid", fgColor="1F4E78")
EDIT = PatternFill("solid", fgColor="FFF2CC")
NEWREV = PatternFill("solid", fgColor="F8CBAD")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()
ws = wb.active
ws.title = "Jobs"

# Hidden list sheet feeding the dropdowns
lists = wb.create_sheet("Lists")
for col, (name, values) in enumerate(
    [("Production status", STATUSES), ("On hold reason", HOLD_REASONS), ("Inspection type", INSPECTION_TYPES)], start=1
):
    lists.cell(row=1, column=col, value=name).font = Font(bold=True)
    for i, v in enumerate(values, start=2):
        lists.cell(row=i, column=col, value=v)
lists.sheet_state = "hidden"
lists.protection.sheet = True

headers = LOCKED + EDITABLE
n_locked = len(LOCKED)
for c, (name, width) in enumerate(headers, start=1):
    cell = ws.cell(row=1, column=c, value=name)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = HEAD_LOCKED if c <= n_locked else HEAD_EDIT
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    cell.border = BORDER
    ws.column_dimensions[get_column_letter(c)].width = width
ws.row_dimensions[1].height = 42
ws.freeze_panes = "D2"

ws["F1"].comment = Comment("NEW REVISION = the drawing revision changed since the previous export to this supplier. Use the new drawing.", "PTS")
ws["K1"].comment = Comment("Pick from the list. On hold needs a reason; Ready for inspection needs an inspection type.", "PTS")
ws["L1"].comment = Comment("Required when status is On hold. 'Other' requires a comment.", "PTS")
ws["M1"].comment = Comment("Required when status is Ready for inspection.", "PTS")
ws["N1"].comment = Comment("Whole number from 0 to Quantity.", "PTS")

DATE_FMT = "yyyy-mm-dd"
for r, row in enumerate(ROWS, start=2):
    job, drw, rev, new_rev, desc, qty, due, status, reason, insp, done, expected, comment = row
    values = [EXPORT_ID, EXPORT_DATE, job, drw, rev, "NEW REVISION" if new_rev else None, desc, qty, SUPPLIER, due,
              status, reason, insp, done, expected, comment]
    for c, v in enumerate(values, start=1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.border = BORDER
        if c <= n_locked:
            cell.fill = GREY
            cell.protection = Protection(locked=True)
        else:
            cell.fill = EDIT
            cell.protection = Protection(locked=False)
        if isinstance(v, date) or c in (2, 10, 15):
            cell.number_format = DATE_FMT
    if new_rev:
        for col in ("E", "F"):
            ws[f"{col}{r}"].fill = NEWREV
            ws[f"{col}{r}"].font = Font(bold=True, color="9C0006")

last = len(ROWS) + 1


def add_dv(dv, col):
    dv.error_style = "stop"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(f"{col}2:{col}{last}")


add_dv(DataValidation(type="list", formula1=f"=Lists!$A$2:$A${len(STATUSES)+1}", allow_blank=False,
                      errorTitle="Invalid status", error="Pick a status from the list."), "K")
add_dv(DataValidation(type="list", formula1=f"=Lists!$B$2:$B${len(HOLD_REASONS)+1}", allow_blank=True,
                      errorTitle="Invalid reason", error="Pick an On hold reason from the list."), "L")
add_dv(DataValidation(type="list", formula1=f"=Lists!$C$2:$C${len(INSPECTION_TYPES)+1}", allow_blank=True,
                      errorTitle="Invalid inspection type", error="Pick an inspection type from the list."), "M")
add_dv(DataValidation(type="custom", formula1="AND(ISNUMBER(N2),N2=INT(N2),N2>=0,N2<=H2)", allow_blank=True,
                      errorTitle="Invalid quantity", error="Whole number from 0 to Quantity."), "N")
add_dv(DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True,
                      errorTitle="Invalid date", error="Enter a valid date (yyyy-mm-dd)."), "O")

# Visual hints for missing conditional fields (PTS still validates on import)
RED = PatternFill("solid", fgColor="FFC7CE")
ws.conditional_formatting.add(f"L2:L{last}", FormulaRule(formula=['AND($K2="On hold",$L2="")'], fill=RED))
ws.conditional_formatting.add(f"M2:M{last}", FormulaRule(formula=['AND($K2="Ready for inspection",$M2="")'], fill=RED))
ws.conditional_formatting.add(f"P2:P{last}", FormulaRule(formula=['AND($L2="Other",$P2="")'], fill=RED))

ws.protection.sheet = True  # no password: protection is a guide, PTS detects locked-column changes on import
ws.protection.formatCells = False
ws.protection.formatColumns = False
ws.protection.autoFilter = False

# Instructions sheet
ins = wb.create_sheet("Instructions", 0)
ins.column_dimensions["A"].width = 110
lines = [
    ("PTS supplier update file", True),
    (f"Export ID: {EXPORT_ID}   Export date: {EXPORT_DATE.isoformat()}   Supplier: {SUPPLIER}", False),
    ("", False),
    ("How to fill in the file", True),
    ("1. Open the 'Jobs' sheet. Grey columns are locked. Do not change them.", False),
    ("2. Fill in the yellow columns for each job. Pick status, reason and inspection type from the dropdown lists.", False),
    ("3. Do not add, delete or reorder rows, and do not rename columns.", False),
    ("4. Save the file as .xlsx and return it to us by email or the shared folder.", False),
    ("", False),
    ("Rules", True),
    ("- Status 'On hold' requires an On hold reason. Reason 'Other' requires a comment.", False),
    ("- Status 'Ready for inspection' requires an inspection type (Before painting or Final).", False),
    ("- Completed quantity is a whole number from 0 to the ordered quantity.", False),
    ("- Expected completion date must be a valid date (yyyy-mm-dd).", False),
    ("- Rows marked NEW REVISION (red) have a new drawing revision. Work from the new drawing in the shared folder.", False),
    ("", False),
    ("All data in this file is fictional.", False),
]
for i, (text, bold) in enumerate(lines, start=1):
    c = ins.cell(row=i, column=1, value=text)
    c.font = Font(bold=bold, size=14 if i == 1 else 11)
ins.protection.sheet = True
wb.active = 1

wb.save(OUT)
print("saved", OUT)
