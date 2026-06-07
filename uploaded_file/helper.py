import pandas as pd
import numpy as np

class DataFrameCleaner:

    REQUIRED_COLUMNS = [
        "customer",
        "email",
        "item",
        "price",
        "quantity",
    ]

    @staticmethod #belongs to the class for organization, but does NOT depend on the class or instance.
    def read_file(uploaded_file):
        
        file_path = uploaded_file.file.path

        # read file
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        
        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        return df

    
    @staticmethod
    def clean_columns(df: pd.DataFrame) -> pd.DataFrame:  #This function takes a Pandas DataFrame as input and returns a Pandas DataFrame.”
        df.columns = df.columns.str.strip().str.lower()
        return df
    
    @staticmethod
    def validate_columns(df):
        missing_column = [
            column
            for column in DataFrameCleaner.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_column:
            missing = ", ".join(missing_column)
            raise ValueError(f"Missing columns: {missing}")
    

    @staticmethod
    def validate_numeric_columns(df, columns):

        for column in columns:

            # Convert to string first
            df[column] = df[column].astype(str)

            # Remove common formatting issues
            df[column] = (
                df[column].str.strip().str.replace(",", "", regex=False).str.replace("$", "", regex=False)
            )

            # Convert to numeric
            try:

                df[column] = pd.to_numeric(df[column],errors="raise")

            except Exception:

                raise ValueError(
                    f"{column} must contain valid numeric values"
                )

            # Check nulls
            if df[column].isnull().any():

                raise ValueError(
                    f"{column} contains missing values"
                )

            # Check infinite numbers
            if np.isinf(df[column]).any():

                raise ValueError(
                    f"{column} contains invalid infinite values"
                )

            # Negative validation
            if (df[column] < 0).any():

                raise ValueError(
                    f"{column} cannot contain negative values"
                )

            # Zero quantity validation
            if column == "quantity":

                if (df[column] == 0).any():

                    raise ValueError(
                        "quantity cannot be zero"
                    )

            # Zero/negative price validation
            if column == "price":

                if (df[column] <= 0).any():

                    raise ValueError(
                        "price must be greater than zero"
                    )

        return df
    @staticmethod
    def normalize_columns(df):

        df["customer"] = (
            df["customer"]
            .astype(str)
            .str.strip()
            .str.title()
        )

        df["email"] = (
            df["email"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        return df