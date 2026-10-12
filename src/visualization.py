"""
Visualization Module
--------------------
Functions for creating all charts and the GridSpec dashboard.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_monthly_trend(monthly: pd.DataFrame, save_path: str = None):
    """Plot monthly sales and profit trend."""
    plt.figure(figsize=(14, 5))
    plt.plot(monthly['Month_Year'], monthly['total_sales'],
             marker='o', label='Sales', color='steelblue', linewidth=2)
    plt.plot(monthly['Month_Year'], monthly['total_profit'],
             marker='s', label='Profit', color='salmon', linewidth=2)
    plt.xticks(rotation=45)
    plt.title('Monthly Sales and Profit Trend', fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Amount ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def plot_category_performance(cat: pd.DataFrame, save_path: str = None):
    """Plot Sales and Profit by Category side-by-side."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.barplot(data=cat, x='Category', y='total_sales',
                hue='Category', palette='Blues_d', legend=False, ax=axes[0])
    axes[0].set_title('Sales by Category', fontweight='bold')
    axes[0].set_ylabel('Sales ($)')
    
    sns.barplot(data=cat, x='Category', y='total_profit',
                hue='Category', palette='Greens_d', legend=False, ax=axes[1])
    axes[1].set_title('Profit by Category', fontweight='bold')
    axes[1].set_ylabel('Profit ($)')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def plot_regional_performance(region: pd.DataFrame, save_path: str = None):
    """Plot Sales, Profit, and Margin by Region (3 charts)."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.barplot(data=region, x='Region', y='total_sales',
                hue='Region', palette='coolwarm', legend=False, ax=axes[0])
    axes[0].set_title('Total Sales by Region', fontweight='bold')
    axes[0].set_ylabel('Sales ($)')
    
    sns.barplot(data=region, x='Region', y='total_profit',
                hue='Region', palette='coolwarm', legend=False, ax=axes[1])
    axes[1].set_title('Total Profit by Region', fontweight='bold')
    axes[1].set_ylabel('Profit ($)')
    
    sns.barplot(data=region, x='Region', y='profit_margin_%',
                hue='Region', palette='coolwarm', legend=False, ax=axes[2])
    axes[2].set_title('Profit Margin by Region', fontweight='bold')
    axes[2].set_ylabel('Profit Margin (%)')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def plot_discount_vs_profit(df: pd.DataFrame, save_path: str = None):
    """Plot relationship between discount and profit."""
    plt.figure(figsize=(10, 5))
    sns.regplot(data=df, x='Discount', y='Profit',
                scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})
    plt.title('Discount vs Profit', fontweight='bold')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def plot_segment_share(segment: pd.DataFrame, save_path: str = None):
    """Plot segment share as pie chart."""
    plt.figure(figsize=(8, 8))
    plt.pie(segment['Sales'], labels=segment['Segment'],
            autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('pastel', 3))
    plt.title('Customer Segment Share of Sales', fontweight='bold')
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def plot_dashboard(monthly, cat, region, df, segment, save_path: str = None):
    """Create the 5-chart GridSpec dashboard."""
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
    sns.barplot(data=cat, x='Category', y='total_sales',
                hue='Category', palette='viridis', legend=False, ax=ax2)
    ax2.set_title('Sales by Category', fontweight='bold')
    ax2.set_ylabel('Sales ($)')
    
    # 3. Regional Market Share
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.pie(region['total_sales'], labels=region['Region'],
            autopct='%1.1f%%', startangle=90)
    ax3.set_title('Regional Market Share', fontweight='bold')
    
    # 4. Discount vs Profit
    ax4 = fig.add_subplot(gs[2, 0])
    sns.regplot(data=df, x='Discount', y='Profit',
                scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'}, ax=ax4)
    ax4.set_title('Discount vs Profit', fontweight='bold')
    
    # 5. Sales by Segment
    ax5 = fig.add_subplot(gs[2, 1])
    sns.barplot(data=segment, x='Segment', y='Sales',
                hue='Segment', palette='pastel', legend=False, ax=ax5)
    ax5.set_title('Sales by Segment', fontweight='bold')
    ax5.set_ylabel('Sales ($)')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()

# تابع جدید برای ساخت داشبورد
def create_superstore_dashboard(df):
    """ساخت داشبورد ترکیبی با Plotly Gridspec"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("فروش بر اساس دسته‌بندی", "سود بر اساس منطقه", 
                        "توزیع سود", "سهم بازار")
    )

    # ۲. اضافه کردن نمودارها به خانه‌های داشبورد
    # توجه: در اینجا از داده‌های df که به تابع پاس داده شده استفاده می‌کنیم
    
    
    bar_data = df.groupby('Category')['Sales'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=bar_data['Category'], y=bar_data['Sales'], name="فروش"),
        row=1, col=1
    )

    # نمودار ۲: پراکندگی (مثال)
    fig.add_trace(
        go.Scatter(x=df['Sales'], y=df['Profit'], mode='markers', name="سود و فروش"),
        row=1, col=2
    )

    # ۳. تنظیمات ظاهری داشبورد
    fig.update_layout(
        height=800, 
        width=1000, 
        title_text="داشبورد مدیریتی Sample Superstore",
        template="plotly_white",
        showlegend=False
    )

    return fig 
def save_interactive_html(fig, filename, output_dir="outputs"):
    """ذخیره نمودار تعاملی به صورت فایل HTML"""
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filepath = os.path.join(output_dir, f"{filename}.html")
    fig.write_html(filepath)
    print(f"✅ نمودار تعاملی با موفقیت در مسیر {filepath} ذخیره شد.")
def plot_bar(df, x, y, color=None, title="", **kwargs):
    fig=px.bar(df, x=x, y=y, color=color, **kwargs)
    fig.update_layout(
        template='plotly_white',
        title=title,
        title_x=0.5,
        height=500, 
        width=800
    )
    return fig
def plot_scatter(df, x, y, color=None, title="", **kwargs):
    fig=px.scatter(df, x=x, y=y, color=color, **kwargs)
    fig.update_layout(
        template='plotly_white',
        title=title,
        title_x=0.5,
        height=500, 
        width=800
    )
    return fig
def plot_histogram(df, x, y, color=None, title="", **kwargs):
    fig=px.histogram(df, x=x, y=y, color=color, **kwargs)
    fig.update_layout(
        template='plotly_white',
        title=title,
        title_x=0.5,
        height=500, 
        width=800
    )
    return fig
def save_interactive_html(fig,filename, output_dir="outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filepath=os.path.join(output_dir,f"{filename}.html")
    fig.write_html(filepath)