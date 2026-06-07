from decimal import Decimal
from .models import InvoiceItem
from .utils import InvoiceCalculator


class InvoiceItemCreationService:

    @staticmethod
    def create_invoice_item(invoice, row):

        total_price = (
            InvoiceCalculator.calculate_total(
                row.price,
                row.quantity
            )
        )

        item = InvoiceItem.objects.create(
            user=invoice.user,
            invoice=invoice,
            item_name=row.item,
            quantity=row.quantity,
            unit_price=row.price,
            total_price=total_price,
        )

        return item, Decimal(str(total_price))