"""
Visualization Module
--------------------
Functions for creating all charts and the GridSpec dashboard.
"""

import os
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots
from .eda import analyze_seasonality
def _base_plotly_layout(fig, title="", height=500, width=800):
    fig.update_layout(
        template="plotly_white",
        title_text=title,
        title_x=0.5,
        height=height,
        width=width,
    )
    return fig

def _finalize_mpl(fig:go.Figure, save_path:Optional[str]=None,show:bool=True)->None:
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
def _validate_columns(df:pd.DataFrame, required: list[str]):
    missing=[c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"DataFrame:{missing}")
def save_interactive_html(fig:go.Figure, filename:str, output_dir:str="outputs")->str:
    os.makedirs(output_dir,exist_ok=True)
    filepath=os.path.join(output_dir, f"{filename}.html")
    fig.write_html(filepath)
    return filepath
#Static plots (Matplotlib/seaborn)

def plot_boxplot(df, save_path= None, show:bool=True):
    """Plot monthly sales and profit trend."""
    cols=['Sales', 'Profit', 'Quantity', 'Discount']
    fig,axes=plt.subplots(2, 2,figsize=(14, 5))
    axes=axes.flatten()
    for i , col in enumerate(cols):
        ax=axes[i]
        sns.boxplot(y=df[col], ax=ax, color='steelblue')
        ax.set_title(f'Boxplot of {col}', fontweight='bold')
        ax.set_ylabel('Values')
        ax.set_xlabel(col)
 
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    _finalize_mpl(fig,save_path,show)
    return fig

def plot_monthly_trend(monthly: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot monthly sales trend."""
    fig,ax=plt.subplots(figsize=(14, 5))
    ax.plot(monthly['Month_Year'], monthly['total_sales'],
             marker='o', label='Sales', color='steelblue', linewidth=2)
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title('Monthly Sales Trend', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')
    ax.legend()
    plt.grid(True, alpha=0.3)
    _finalize_mpl(fig,save_path,show)
    return fig

def plot_monthly_profit_trend(monthly: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot monthly profit trend."""
    fig,ax=plt.subplots(figsize=(14, 5))
    ax.plot(monthly['Month_Year'], monthly['total_profit'],
             marker='o', label='Profit', color='steelblue', linewidth=2)
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title('Monthly Profit Trend', fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')

    ax.legend()
    plt.grid(True, alpha=0.3)
    _finalize_mpl(fig,save_path,show)
    return fig

def plot_seasonal_trend(df: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot seasonal trend."""
    season=analyze_seasonality(df)
    seasonal_idx=season['seasonal_index']
    fig,ax=plt.subplots(figsize=(14, 5))
    colors=['#2ecc71' if v>1 else '#e74c3c' for v in seasonal_idx.values]
    ax.bar(seasonal_idx.index.astype(str), seasonal_idx.values, color=colors, alpha=0.8)
    ax.axhline(1, color='black', linestyle='--',label='Average(1.0)')
    ax.set_xlabel('Month')
    ax.set_ylabel('Seasonal Index')

    plt.legend()
    plt.grid(True, alpha=0.3)
    _finalize_mpl(fig,save_path,show)
    return fig


def plot_category_performance(cat: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot Sales and Profit by Category side-by-side."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.barplot(data=cat, x='Category', y='total_sales',
                hue='Category', palette='Blues_d', legend=False, ax=axes[0])
    axes[0].set_title('Sales by Category', fontweight='bold')
    axes[0].set_ylabel("Sales($)")
    sns.barplot(data=cat, x='Category', y='total_profit',
                hue='Category', palette='Greens_d', legend=False, ax=axes[1])
    axes[1].set_title('Profit by Category', fontweight='bold')
    axes[1].set_ylabel("Profit ($")
    _finalize_mpl(fig, save_path, show)
    return fig
def plot_top_subcategories(data: pd.Series, save_path: str = None, show: bool = True) -> plt.Figure:
    """رسم نمودار میله‌ای افقی برای زیردسته‌بندی‌های برتر."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data.plot(kind='barh', color='#2E7D32', edgecolor='black', ax=ax)
    
    # تنظیمات ظاهری
    ax.set_title('Top 5 Sub-Categories by Total Sales', fontweight='bold', fontsize=14)
    ax.set_xlabel('Total Sales ($)', fontsize=12)
    ax.set_ylabel('Sub-Category', fontsize=12)
    
    # برعکس کردن محور Y تا بزرگترین مورد در بالای نمودار قرار بگیرد
    # ax.invert_yaxis()
    
    # اضافه کردن خطوط راهنما در پس‌زمینه
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # اضافه کردن برچسب اعداد روی هر میله (برای خوانایی بهتر)
    for i, v in enumerate(data.values):
        ax.text(v + (v * 0.01), i, f"${v:,.0f}", va='center', fontweight='bold')

    _finalize_mpl(fig, save_path, show)
    return fig

def plot_regional_performance(region: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot Sales, Profit, and Margin by Region (3 charts)."""
    _validate_columns(region, ['Region', 'total_sales'])
    fig, ax = plt.subplots(figsize=(14, 5))
   
    ax.pie(
        region['total_sales'], 
        labels=region['Region'], 
        autopct='%1.1f%%',       # نمایش درصد با یک رقم اعشار
        startangle=90,           # زاویه شروع برای زیبایی
        colors=sns.color_palette('pastel', len(region)), # رنگ‌های پاستلی
        wedgeprops={'edgecolor': 'white', 'linewidth': 2} # خط سفید بین برش‌ها
        )
    ax.set_title('Regional Market Share of Sales', fontweight='bold', fontsize=14)
    _finalize_mpl(fig, save_path, show)
    return fig


def plot_discount_vs_profit(df: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot relationship between discount and profit."""
    fig,ax=plt.subplots(figsize=(10, 5))
    sns.regplot(data=df, x='Discount', y='Profit',
                scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'}, ax=ax)
    ax.set_title('Discount vs Profit', fontweight='bold')
    _finalize_mpl(fig, save_path, show)
    return fig

def plot_correlation_heatmap(corr_matrix: pd.DataFrame, save_path: str = None, show: bool = True)->plt.figure:
    """Plot relationship between discount and profit."""
    fig,ax=plt.subplots(figsize=(10, 5))
    sns.heatmap(corr_matrix, 
                annot=True, 
                cmap='coolwarm', 
                center=0, 
                fmt='.2f', 
                linewidths=0.5, 
                ax=ax)
    ax.set_title('Correlation Matrix (ماتریس همبستگی)', fontweight='bold', fontsize=14)
    _finalize_mpl(fig, save_path, show)
    return fig
def plot_segment_share(segment: pd.DataFrame, save_path: str = None, show:bool=True)->plt.figure:
    """Plot segment share as pie chart."""
    fig,ax=plt.subplots(figsize=(8, 8))
    ax.pie(segment['Sales'], labels=segment['Segment'],
            autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('pastel', 3))
    ax.set_title('Customer Segment Share of Sales', fontweight='bold')
    _finalize_mpl(fig,save_path, show)
    return fig
#-----------------------------------------
#DAshbord(Matplotlb GripSpec)
#-----------------------------------------
def _draw_monthly_ax(ax,monthly):
    ax.plot(monthly["Month_Year"], monthly["total_sales"], "b-o",linewidth=2)
    ax.set_title("Monthly Sales Trend",fontweight='bold')
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(alpha=0.3)
def _draw_category_ax(ax,cat):
    ax.barplot(data=cat, x='Category', y='total_sales', hue='Category', palette='viridis', legend=False, ax=ax)
    ax.set_title("Sales by Category",fontweight='bold')
    ax.set_ylabel('Sales ($)')
def _draw_region_ax(ax,region):
    ax.pie(region['total_sales'], labels=region['Region'], autopct='%1.1f%%', startangle=90)
    ax.set_title("Regional Market Share",fontweight='bold')

def _draw_discount_ax(ax,df):
    sns.regplot(data=df, x='Discount', y='Profit', scatter_kws={'alpha:0.3'}, line_kws={'color':'red'}, ax=ax)
    ax.set_title("Discount vs Profit",fontweight='bold')
    ax.set_ylabel('Sales ($)')

    
def _draw_segment_ax(ax,segment):
    sns.barplot(data=segment, x='Segment', y='Sales', hue='Segment', palette='pastel', legend=False, ax=ax)
    ax.set_title("Sales by Segment",fontweight='bold')
    ax.set_ylabel('Sales ($)')

def plot_dashboard(monthly, cat, region, df, segment, save_path:str=None,show:bool=True)->plt.figure:
    fig=plt.figure(figsize=(16,12))
    gs=fig.add_gridspec(3, 2, heigt_ratios=[1, 1, 1], width_ratios=[1.5,1])
    _draw_monthly_ax(fig.add_subplot(gs[0,:],monthly))
    _draw_category_ax(fig.add_subplot(gs[1,0], cat))
    _draw_region_ax(fig.add_subplot(gs[1,1], region))
    _draw_discount_ax(fig.add_subplot(gs[2,0], df))
    _draw_segment_ax(fig.add_subplot(gs[2,1], segment))
    _finalize_mpl(fig,save_path,show)
    return fig

# ==========================================
# بخش ۳: داشبورد Matplotlib
# ==========================================

def plot_dashboard(monthly, cat, region, df, segment, save_path=None, show=True):
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], width_ratios=[1.5, 1])

    # 1. Monthly Sales Trend
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(monthly['Month_Year'], monthly['total_sales'], 'b-o', linewidth=2)
    ax1.set_title('Monthly Sales Trend', fontweight='bold')
    ax1.tick_params(axis='x', labelrotation=45)
    ax1.grid(alpha=0.3)

    # 2. Sales by Category
    ax2 = fig.add_subplot(gs[1, 0])
    sns.barplot(data=cat, x='Category', y='total_sales', hue='Category', palette='viridis', legend=False, ax=ax2)
    ax2.set_title('Sales by Category', fontweight='bold')
    ax2.set_ylabel('Sales ($)')

    # 3. Regional Market Share
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.pie(region['total_sales'], labels=region['Region'], autopct='%1.1f%%', startangle=90)
    ax3.set_title('Regional Market Share', fontweight='bold')

    # 4. Discount vs Profit
    ax4 = fig.add_subplot(gs[2, 0])
    sns.regplot(data=df, x='Discount', y='Profit', scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'}, ax=ax4)
    ax4.set_title('Discount vs Profit', fontweight='bold')

    # 5. Sales by Segment
    ax5 = fig.add_subplot(gs[2, 1])
    sns.barplot(data=segment, x='Segment', y='Sales', hue='Segment', palette='pastel', legend=False, ax=ax5)
    ax5.set_title('Sales by Segment', fontweight='bold')
    ax5.set_ylabel('Sales ($)')

    _finalize_mpl(fig, save_path, show)
    return fig


# ==========================================
# interactve
# ==========================================

def create_superstore_dashboard(df):
    """ساخت داشبورد ترکیبی با Plotly"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("فروش بر اساس دسته‌بندی", "سود بر اساس منطقه", "توزیع سود", "سهم بازار")
    )

    bar_data = df.groupby('Category')['Sales'].sum().reset_index()
    fig.add_trace(go.Bar(x=bar_data['Category'], y=bar_data['Sales'], name="فروش"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Sales'], y=df['Profit'], mode='markers', name="سود و فروش"), row=1, col=2)
    fig.update_layout(
        height=800, width=1000, 
        title_text="داشبورد مدیریتی Sample Superstore",
        template="plotly_white", showlegend=False
    )
    return fig

def plot_bar(df, x, y, color, title, **kwargs):
    fig = px.bar(df, x=x, y=y, color=color, **kwargs)
    return _base_plotly_layout(fig, title)

def plot_bar(df, x, y, color=None, title="", **kwargs):
    fig = px.bar(df, x=x, y=y, color=color, **kwargs)
    return _base_plotly_layout(fig, title)

def plot_scatter(df, x, y, color, title, **kwargs):
    fig = px.scatter(df, x=x, y=y, color=color, **kwargs)
    return _base_plotly_layout(fig, title)

def plot_histogram(df, x, y=None, color=None, title="", **kwargs):
    fig = px.histogram(df, x=x, y=y, color=color, **kwargs)
    return _base_plotly_layout(fig, title)

 #Average shipping time   
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
#Top 5 Sub-Categories
 
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


#Quarterly Sales
def plot_quarterly(quarterly:pd.Series)->plt.figure:
    fig,ax=plt.subplots(figsize=(10,5))
    sns.barplot(data=quarterly, x="Quarter",
            y="Sales", hue="Quarter", palette="autumn",legend=False, ax=ax)
    ax.set_title("Sales by Quarter", fontweight="bold")
    return fig

#Correlation Matrix
DEFAULT_CORR_COLS=["Sales", "Quantity", "Discount", "Profit"]
def plot_correlation(corr:pd.Series)->plt.figure:
    fig,ax=plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True,cmap="coolwarm",center=0,
            fmt=".2f", square=True, linewidths=1,ax=ax)
    ax.set_title("Correlation Matrix", fontweight="bold")
    return fig