"""
Data Loader Module
------------------
Loads the Superstore dataset from an Excel file.
"""

import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the Superstore dataset from an Excel file.
    
    Parameters
    ----------
    filepath : str
        Path to the Excel file.
    
    Returns
    -------
    pd.DataFrame
        Raw dataframe with all original columns.
    """
    df = pd.read_excel(filepath)
    
    # Convert date columns to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    print(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    return df