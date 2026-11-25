"""Generate the PTS Excel templates in Norwegian (fictional example data).

Writes two files:
  - pts-supplier-template.xlsx   supplier file, per PRD FR-7, FR-8, FR-9 and section 3.1
  - pts-job-package-template.xlsx  job package, per PRD FR-31

Usage: python make_template.py [SUPPLIER_OUT [JOB_PACKAGE_OUT]]
Without arguments, both files are written next to this script.
All data is fictional (PRD NFR-8).
"""
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).resolve().parent
SUPPLIER_OUT = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "pts-supplier-template.xlsx")
PACKAGE_OUT = sys.argv[2] if len(sys.argv) > 2 else str(HERE / "pts-job-package-template.xlsx")

YES_NO = ["Ja", "Nei"]
STOP_REASONS = ["Tegningsfeil", "Mangler materiale", "Ønsker kontroll", "Annet"]
STAGES = ["Material", "Sveiset", "Kontrollert", "Sandblåst", "Malt", "Sluttkontroll"]

LOCKED = [
    ("Eksport-ID", 18), ("Eksportdato", 12), ("Jobb-ID", 10), ("Rom", 8), ("Tegningsnummer", 28),
    ("Revisjon", 10), ("Revisjonsmerknad", 16), ("Leverandør", 26), ("Frist", 12),
]
EDITABLE = [(s, 13) for s in STAGES] + [
    ("Stoppet", 10), ("Årsak til stopp", 18), ("Forventet dato levert", 14), ("Kommentar / avviksbeskrivelse", 40),
]

EXPORT_ID = "EXP-20261125-0001"
EXPORT_DATE = date(2026, 11, 25)
SUPPLIER = "Leverandør Alfa (fiktiv)"
DATE_FMT = "dd.mm.yyyy"


def d(day, month=11):
    return date(2026, month, day)


# Fictional rows. Stage dates are in the order Material, Sveiset, Kontrollert, Sandblåst, Malt, Sluttkontroll.
# (job, room, drawing, rev, new_rev, due, stage dates, stopped, reason, expected, comment)
ROWS = [
    ("PTS-0001", "0101", "DEMO-0101-A001", "B", False, d(4, 12), [d(16), d(18), d(20), d(23), None, None], "Nei", None, d(1, 12), None),
    ("PTS-0002", "0101", "DEMO-0101-A002", "C", True, d(11, 12), [d(17), None, None, None, None, None], "Nei", None, None, None),
    ("PTS-0003", "0101", "DEMO-0101-A003", "A", False, d(27), [None, None, None, None, None, None], "Ja", "Mangler materiale", d(9, 12), "Venter på levering av plate"),
    ("PTS-0004", "0102", "DEMO-0102-B001", "A", False, d(30), [d(10), d(14), None, None, None, None], "Nei", None, d(28), None),
    ("PTS-0005", "0102", "DEMO-0102-B002", "B", False, d(18, 12), [None, None, None, None, None, None], "Nei", None, None, None),
    ("PTS-0006", "0102", "DEMO-0102-B003", "A", False, d(2, 12), [d(5), d(9), d(12), d(16), d(19), d(23)], "Nei", None, d(27), None),
    ("PTS-0007", "0103", "DEMO-0103-C001", "A", False, d(9, 12), [d(12), d(16), d(18), d(23), None, None], "Nei", None, d(4, 12), "Aluminium"),
    ("PTS-0008", "0103", "DEMO-0103-C002", "B", False, d(15, 12), [d(20), None, None, None, None, None], "Ja", "Tegningsfeil", None, "AVKLARES – måltoleranse"),
]

GREY = PatternFill("solid", fgColor="E7E6E6")
HEAD_LOCKED = PatternFill("solid", fgColor="595959")
HEAD_EDIT = PatternFill("solid", fgColor="1F4E78")
EDIT = PatternFill("solid", fgColor="FFF2CC")
NEWREV = PatternFill("solid", fgColor="F8CBAD")
RED = PatternFill("solid", fgColor="FFC7CE")
ORANGE = PatternFill("solid", fgColor="FFD966")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def style_header(cell, fill):
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = fill
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    cell.border = BORDER


def write_instructions(wb, lines, index=0):
    ins = wb.create_sheet("Instruksjoner", index)
    ins.column_dimensions["A"].width = 110
    for i, (text, bold) in enumerate(lines, start=1):
        c = ins.cell(row=i, column=1, value=text)
        c.font = Font(bold=bold, size=14 if i == 1 else 11)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ins.protection.sheet = True
    return ins


def build_supplier_file(out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Jobber"

    # Hidden list sheet feeding the dropdowns
    lists = wb.create_sheet("Lister")
    for col, (name, values) in enumerate([("Stoppet", YES_NO), ("Årsak til stopp", STOP_REASONS)], start=1):
        lists.cell(row=1, column=col, value=name).font = Font(bold=True)
        for i, v in enumerate(values, start=2):
            lists.cell(row=i, column=col, value=v)
    lists.sheet_state = "hidden"
    lists.protection.sheet = True

    headers = LOCKED + EDITABLE
    n_locked = len(LOCKED)
    col_of = {name: get_column_letter(i) for i, (name, _) in enumerate(headers, start=1)}
    for c, (name, width) in enumerate(headers, start=1):
        style_header(ws.cell(row=1, column=c, value=name), HEAD_LOCKED if c <= n_locked else HEAD_EDIT)
        ws.column_dimensions[get_column_letter(c)].width = width
    ws.row_dimensions[1].height = 42
    ws.freeze_panes = "F2"

    ws[f"{col_of['Revisjonsmerknad']}1"].comment = Comment(
        "NY REVISJON = tegningsrevisjonen er endret siden forrige fil til denne leverandøren. Bruk den nye tegningen.", "PTS")
    ws[f"{col_of['Material']}1"].comment = Comment(
        "Dato for når materialet er på plass. Tomt = ikke klart.", "PTS")
    ws[f"{col_of['Sveiset']}1"].comment = Comment(
        "Fyll inn dato når trinnet er ferdig. Trinnene tas i rekkefølge: Material, Sveiset, Kontrollert, Sandblåst, Malt, Sluttkontroll.", "PTS")
    ws[f"{col_of['Stoppet']}1"].comment = Comment("Velg Ja eller Nei. Ja krever årsak til stopp.", "PTS")
    ws[f"{col_of['Årsak til stopp']}1"].comment = Comment("Påkrevd når Stoppet er Ja. Annet krever kommentar.", "PTS")

    for r, row in enumerate(ROWS, start=2):
        job, room, drw, rev, new_rev, due, stage_dates, stopped, reason, expected, comment = row
        values = [EXPORT_ID, EXPORT_DATE, job, room, drw, rev, "NY REVISJON" if new_rev else None, SUPPLIER, due,
                  *stage_dates, stopped, reason, expected, comment]
        for c, v in enumerate(values, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.border = BORDER
            if c <= n_locked:
                cell.fill = GREY
                cell.protection = Protection(locked=True)
            else:
                cell.fill = EDIT
                cell.protection = Protection(locked=False)
            if isinstance(v, date):
                cell.number_format = DATE_FMT
            if c == 4:  # Rom as text so leading zeros are kept
                cell.number_format = "@"
        if new_rev:
            for name in ("Revisjon", "Revisjonsmerknad"):
                cell = ws[f"{col_of[name]}{r}"]
                cell.fill = NEWREV
                cell.font = Font(bold=True, color="9C0006")

    last = len(ROWS) + 1

    def add_dv(dv, col):
        dv.error_style = "stop"
        dv.showErrorMessage = True
        ws.add_data_validation(dv)
        dv.add(f"{col}2:{col}{last}")

    stage_cols = [col_of[s] for s in STAGES]
    for col in stage_cols + [col_of["Forventet dato levert"]]:
        add_dv(DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True,
                              errorTitle="Ugyldig dato", error="Skriv en gyldig dato (dd.mm.åååå)."), col)
    add_dv(DataValidation(type="list", formula1=f"=Lister!$A$2:$A${len(YES_NO)+1}", allow_blank=True,
                          errorTitle="Ugyldig verdi", error="Velg Ja eller Nei fra listen."), col_of["Stoppet"])
    add_dv(DataValidation(type="list", formula1=f"=Lister!$B$2:$B${len(STOP_REASONS)+1}", allow_blank=True,
                          errorTitle="Ugyldig årsak", error="Velg en årsak fra listen."), col_of["Årsak til stopp"])

    # Visual hints (PTS still validates every rule on import)
    stopped, reason, comment = col_of["Stoppet"], col_of["Årsak til stopp"], col_of["Kommentar / avviksbeskrivelse"]
    ws.conditional_formatting.add(f"{reason}2:{reason}{last}",
                                  FormulaRule(formula=[f'AND(${stopped}2="Ja",${reason}2="")'], fill=RED))
    ws.conditional_formatting.add(f"{comment}2:{comment}{last}",
                                  FormulaRule(formula=[f'AND(${reason}2="Annet",${comment}2="")'], fill=RED))
    for i, col in enumerate(stage_cols[1:], start=1):  # a stage date with an earlier stage missing
        first, prev = stage_cols[0], stage_cols[i - 1]
        ws.conditional_formatting.add(
            f"{col}2:{col}{last}",
            FormulaRule(formula=[f'AND({col}2<>"",COUNTBLANK(${first}2:${prev}2)>0)'], fill=ORANGE))

    ws.protection.sheet = True  # no password: protection is a guide, PTS detects locked-column changes on import
    ws.protection.formatCells = False
    ws.protection.formatColumns = False
    ws.protection.autoFilter = False

    write_instructions(wb, [
        ("PTS oppdateringsfil for leverandør", True),
        (f"Eksport-ID: {EXPORT_ID}   Eksportdato: {EXPORT_DATE.strftime('%d.%m.%Y')}   Leverandør: {SUPPLIER}", False),
        ("", False),
        ("Slik fyller du ut fila", True),
        ("1. Åpne arket «Jobber». Grå kolonner er låst. Ikke endre dem. Jobbene er sortert etter rom.", False),
        ("2. Fyll ut de gule kolonnene for hver jobb.", False),
        ("3. Ikke legg til, slett eller flytt rader, og ikke endre kolonnenavn.", False),
        ("4. Lagre fila som .xlsx og send den tilbake til oss på e-post eller i den delte mappa.", False),
        ("", False),
        ("Trinn og datoer", True),
        ("- Trinnene er: Material, Sveiset, Kontrollert, Sandblåst, Malt, Sluttkontroll. Fyll inn datoen når trinnet er ferdig. Tomt betyr ikke ferdig.", False),
        ("- Ta trinnene i rekkefølge. En dato på et trinn uten at forrige trinn er ferdig (oransje celle) gir en advarsel hos oss.", False),
        ("- Datoer skrives som dd.mm.åååå.", False),
        ("- Forventet dato levert er datoen dere forventer å levere jobben. Den kan stå tom.", False),
        ("- Levert registrerer vi selv når jobben er mottatt. Den er ikke i fila.", False),
        ("", False),
        ("Stopp og kommentar", True),
        ("- Velg Ja i kolonnen Stoppet hvis jobben ikke kan fortsette. Da må dere velge årsak til stopp (rød celle hvis den mangler).", False),
        ("- Årsaken «Annet» krever en kommentar.", False),
        ("- Rader merket NY REVISJON (rødt) har en ny tegningsrevisjon. Bruk den nye tegningen i den delte mappa.", False),
        ("", False),
        ("Alle data i denne fila er fiktive.", False),
    ])
    wb.active = 1
    wb.save(out)
    print("saved", out)


def build_job_package(out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Jobbpakke"
    columns = [("Rom", 10), ("Område", 18), ("Tegningsnummer", 28), ("Revisjon", 10), ("Frist", 13)]
    for c, (name, width) in enumerate(columns, start=1):
        style_header(ws.cell(row=1, column=c, value=name), HEAD_EDIT)
        ws.column_dimensions[get_column_letter(c)].width = width
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    ws["B1"].comment = Comment("Intern gruppering, for eksempel dekk. Kan stå tom. Går ikke til leverandøren.", "PTS")

    rows = [
        ("0101", "Område A", "DEMO-0101-A001", "B", d(4, 12)),
        ("0101", "Område A", "DEMO-0101-A002", "C", d(11, 12)),
        ("0102", "Område A", "DEMO-0102-B001", "A", d(30)),
        ("0102", "Område A", "DEMO-0102-B002", "B", d(18, 12)),
        ("0201", "Område B", "DEMO-0201-D001", "A", d(9, 12)),
        ("0201", "Område B", "DEMO-0201-D002", "A", d(15, 12)),
    ]
    for r, row in enumerate(rows, start=2):
        for c, v in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.border = BORDER
            cell.fill = EDIT
            if isinstance(v, date):
                cell.number_format = DATE_FMT
            if c in (1, 4):  # Rom and Revisjon as text so leading zeros are kept
                cell.number_format = "@"

    last = 500  # room for a full job package
    dv = DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True,
                        errorTitle="Ugyldig dato", error="Skriv en gyldig dato (dd.mm.åååå).")
    ws.add_data_validation(dv)
    dv.add(f"E2:E{last}")

    write_instructions(wb, [
        ("PTS jobbpakke", True),
        ("Denne fila lister tegninger som skal opprettes som jobber for én leverandør.", False),
        ("", False),
        ("Slik fyller du ut fila", True),
        ("1. Én rad per tegning. Alle kolonner unntatt Område må fylles ut.", False),
        ("2. Importer fila i PTS og velg leverandør. PTS viser en forhåndsvisning før noe opprettes.", False),
        ("3. Rader hoppes over hvis rom, tegningsnummer eller revisjon mangler, eller fristen ikke er en gyldig dato. Et tegningsnummer som finnes fra før gir en advarsel i forhåndsvisningen, men hoppes ikke over, siden samme tegning kan lages flere ganger.", False),
        ("4. Maks 500 rader per fil.", False),
        ("", False),
        ("Alle data i denne fila er fiktive.", False),
    ])
    wb.active = 1
    wb.save(out)
    print("saved", out)


build_supplier_file(SUPPLIER_OUT)
build_job_package(PACKAGE_OUT)
