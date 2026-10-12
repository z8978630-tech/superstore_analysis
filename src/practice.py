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

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def practice_1_shipping_time(df: pd.DataFrame, save_path: str = None):
    """Exercise 1: Average shipping time."""
    print("=" * 60)
    print("EXERCISE 1 — AVERAGE SHIPPING TIME")
    print("=" * 60)
    print(df['Shipping Days'].describe())
    
    plt.figure(figsize=(10, 5))
    plt.hist(df['Shipping Days'].dropna(), bins=20,
             color='steelblue', edgecolor='black')
    plt.xlabel('Days')
    plt.ylabel('Frequency')
    plt.title('Shipping Duration Distribution', fontweight='bold')
    plt.axvline(df['Shipping Days'].mean(), color='red', linestyle='--',
                label=f"Mean = {df['Shipping Days'].mean():.1f} days")
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def practice_2_loss_orders(df: pd.DataFrame):
    """Exercise 2: Loss-making orders by category and region."""
    print("=" * 60)
    print("EXERCISE 2 — LOSS-MAKING ORDERS")
    print("=" * 60)
    loss = df[df['Profit'] < 0]
    print(f"Total loss orders: {len(loss)}")
    print(f"Total loss amount: ${loss['Profit'].sum():,.2f}\n")
    analysis = loss.groupby(['Category', 'Region'])['Profit'].sum()
    print(analysis.sort_values())
    return analysis


def practice_3_top_subcategories(df: pd.DataFrame, save_path: str = None):
    """Exercise 3: Top 5 sub-categories by sales."""
    print("=" * 60)
    print("EXERCISE 3 — TOP 5 SUB-CATEGORIES")
    print("=" * 60)
    top = df.groupby('Sub-Category')['Sales'].sum().nlargest(5)
    print(top)
    
    plt.figure(figsize=(10, 5))
    top.plot(kind='barh', color='teal', edgecolor='black')
    plt.xlabel('Total Sales ($)')
    plt.ylabel('Sub-Category')
    plt.title('Top 5 Sub-Categories by Sales', fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
    return top


def practice_4_segment_share(df: pd.DataFrame, save_path: str = None):
    """Exercise 4: Segment share of total sales."""
    print("=" * 60)
    print("EXERCISE 4 — SEGMENT SHARE")
    print("=" * 60)
    total = df['Sales'].sum()
    share = (df.groupby('Segment')['Sales'].sum() / total * 100).round(2)
    print(share)
    
    plt.figure(figsize=(8, 8))
    plt.pie(share.values, labels=share.index,
            autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('pastel', 3))
    plt.title('Customer Segment Share of Sales', fontweight='bold')
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
    return share


def practice_5_quarterly(df: pd.DataFrame, save_path: str = None):
    """Exercise 5: Quarterly sales analysis."""
    print("=" * 60)
    print("EXERCISE 5 — QUARTERLY SALES")
    print("=" * 60)
    quarterly = df.groupby('Quarter')['Sales'].sum().reset_index()
    print(quarterly)
    
    plt.figure(figsize=(10, 5))
    sns.barplot(data=quarterly, x='Quarter', y='Sales',
                hue='Quarter', palette='autumn', legend=False)
    plt.title('Sales by Quarter', fontweight='bold')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
    return quarterly


def practice_6_correlation(df: pd.DataFrame, save_path: str = None):
    """Exercise 6: Correlation matrix of numeric variables."""
    print("=" * 60)
    print("EXERCISE 6 — CORRELATION MATRIX")
    print("=" * 60)
    corr = df[['Sales', 'Quantity', 'Discount', 'Profit']].corr()
    print(corr.round(3))
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', square=True, linewidths=1)
    plt.title('Correlation Matrix', fontweight='bold')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
    return corr