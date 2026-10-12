"""
Data Cleaning Module
--------------------
Cleans the Superstore dataset:
- Removes duplicate Order IDs
- Converts categorical columns to 'category' dtype
- Filters invalid values (negative Sales, unreasonable Profit)
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by removing duplicates and invalid values.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe.
    
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.
    """
    print("=" * 60)
    print("DATA CLEANING")
    print("=" * 60)
    
    # Step 1: Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['Order ID', 'Product ID'])
    print(f"✓ Removed duplicates: {before - len(df)} rows")
    
    # Step 2: Convert categorical columns
    categorical_cols = ['Segment', 'Region', 'Category', 'Sub-Category']
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    print(f"✓ Converted {len(categorical_cols)} columns to category")
    
    # Step 3: Filter invalid values
    before = len(df)
    df = df[(df['Sales'] >= 0) & (df['Profit'].abs() <= 1000)]
    print(f"✓ Removed invalid values: {before - len(df)} rows")
    
    print(f"\n✅ Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
    return df