from decimal import Decimal
from uploaded_file.dto.invoice_data import InvoiceData
from uploaded_file.dto.invoice_item_data import InvoiceItemData


class InvoiceDataMapper:
    @staticmethod
    def map_group_to_dto(customer,email,rows):
        # first_row = rows.iloc[0]
        items = [ 
             InvoiceItemData(
                item=row.item,
                price=Decimal(str(row.price)),
                quantity=int(row.quantity),
            )
            for row in rows.itertuples(index=False)

            ]
        
       
         

        return InvoiceData(
            customer=customer,
            email=email,
            items=items

        )
