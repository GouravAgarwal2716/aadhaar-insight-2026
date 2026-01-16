import pandas as pd
import numpy as np

class DataCleaner:
    """
    Cleans and standardizes the Aadhar ecosystem data.
    """
    
    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Strip whitespace and lowercase column names."""
        df.columns = df.columns.str.strip().str.lower()
        return df

    @staticmethod
    def clean_strings(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Title case and strip whitespace for string columns."""
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()
        return df

    @staticmethod
    def parse_dates(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
        """Convert date column to datetime objects."""
        if date_col in df.columns:
            # We assume day-first format (DD-MM-YYYY) based on inspection "02-03-2025"
            df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce')
        return df

    @staticmethod
    def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
        """
        Fills missing values:
        - 0 for numeric columns (transactions count).
        - 'Unknown' for string columns.
        """
        numerics = df.select_dtypes(include=[np.number]).columns
        df[numerics] = df[numerics].fillna(0)
        
        strings = df.select_dtypes(include=[object]).columns
        df[strings] = df[strings].fillna('Unknown')
        return df

    @classmethod
    def process(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Master function to run all cleaning steps."""
        df = cls.clean_column_names(df)
        df = cls.clean_strings(df, ['state', 'district'])
        df = cls.parse_dates(df, 'date')
        df = cls.handle_missing(df)
        return df
