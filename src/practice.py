"""
Exercises Module
----------------
Six bonus exercises from the course project:
1. Average shipping time
2. Loss-making orders
3. Top 5 sub-categories
4. Segment share
5. Quarterly analysis
6. Correlation matrix
"""

from __future__ import annotations
import inspect
import logging
import os
import sys 
from dataclasses import dataclass
from typing import Any,Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
logger=logging.getLogger(__name__)
__all__=[
    "PracticeResult",
    "practice_1_shipping_time",
    "practice_2_loss_orders",
    "practice_3_top_subcategories",
    "practice_4_segment_share",
    "practice_5_quarterly",
    "practice_6_correlation",
    "run_all"
]
@dataclass(frozen=True)
class PracticeResult:
    name:str
    date:Any=None
    figure:Optional[plt.figure]=None
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
def save_figure(fig:plt.figure,path:str, dpi:int=150)->None:
    fig.savefig(path,dpi=dpi)
    logger.info("figure save:%s", path)
def _finalize(fig:plt.figure,save_path:Optional[str], show:bool)->None:
    fig.tight_layout()
    if save_path:
        save_figure(fig, save_path)
    if show:
        plt.show()
 #Average shipping time   
def compute_shipping_stats(df: pd.DataFrame)->tuple[pd.Series,pd.Series]:
    _validate_columns(df,["Shipping Days"])
    days=df["Shipping Days"].dropna()
    return days.describe(),days
def plot_shipping_distribution(days:pd.Series)->plt.figure:
    fig,ax=plt.subplots(figsize=(10, 5))
    ax.hist(days,bins=20, color="steelblue", edgecolor="black")
    ax.set_xlabel('Days')
    ax.set_ylabel('Frequency')
    ax.set_title('Shipping Duration Distribution', fontweight='bold')
    ax.axvline(days.mean(), color='red', linestyle='--',
                label=f"Mean = {days.mean():.1f} days")
    ax.legend()
    return fig


def practice_1_Shipping_time(
        df: pd.DataFrame,save_path:Optional[str]=None,show:bool=True
        )->PracticeResult:
    _print_header("Average SHIPPING TIME")
    stats, days=compute_shipping_stats(df)
    print(stats)
    fig=plot_shipping_distribution(days)
    _finalize(fig,save_path,show)
    return PracticeResult("shipping_time",date=days, figure=fig, stats=stats)


#Losس_making Orders
def compute_loss_order(df: pd.DataFrame)->tuple[pd.series,pd.series]:
    _validate_columns(df,["Profit", "Category", "Region"])
    loss=df[df["Profit"]<0]
    analysis=loss.groupby(["Category", "Region"])["Profit"].sum().sort_values()
    return loss,analysis

def analysis_loss_orders(df: pd.DataFrame,
                           show:bool=True)->PracticeResult:
    """ Loss-making orders by category and region."""
    _print_header(" LOSS-MAKING ORDERS")
    loss,analysis = compute_loss_order(df)
    print(f"Total loss orders: {len(loss)}")
    print(f"Total loss amount: ${loss['Profit'].sum():.2f}\n")
    return PracticeResult("loss_order", data=analysis)
#Top 5 Sub-Categories
def compute_top_subcategories( df:pd.DataFrame, n:int=5 )->pd.series:
    _validate_columns(df, ["Sub-Category", "Sales"])
    return df.groupby("Sub-Category")["Sales"].sum().nlargest(n)
 
def plot_top_subcategories(
        data:pd.Series,
        title:str="Top 5 Sub-Categories by Sales",
        color:str="teal"
    )->plt.figure:
    fig,ax=plt.subplots(figsize=(10, 5))
    data.plot(kind="barh", color=color, edgecolor="Black", ax=ax)
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("Sub-Cateory")
    ax.set_title(title,fontweight="bold")
    ax.invert_yaxis()
    fig.tight_layout()
    return fig
def practice_3_top_subcategories(
        df:pd.DataFrame,
        save_path:Optional[str]=None,
        n:int=5,
        show:bool=True,
    )->PracticeResult:
    _print_header("top")
    top=compute_top_subcategories(df,n=n)
    print(top)
    fig=plot_top_subcategories(top,title=f"Top {n} Sub-Categories by sales")
    _finalize(fig,save_path, show)
    return PracticeResult("top_subcategories", data=top, figure=fig)
#Segment share
def compute_segment_share( df:pd.DataFrame)->pd.Series:
    _validate_columns(df, ["Segment", "Sales"])
    total=df["Sales"].sum()
    return (df.groupby("Category")["Sales"].sum()/total*100).round(2)
def plot_segment_share(share:pd.Series)->plt.figure:
    fig,ax=plt.subplots(figsize=(8, 8))
    ax.pie(share.values, labels=share.index,
            autopct="%1.1f%%", startangle=90,
            colors=sns.color_palette("pastel", len(share)))
    ax.set_title("Customer Segment Share of Sales", fontweight="bold")
    return fig
def practice_4_segment_share(df: pd.DataFrame, save_path:Optional[str] = None,
                             show:bool=True)->PracticeResult:
     _print_header("SEGMENT SHARE")
     share = compute_segment_share(df)
     print(share)
     fig=plot_segment_share(share)
     _finalize(fig, save_path, show)
     return PracticeResult("segment_share", data=share, figure=fig)
#Quarterly Sales
def compute_quarterly( df:pd.DataFrame)->pd.DataFrame:
    _validate_columns(df, ["Quarter", "Sales"])
    total=df["Sales"].sum()
    return (df.groupby("Quarter")["Sales"].sum().reset_index())
def plot_quarterly(quarterly:pd.Series)->plt.figure:
    fig,ax=plt.subplots(figsize=(10,5))
    sns.barplot(data=quarterly, x="Quarter",
            y="Sales", hue="Quarter", palette="autumn",legend=False, ax=ax)
    ax.set_title("Sales by Quarter", fontweight="bold")
    return fig
def practice_5_quarterly(df: pd.DataFrame, save_path: Optional[str] = None,
                         show:bool=True)->PracticeResult:
     _print_header("QUARTERLY SALES ANALYSIS")
     quarterly = compute_quarterly(df)
     print(quarterly)
     fig=plot_quarterly(quarterly)
     _finalize(fig, save_path,show)
     return PracticeResult("quarterly", data=quarterly, figure=fig )

#Correlation Matrix
DEFAULT_CORR_COLS=["Sales", "Quantity", "Discount", "Profit"]
def compute_correlation( df:pd.DataFrame,
                        cols:Optional[list[str]]=None)->pd.DataFrame:
    cols=cols or DEFAULT_CORR_COLS
    _validate_columns(df, cols)
    return df[cols].corr()
def plot_correlation(corr:pd.Series)->plt.figure:
    fig,ax=plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True,cmap="coolwarm",center=0,
            fmt=".2f", square=True, linewidths=1,ax=ax)
    ax.set_title("Correlation Matrix", fontweight="bold")
    return fig
def practice_6_correlation(df: pd.DataFrame, 
                           save_path:Optional[str] = None,
                           cols:Optional[list[str]]=None,
                           show:bool=True)->PracticeResult:
    _print_header("CORRELATION MATRIX")
    corr = compute_correlation(df,cols)
    print(corr.round(3))
    fig=plot_correlation(corr)
    _finalize(fig,save_path,show)
    return PracticeResult("correltion", data=corr, figure=fig)
# ═════════════════════════════════════════════
#  Runner — اجرای همه تمرین‌ها
# ═════════════════════════════════════════════

PRACTICES = {
    1: practice_1_Shipping_time,
    2: practice_2_loss_orders,
    3: practice_3_top_subcategories,
    4: practice_4_segment_share,
    5: practice_5_quarterly,
    6: practice_6_correlation,
}


def run_all(df: pd.DataFrame,
            save_dir: Optional[str] = None,
            show: bool = False) -> dict[int, PracticeResult]:
    """
    همه تمرین‌ها را اجرا می‌کند.
    فقط تمرین‌هایی که پارامتر save_path دارند، تصویر ذخیره می‌کنند.
    """
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    results: dict[int, PracticeResult] = {}
    for i, fn in PRACTICES.items():
        kwargs: dict[str, Any] = {"show": show}
        if "save_path" in inspect.signature(fn).parameters:
            kwargs["save_path"] = (
                f"{save_dir}/practice_{i}.png" if save_dir else None
            )
        results[i] = fn(df, **kwargs)
    return results