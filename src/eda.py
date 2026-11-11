"""
EDA Module (Exploratory Data Analysis)
--------------------------------------
Functions for aggregating and analyzing the dataset.
"""

from __future__ import annotations
import inspect
import logging
import os
import sys 
from dataclasses import dataclass
from typing import Any,Optional
import pandas as pd
from .feature_engineering import add_time_features
logger=logging.getLogger(__name__)
@dataclass(frozen=True)
class PracticeResult:
    name:str
    date:Any=None
    # figure:Optional[plt.figure]=None
    stats:Optional[pd.Series]=None
    data:Any=None
def _validate_columns(df:pd.DataFrame, required: list[str]):
    missing=[c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"DataFrame:{missing}")
def _print_header(title:str,width:int=60)->None:
    print("="*width)
    print(title)
    print("="*width)

def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales and profit by month."""
    df_feat=add_time_features(df)
    _validate_columns(df_feat,['Month_Year', 'Sales', 'Profit'])
    monthly = df_feat.groupby('Month_Year').agg(
        total_sales=('Sales', 'sum'),
        total_profit=('Profit', 'sum'),
    ).reset_index()
    
    monthly['Month_Year']=monthly['Month_Year'].astype(str)
    return monthly
def analyze_seasonality(df: pd.DataFrame) -> dict:
    """آیا فروش در ماه‌های خاصی از سال تکرارشونده بالاتر است؟"""
    _validate_columns(df,['Year','Month', 'Sales'])
    work=df.copy()
    work['Year']=work['Year'].astype(int)
    work['Month']=work['Month'].astype(int)
    monthly=(work.groupby(['Year','Month'])['Sales']).sum().unstack('Year')
    month_avg = monthly.mean(axis=1)
    overall_avg = month_avg.mean()
    
    # شاخص فصلی: >1 یعنی بالاتر از میانگین، <1 یعنی پایین‌تر
    seasonal_index = (month_avg / overall_avg).round(3)
    
    strength = seasonal_index.std()  
    has_seasonality=bool(strength>0.15)
    ranks=monthly.rank(ascending=False)
    rank_consistency= float(1-ranks.std(axis=1).mean()/12)
    return {
        'has_seasonality': bool(strength>0.15),
        'seasonality_strength': round(float(strength),3),
        'seasonal_index': seasonal_index,
        'peak_months': seasonal_index.nlargest(3).index.tolist(),
        'low_months': seasonal_index.nsmallest(3).index.tolist(),
        'monthly_by_year':monthly
    }


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

def analyze_discount_impact(df: pd.DataFrame) -> pd.DataFrame:
    """تحلیل جامع تأثیر تخفیف بر فروش و سودآوری."""
    _validate_columns(df, ['Discount', 'Sales', 'Profit'])
    
    discount_analysis = df.groupby('Discount').agg(
        order_count=('Profit', 'count'),           
        total_sales=('Sales', 'sum'),              
        total_profit=('Profit', 'sum'),            
        avg_profit=('Profit', 'mean'),             
        loss_orders=('Profit', lambda x: (x < 0).sum()) 
    ).reset_index()
    
    discount_analysis['loss_rate_%'] = (
        discount_analysis['loss_orders'] / discount_analysis['order_count'] * 100
    ).round(2)
    
    discount_analysis['profit_margin_%'] = (
        discount_analysis['total_profit'] / discount_analysis['total_sales'] * 100
    ).round(2)
    
    return discount_analysis

#Correlation Matrix
DEFAULT_CORR_COLS=["Sales", "Quantity", "Discount", "Profit"]
def compute_correlation( df:pd.DataFrame,
                        cols:Optional[list[str]]=None)->pd.DataFrame:
    cols=cols or DEFAULT_CORR_COLS
    _validate_columns(df, cols)
    return df[cols].corr()
def report_correlation(df,cols:Optional[list[str]]=None):
    _print_header("CORRELATION MATRIX")
    corr = compute_correlation(df,cols)
    print(corr.round(3))
    return PracticeResult("correlation", data=corr)


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
def get_skewnes(df:pd.DataFrame):
    col=['Sales', 'Profit', 'Quantity', 'Discount']
    print("\nSkewness:")
    print(df[col].skew())

def get_kurtosis(df:pd.DataFrame):
    col=['Sales', 'Profit', 'Quantity', 'Discount']
    print("\nkurtosis:")
    print(df[col].kurt())

def compute_loss_order(df: pd.DataFrame)->tuple[pd.DataFrame,pd.Series]:
    _validate_columns(df,["Profit", "Category", "Region"])
    loss=df[df["Profit"]<0]
    analysis=loss.groupby(["Category", "Region"])["Profit"].sum().sort_values()
    return loss,analysis

def analyze_loss_orders(df: pd.DataFrame,
                           show:bool=True)->PracticeResult:
    """ Loss-making orders by category and region."""
    _print_header("LOSS-MAKING ORDERS")
    loss,analysis = compute_loss_order(df)
    print(f"Total loss orders: {len(loss)}")
    print(f"Total loss amount: ${loss['Profit'].sum():,.2f}\n")
    return PracticeResult("loss_order", data=analysis)
 #Average shipping time   
def compute_shipping_stats(df: pd.DataFrame)->tuple[pd.Series,pd.Series]:
    _validate_columns(df,["Shipping Days"])
    days=df["Shipping Days"].dropna()
    return days.describe(),days


def practice_1_Shipping_time(
        df: pd.DataFrame,save_path:Optional[str]=None,show:bool=True
        )->PracticeResult:
    _print_header("Average SHIPPING TIME")
    stats, days=compute_shipping_stats(df)
    print(stats)
    return PracticeResult("shipping_time")

#Top 5 Sub-Categories
def compute_top_subcategories( df:pd.DataFrame, n:int=5 )->pd.Series:
    _validate_columns(df, ["Sub-Category", "Sales"])
    return df.groupby("Sub-Category")["Sales"].sum().nlargest(n)

def practice_3_top_subcategories(
        df:pd.DataFrame,
        save_path:Optional[str]=None,
        n:int=5,
    )->PracticeResult:
    _print_header("top")
    top=compute_top_subcategories(df,n=n)
    return PracticeResult("top_subcategories")

#Quarterly Sales
def compute_quarterly( df:pd.DataFrame)->pd.DataFrame:
    _validate_columns(df, ["Quarter", "Sales"])
    return (df.groupby("Quarter")["Sales"].sum().reset_index())
def practice_5_quarterly(df: pd.DataFrame, save_path: Optional[str] = None,
                         show:bool=True)->PracticeResult:
     _print_header("QUARTERLY SALES ANALYSIS")
     quarterly = compute_quarterly(df)
     print(quarterly)
     return PracticeResult("quarterly", data=quarterly)
