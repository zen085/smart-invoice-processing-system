
from io import BytesIO

from django.core.files.base import ContentFile

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.platypus.flowables import HRFlowable
from invoice.helper import InvoiceBranding,QRCodeGenerator
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from django.conf import settings
import os

PRIMARY_COLOR = HexColor(
    InvoiceBranding.PRIMARY_COLOR
)

class PDFGenerator:

    @staticmethod
    def generate_invoice_pdf(invoice):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=28,
        )

        styles = getSampleStyleSheet()

        elements = []
        
        # logo
        logo_path = os.path.join(settings.MEDIA_ROOT,"branding/logo.png")
        logo = Image(logo_path,width=140,height=70)
        elements.append(logo)
        elements.append(Spacer(1,10))

        # ======================
        # TITLE
        # ======================

        title = Paragraph(
            f"<b>INVOICE</b>",
            styles["Title"]
        )

        elements.append(title)
        elements.append(Spacer(1, 20))

        company_info = Paragraph(
            f"""
            <b>{InvoiceBranding.COMPANY_NAME}</b><br/>
            {InvoiceBranding.COMPANY_EMAIL}<br/>
            {InvoiceBranding.COMPANY_PHONE}<br/>
            {InvoiceBranding.COMPANY_WEBSITE}
            """,
            styles["BodyText"]
            )

        elements.append(company_info)
        elements.append(Spacer(1, 20))

        # ======================
        # INVOICE INFO
        # ======================

        invoice_info = [
            ["Invoice Number:", str(invoice.invoice_number)],
            ["Customer:", invoice.customer_name],
            ["Email:", invoice.customer_email],
            ["Status:", invoice.status],
        ]

        info_table = Table(
            invoice_info,
            colWidths=[150, 300]
        )

        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), PRIMARY_COLOR),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))

        elements.append(info_table)
        elements.append(Spacer(1, 20))

        elements.append(HRFlowable())
        elements.append(Spacer(1, 20))

        # ======================
        # ITEMS TABLE
        # ======================

        table_data = [
            ["Item", "Quantity", "Unit Price", "Total"]
        ]

        for item in invoice.items.all():

            table_data.append([
                item.item_name,
                str(item.quantity),
                f"${item.unit_price}",
                f"${item.total_price}",
            ])

        items_table = Table(
            table_data,
            colWidths=[200, 80, 100, 100]
        )

        items_table.setStyle(TableStyle([

            # Header
            ("BACKGROUND", (0, 0), (-1, 0), colors.black ),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            # Body
            ("BACKGROUND", (0, 1), (-1, -1), PRIMARY_COLOR),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))

        elements.append(items_table)
        elements.append(Spacer(1, 30))

        # ======================
        # TOTALS
        # ======================

        totals_data = [
            ["Subtotal", f"${invoice.subtotal}"],
            ["Tax", f"${invoice.tax}"],
            ["Total", f"${invoice.total}"],
        ]

        totals_table = Table(
            totals_data,
            colWidths=[300, 180]
        )

        totals_table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_COLOR),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))

        elements.append(totals_table)

        # terms&conditions
        terms = Paragraph(
            f"""
            <b>Terms & Conditions</b><br/>
            {InvoiceBranding.TERMS}
            """,
            styles["BodyText"]
        )

        elements.append(Spacer(1, 30))
        elements.append(terms)

        # signature
        signature_path = os.path.join(
                settings.MEDIA_ROOT,
                "branding/signature.png"
            )
        signature = Image(
            signature_path,
            width=120,
            height=50
        )

        elements.append(Spacer(1, 40))
        elements.append(signature)

        signed_by = Paragraph(
            "<b>Authorized Signature</b>",
            styles["BodyText"]
        )

        elements.append(signed_by)

        # qr code 
        qr_buffer = QRCodeGenerator.generate(invoice)

        qr_image = Image(
            qr_buffer,
            width=100,
            height=100
        )

        elements.append(Spacer(1, 20))
        elements.append(qr_image)

        # Build PDF
        doc.build(elements,
                  onFirstPage=PDFGenerator.add_footer,
                  onLaterPages=PDFGenerator.add_footer
                  )

        buffer.seek(0)

        file_name = (
            f"invoice_{invoice.invoice_number}.pdf"
        )

        invoice.pdf_file.save(
            file_name,
            ContentFile(buffer.read()),
            save=True
        )

        buffer.close()
    
    @staticmethod
    def add_footer(canvas, doc):

        canvas.saveState()

        footer_text = (
            InvoiceBranding.FOOTER_TEXT
        )

        canvas.setFont("Helvetica", 9)

        canvas.drawString(
            40,
            20,
            footer_text
        )

        page_number = (
            f"Page {canvas.getPageNumber()}"
        )

        canvas.drawRightString(
            200 * mm,
            20,
            page_number
        )

        canvas.restoreState()   



        


