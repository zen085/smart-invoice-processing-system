from django.db import models
import uuid
from core.models import TimeStampModel
from uploaded_file.models import UploadedFile
from django.conf import settings
from .utils import generate_invoice_number

# Create your models here.

class Invoice(TimeStampModel):
    STATUS_CHOICES = [
        ("DRAFT","Draft"),
        ("PAID","Paid"),
        ("UNPAID","Unpaid"),

    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="invoices")
    invoice_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    invoice_number = models.CharField(max_length=50,unique=True,editable=False)
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField()

    subtotal = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="UNPAID")

    uploaded_file = models.ForeignKey(UploadedFile,on_delete=models.CASCADE,related_name="invoices")
    pdf_file = models.FileField(upload_to="invoices/pdf/")
     

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number}"
