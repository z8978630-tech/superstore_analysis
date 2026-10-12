"""
Feature Engineering Module
--------------------------
Creates new features from existing columns for time-based analysis.
"""

import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features to the dataframe.
    
    Creates:
    - Year: year of Order Date
    - Month: month number
    - Month_Year: monthly period (e.g., '2017-12')
    - Quarter: quarter number (1-4)
    - Shipping Days: days between Order and Ship Date
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with 'Order Date' and 'Ship Date' columns.
    
    Returns
    -------
    pd.DataFrame
        Dataframe with new time-based features.
    """
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Month_Year'] = df['Order Date'].dt.to_period('M')
    df['Quarter'] = df['Order Date'].dt.quarter
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    print("✅ Added time features: Year, Month, Month_Year, Quarter, Shipping Days")
    return df