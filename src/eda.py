"""
EDA Module (Exploratory Data Analysis)
--------------------------------------
Functions for aggregating and analyzing the dataset.
"""

import pandas as pd


def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales and profit by month."""
    monthly = df.groupby('Month_Year').agg(
        total_sales=('Sales', 'sum'),
        total_profit=('Profit', 'sum')
    ).reset_index()
    monthly['Month_Year'] = monthly['Month_Year'].astype(str)
    return monthly


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales and profit by category with margin."""
    cat = df.groupby('Category').agg(
        total_sales=('Sales', 'sum'),
        total_profit=('Profit', 'sum')
    ).reset_index()
    cat['profit_margin_%'] = (
        cat['total_profit'] / cat['total_sales'] * 100
    ).round(2)
    return cat.sort_values('total_sales', ascending=False)


def get_region_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales, profit, and margin by region (multi-metric)."""
    region = df.groupby('Region').agg(
        total_sales=('Sales', 'sum'),
        total_profit=('Profit', 'sum')
    ).reset_index()
    region['profit_margin_%'] = (
        region['total_profit'] / region['total_sales'] * 100
    ).round(2)
    region['sales_share_%'] = (
        region['total_sales'] / region['total_sales'].sum() * 100
    ).round(2)
    return region.sort_values('total_sales', ascending=False)


def get_segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by customer segment."""
    segment = df.groupby('Segment')['Sales'].sum().reset_index()
    segment['share_%'] = (
        segment['Sales'] / segment['Sales'].sum() * 100
    ).round(2)
    return segment.sort_values('Sales', ascending=False)


def get_discount_profit(df: pd.DataFrame) -> pd.DataFrame:
    """Compute average profit per discount rate."""
    return df.groupby('Discount')['Profit'].mean().reset_index()


def get_top_subcategories(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Return top-N sub-categories by total sales."""
    return df.groupby('Sub-Category')['Sales'].sum().nlargest(n)


def get_peak_months(df: pd.DataFrame, n: int = 3) -> dict:
    """Return top-N months by sales and by profit."""
    monthly = get_monthly_summary(df)
    return {
        'peak_sales': monthly.nlargest(n, 'total_sales')[['Month_Year', 'total_sales']],
        'peak_profit': monthly.nlargest(n, 'total_profit')[['Month_Year', 'total_profit']],
    }