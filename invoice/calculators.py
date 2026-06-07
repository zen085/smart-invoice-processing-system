from decimal import Decimal,ROUND_HALF_UP

class InvoiceCalculator:   
    TAX_RATE = Decimal("0.16")

    @classmethod
    def calculate_totals(cls,subtotal):
        tax =  (subtotal*cls.TAX_RATE).quantize(Decimal("0.00"),rounding=ROUND_HALF_UP)
        total = (subtotal+tax).quantize(Decimal("0.00"),rounding=ROUND_HALF_UP)
        return{
            "tax":tax,
            "total":total
        }
    
    @classmethod
    def update_invoice_totals(cls,invoice,subtotal):
        totals = cls.calculate_totals(subtotal)
        invoice.subtotal = subtotal
        invoice.tax = totals["tax"]
        invoice.total = totals["total"]
        invoice.save(
            update_fields=["subtotal","tax","total",]
        )
