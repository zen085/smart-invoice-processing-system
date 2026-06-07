from dataclasses import dataclass
from uploaded_file.dto.invoice_item_data import InvoiceItemData

@dataclass
class InvoiceData:
    customer: str
    email: str
    items: list[InvoiceItemData]
    