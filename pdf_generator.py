from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# INVOICE DIRECTORY

BASE_DIR = Path(__file__).resolve().parent

INVOICES_DIR = BASE_DIR / "invoices"

INVOICES_DIR.mkdir(exist_ok=True)



# GENERATE PDF



def generate_invoice_pdf(invoice):
    """
    Generate a PDF invoice.

    Returns:
        Path to the generated PDF.
    """

    invoice_number = invoice["invoice_number"]

    pdf_path = INVOICES_DIR / f"{invoice_number}.pdf"
    # DOCUMENT
    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    # STYLES
    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    normal_style = styles["Normal"]

    heading_style = styles["Heading2"]
    # PDF CONTENT
    content = []
    # TITLE
    content.append(Paragraph("INVOICE", title_style))

    content.append(Spacer(1, 10))
    # INVOICE INFORMATION
    invoice_information = [
        [Paragraph("<b>Invoice Number:</b>", normal_style), invoice["invoice_number"]],
        [Paragraph("<b>Date:</b>", normal_style), invoice["date"]],
        [Paragraph("<b>Customer:</b>", normal_style), invoice["customer_name"]],
        [Paragraph("<b>Email:</b>", normal_style), invoice["customer_email"]],
    ]

    info_table = Table(invoice_information, colWidths=[45 * mm, 110 * mm])

    info_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    content.append(info_table)

    content.append(Spacer(1, 15))
    # ITEMS
    content.append(Paragraph("Items", heading_style))

    content.append(Spacer(1, 5))

    items_table = [["Item / Service", "Quantity", "Unit Price", "Total"]]

    for item in invoice["items"]:
        items_table.append(
            [
                item["name"],
                f"{item['quantity']:.2f}",
                f"${item['unit_price']:.2f}",
                f"${item['total']:.2f}",
            ]
        )

    item_table = Table(items_table, colWidths=[75 * mm, 25 * mm, 30 * mm, 30 * mm])

    item_table.setStyle(
        TableStyle(
            [
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                # Borders
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                # Alignment
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # Padding
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    content.append(item_table)

    content.append(Spacer(1, 20))
    # TOTALS
    totals_table = [
        ["Subtotal:", f"${invoice['subtotal']:.2f}"],
        [f"Tax ({invoice['tax_rate']:.2f}%):", f"${invoice['tax']:.2f}"],
        ["Discount:", f"-${invoice['discount']:.2f}"],
        [
            Paragraph("<b>TOTAL:</b>", normal_style),
            Paragraph(f"<b>${invoice['total']:.2f}</b>", normal_style),
        ],
    ]

    totals = Table(totals_table, colWidths=[130 * mm, 30 * mm])

    totals.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEABOVE", (0, 3), (-1, 3), 1, colors.black),
            ]
        )
    )

    content.append(totals)

    content.append(Spacer(1, 30))
    # FOOTER
    content.append(Paragraph("Thank you for your business!", normal_style))
    # BUILD PDF
    document.build(content)

    return pdf_path
