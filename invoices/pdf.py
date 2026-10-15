from fpdf import FPDF
from fpdf.enums import XPos, YPos

from .config import FONTS_DIR
from .money import fmt_date, fmt_money

GREY = (110, 110, 110)


def render(inv, path) -> None:
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_font("WorkSans", "", str(FONTS_DIR / "WorkSans-Regular.ttf"))
    pdf.add_font("WorkSans", "B", str(FONTS_DIR / "WorkSans-Bold.ttf"))
    pdf.add_page()
    width = pdf.w - pdf.l_margin - pdf.r_margin

    def text(size, bold=False, colour=(0, 0, 0)):
        pdf.set_font("WorkSans", "B" if bold else "", size)
        pdf.set_text_color(*colour)

    def block(title, lines):
        text(8, colour=GREY)
        pdf.cell(0, 5, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        text(10)
        for line in lines:
            pdf.cell(0, 5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

    text(22, bold=True)
    pdf.cell(width / 2, 10, "INVOICE")
    text(10)
    pdf.cell(width / 2, 5, f"Invoice no: {inv.number}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(width / 2, 5, "")
    pdf.cell(width / 2, 5, f"Date: {fmt_date(inv.date)}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    s = inv.sender
    block("From", [s["name"], *s["address"].strip().splitlines(), s["phone"], s["email"]])
    block("Bill to", [inv.client["name"], *inv.client["address"].strip().splitlines()])

    col = [30, width - 30 - 32, 32]
    text(9, bold=True, colour=GREY)
    pdf.set_draw_color(*GREY)
    for w, label, align in zip(col, ["Date", "Description", "Amount"], ["L", "L", "R"]):
        pdf.cell(w, 8, label, border="B", align=align)
    pdf.ln(8)
    text(10)
    for item in inv.items:
        lines = pdf.multi_cell(col[1], 7, item.description, dry_run=True, output="LINES")
        height = 7 * max(len(lines), 1)
        if pdf.get_y() + height > pdf.page_break_trigger:
            pdf.add_page()
        x, y = pdf.l_margin, pdf.get_y()
        pdf.set_xy(x, y)
        pdf.cell(col[0], 7, fmt_date(item.date))
        pdf.multi_cell(col[1], 7, item.description, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_xy(x + col[0] + col[1], y)
        pdf.cell(col[2], 7, fmt_money(item.amount), align="R")
        pdf.set_xy(x, y + height)
    pdf.ln(2)
    text(11, bold=True)
    pdf.cell(col[0] + col[1], 9, "Total", border="T", align="R")
    pdf.cell(col[2], 9, fmt_money(inv.total), border="T", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    if inv.notes:
        block("Notes", inv.notes.strip().splitlines())
    block("Payment details", inv.payment["details"].strip().splitlines())
    pdf.output(str(path))
