from invoice.reports.pdf_generator import PDFGenerator
from decimal import Decimal
from .models import Invoice
from django.db import transaction
from invoice_item.services import InvoiceItemCreationService
from .utils import generate_invoice_number
from .calculators import InvoiceCalculator
from zipfile import ZipFile
from pathlib import Path
from django.conf import settings


class InvoiceCreationService:

    @classmethod
    def create_invoices(cls,invoice_data_list, uploaded_file):
        invoices = []

        for invoice_data in invoice_data_list:
            invoice  = cls.create_invoice(invoice_data,uploaded_file)           
            PDFGenerator.generate_invoice_pdf(invoice)
            invoices.append(invoice)

        InvoiceArchiveService.generate_archive(uploaded_file)         
        return invoices
    
        

    @classmethod
    def create_invoice(cls,invoice_data,uploaded_file):
        with transaction.atomic(): 
            invoice = Invoice.objects.create(
                user = uploaded_file.user,
                invoice_number=generate_invoice_number(),
                customer_name=invoice_data.customer,
                customer_email=invoice_data.email,
                subtotal=Decimal("0.00"),
                tax=Decimal("0.00"),
                total=Decimal("0.00"),
                uploaded_file=uploaded_file,
            )

            subtotal = Decimal("0.00")

            for item_data in invoice_data.items:

                _, total_price = (
                    InvoiceItemCreationService.create_invoice_item(invoice,item_data)
                )

                subtotal += total_price
            InvoiceCalculator.update_invoice_totals(invoice,subtotal)


        
        return invoice


class InvoiceArchiveService:

    @classmethod
    def generate_archive(cls,uploaded_file):
        uploaded_file = uploaded_file.__class__.objects.prefetch_related("invoices").get(pk=uploaded_file.pk)
        invoices = uploaded_file.invoices.all()
        archive_name = "Invoices.zip"
        archive_relative_path = f"invoice_archives/{archive_name}"
        archive_full_path = Path(settings.MEDIA_ROOT)/archive_relative_path
        archive_full_path.parent.mkdir(parents=True,exist_ok=True)

        with ZipFile(archive_full_path,"w") as zip_file:
            for invoice in invoices:
                if invoice.pdf_file and Path(invoice.pdf_file.path).exists():
                    pdf_path = invoice.pdf_file.path
                    zip_file.write(pdf_path,arcname=Path(pdf_path).name)
        
        uploaded_file.invoice_archive = archive_relative_path
        uploaded_file.save(
            update_fields = ["invoice_archive"]
        )
