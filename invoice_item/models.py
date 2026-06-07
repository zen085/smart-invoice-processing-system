from django.db import models
from core.models import TimeStampModel
from invoice.models import Invoice
from django.conf import settings

# Create your models here.

class InvoiceItem(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="items")
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name="items")
    item_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=20,decimal_places=2)
    total_price = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return f"{self.item_name}"

    