"""
Test Script — Verifies all modules work correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

# Import modules
from data_loader import load_data
from data_cleaning import clean_data
from feature_engineering import add_time_features

print("✅ All imports successful!")

# Test with actual data
print("\n" + "=" * 60)
print("TESTING WITH REAL DATA")
print("=" * 60)

df = load_data('data/Sample-Superstore.xlsx')
df = clean_data(df)
df = add_time_features(df)

print("\n✅ Everything works!")
print(f"\nFinal data: {df.shape[0]} rows × {df.shape[1]} columns")