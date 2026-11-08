"""Generate the PTS supplier Excel template in Norwegian (fictional example data), per PRD FR-7 and section 3.1."""
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1]

STATUSES = ["Ikke startet", "I produksjon", "Stoppet", "Klar for inspeksjon", "Ferdig"]
HOLD_REASONS = ["Tegningsfeil", "Mangler materiale", "Ønsker kontroll", "Annet"]
INSPECTION_TYPES = ["Før maling", "Sluttinspeksjon"]

LOCKED = [
    ("Eksport-ID", 20), ("Eksportdato", 13), ("Jobb-ID", 11), ("Tegningsnummer", 16),
    ("Revisjon", 10), ("Revisjonsmerknad", 16), ("Beskrivelse", 30), ("Antall", 10),
    ("Leverandør", 26), ("Frist", 13),
]
EDITABLE = [
    ("Produksjonsstatus", 21), ("Årsak til stopp", 18), ("Inspeksjonstype", 17),
    ("Antall ferdig", 12), ("Forventet ferdigdato", 14), ("Kommentar / avviksbeskrivelse", 40),
]

EXPORT_ID = "EXP-20261108-0001"
EXPORT_DATE = date(2026, 11, 8)
SUPPLIER = "Leverandør Alfa (fiktiv)"

# Fictional rows: (job, drawing, rev, new_rev, description, qty, due, status, reason, insp, done, expected, comment)
ROWS = [
    ("PTS-0001", "DRW-10001", "B", False, "Brakett, rustfritt stål", 12, date(2026, 12, 4), "I produksjon", None, None, 4, date(2026, 12, 1), None),
    ("PTS-0002", "DRW-10002", "C", True, "Akselhus, maskinert", 4, date(2026, 12, 11), "Ikke startet", None, None, 0, None, None),
    ("PTS-0003", "DRW-10003", "A", False, "Sveiset ramme, fundament", 2, date(2026, 11, 27), "Stoppet", "Mangler materiale", None, 0, date(2026, 12, 9), None),
    ("PTS-0004", "DRW-10004", "A", False, "Dekkplate", 20, date(2026, 11, 20), "Klar for inspeksjon", None, "Før maling", 20, date(2026, 11, 19), None),
    ("PTS-0005", "DRW-10005", "D", False, "Flens, DN150", 8, date(2026, 12, 18), "Ikke startet", None, None, 0, None, None),
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
ws.title = "Jobber"

# Hidden list sheet feeding the dropdowns
lists = wb.create_sheet("Lister")
for col, (name, values) in enumerate(
    [("Produksjonsstatus", STATUSES), ("Årsak til stopp", HOLD_REASONS), ("Inspeksjonstype", INSPECTION_TYPES)], start=1
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

ws["F1"].comment = Comment("NY REVISJON = tegningsrevisjonen er endret siden forrige fil til denne leverandøren. Bruk den nye tegningen.", "PTS")
ws["K1"].comment = Comment("Velg fra listen. Stoppet krever årsak. Klar for inspeksjon krever inspeksjonstype.", "PTS")
ws["L1"].comment = Comment("Påkrevd når status er Stoppet. Annet krever kommentar.", "PTS")
ws["M1"].comment = Comment("Påkrevd når status er Klar for inspeksjon.", "PTS")
ws["N1"].comment = Comment("Heltall fra 0 til Antall.", "PTS")

DATE_FMT = "dd.mm.yyyy"
for r, row in enumerate(ROWS, start=2):
    job, drw, rev, new_rev, desc, qty, due, status, reason, insp, done, expected, comment = row
    values = [EXPORT_ID, EXPORT_DATE, job, drw, rev, "NY REVISJON" if new_rev else None, desc, qty, SUPPLIER, due,
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


add_dv(DataValidation(type="list", formula1=f"=Lister!$A$2:$A${len(STATUSES)+1}", allow_blank=False,
                      errorTitle="Ugyldig status", error="Velg en status fra listen."), "K")
add_dv(DataValidation(type="list", formula1=f"=Lister!$B$2:$B${len(HOLD_REASONS)+1}", allow_blank=True,
                      errorTitle="Ugyldig årsak", error="Velg en årsak fra listen."), "L")
add_dv(DataValidation(type="list", formula1=f"=Lister!$C$2:$C${len(INSPECTION_TYPES)+1}", allow_blank=True,
                      errorTitle="Ugyldig inspeksjonstype", error="Velg en inspeksjonstype fra listen."), "M")
add_dv(DataValidation(type="custom", formula1="AND(ISNUMBER(N2),N2=INT(N2),N2>=0,N2<=H2)", allow_blank=True,
                      errorTitle="Ugyldig antall", error="Heltall fra 0 til Antall."), "N")
add_dv(DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True,
                      errorTitle="Ugyldig dato", error="Skriv en gyldig dato (dd.mm.åååå)."), "O")

# Visual hints for missing conditional fields (PTS still validates on import)
RED = PatternFill("solid", fgColor="FFC7CE")
ws.conditional_formatting.add(f"L2:L{last}", FormulaRule(formula=['AND($K2="Stoppet",$L2="")'], fill=RED))
ws.conditional_formatting.add(f"M2:M{last}", FormulaRule(formula=['AND($K2="Klar for inspeksjon",$M2="")'], fill=RED))
ws.conditional_formatting.add(f"P2:P{last}", FormulaRule(formula=['AND($L2="Annet",$P2="")'], fill=RED))

ws.protection.sheet = True  # no password: protection is a guide, PTS detects locked-column changes on import
ws.protection.formatCells = False
ws.protection.formatColumns = False
ws.protection.autoFilter = False

# Instructions sheet
ins = wb.create_sheet("Instruksjoner", 0)
ins.column_dimensions["A"].width = 110
lines = [
    ("PTS oppdateringsfil for leverandør", True),
    (f"Eksport-ID: {EXPORT_ID}   Eksportdato: {EXPORT_DATE.strftime('%d.%m.%Y')}   Leverandør: {SUPPLIER}", False),
    ("", False),
    ("Slik fyller du ut fila", True),
    ("1. Åpne arket «Jobber». Grå kolonner er låst. Ikke endre dem.", False),
    ("2. Fyll ut de gule kolonnene for hver jobb. Velg status, årsak og inspeksjonstype fra nedtrekkslistene.", False),
    ("3. Ikke legg til, slett eller flytt rader, og ikke endre kolonnenavn.", False),
    ("4. Lagre fila som .xlsx og send den tilbake til oss på e-post eller i den delte mappa.", False),
    ("", False),
    ("Regler", True),
    ("- Status «Stoppet» krever årsak til stopp. Årsaken «Annet» krever kommentar.", False),
    ("- Status «Klar for inspeksjon» krever inspeksjonstype (Før maling eller Sluttinspeksjon).", False),
    ("- Antall ferdig er et heltall fra 0 til bestilt antall.", False),
    ("- Forventet ferdigdato må være en gyldig dato (dd.mm.åååå).", False),
    ("- Rader merket NY REVISJON (rødt) har en ny tegningsrevisjon. Bruk den nye tegningen i den delte mappa.", False),
    ("", False),
    ("Alle data i denne fila er fiktive.", False),
]
for i, (text, bold) in enumerate(lines, start=1):
    c = ins.cell(row=i, column=1, value=text)
    c.font = Font(bold=bold, size=14 if i == 1 else 11)
ins.protection.sheet = True
wb.active = 1

wb.save(OUT)
print("saved", OUT)
