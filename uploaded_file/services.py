from .helper import DataFrameCleaner
from invoice.services import InvoiceCreationService
from .mapper.invoice_mapper import InvoiceDataMapper


class UploadedFileProcessingService:

    @staticmethod
    def process_uploaded(uploaded_file):
        df = UploadedFileProcessingService.prepare_dataframe(uploaded_file)

        invoice_data_list = UploadedFileProcessingService.map_df_to_dto(df)
        InvoiceCreationService.create_invoices(
            invoice_data_list,
            uploaded_file=uploaded_file
        )

        uploaded_file.status = "Processed"
        uploaded_file.save(update_fields=["status"])


    @staticmethod
    def prepare_dataframe(uploaded_file):
        df = DataFrameCleaner.read_file(uploaded_file)
        df = DataFrameCleaner.clean_columns(df)
        DataFrameCleaner.validate_columns(df)
        df = DataFrameCleaner.validate_numeric_columns(
            df,
            ["price", "quantity"]
        )
        df = DataFrameCleaner.normalize_columns(df)

        return df
    
    @staticmethod
    def map_df_to_dto(df):
        grouped = df.groupby(["customer","email"])        
        
        invoice_data_list = []
        for grouped_key,rows in grouped: 
            customer,email = grouped_key          
            invoice_data = (
                InvoiceDataMapper.map_group_to_dto(customer,email,rows)
                            )
            invoice_data_list.append(invoice_data)

        return invoice_data_list
