# Data Validation and Cleaning Helper Script
# Use this to validate your Excel data before training models

import pandas as pd
import numpy as np

def validate_and_clean_broker_data(file_path):
    """
    Validates and cleans broker data from Excel.
    Handles percentage columns and detects data quality issues.

    Parameters:
    -----------
    file_path : str
        Path to Excel file

    Returns:
    --------
    cleaned_df : DataFrame
        Cleaned dataframe ready for modeling
    report : dict
        Validation report with any issues found
    """

    print("="*70)
    print("BROKER DATA VALIDATION AND CLEANING")
    print("="*70)

    # Load data
    print(f"\n📂 Loading data from: {file_path}")
    df = pd.read_excel(file_path)
    print(f"✓ Loaded {df.shape[0]} rows × {df.shape[1]} columns")

    report = {
        'original_shape': df.shape,
        'issues': [],
        'warnings': [],
        'percentage_columns_cleaned': []
    }

    # 1. Detect and clean percentage columns
    print("\n" + "="*70)
    print("STEP 1: CLEANING PERCENTAGE COLUMNS")
    print("="*70)

    pct_columns = [col for col in df.columns if '%' in col]
    print(f"\nFound {len(pct_columns)} columns with '%' in name")

    for col in pct_columns:
        original_dtype = df[col].dtype

        # Check if column contains strings
        if df[col].dtype == 'object':
            print(f"\n⚠️  {col}: Contains string values, cleaning...")

            # Remove % symbols and convert to numeric
            df[col] = df[col].astype(str).str.replace('%', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')

            report['percentage_columns_cleaned'].append(col)
            print(f"   ✓ Converted to numeric")

        # Show value range
        col_data = df[col].dropna()
        if len(col_data) > 0:
            print(f"\n   {col}:")
            print(f"     Min: {col_data.min():.2f}")
            print(f"     Max: {col_data.max():.2f}")
            print(f"     Mean: {col_data.mean():.2f}")

            # Detect scale
            if col_data.max() > 10:
                print(f"     Scale: Percentage format (0-100+) ✓")
            elif col_data.max() <= 1.5:
                print(f"     Scale: Decimal format (0-1) ✓")

            # Warn about extreme values
            if col_data.max() > 500:
                warning = f"{col} has very high values (max: {col_data.max():.0f}%)"
                report['warnings'].append(warning)
                print(f"     ⚠️  Very high percentages detected (max: {col_data.max():.0f}%)")
                print(f"        This is OK if expected in your business logic!")

    # 2. Check for missing values
    print("\n" + "="*70)
    print("STEP 2: CHECKING MISSING VALUES")
    print("="*70)

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if len(missing) > 0:
        print(f"\nFound missing values in {len(missing)} columns:")
        print(missing.head(10))

        # Flag critical missing values
        critical_cols = ['Account Name', 'Month', 'Competitor Loans this Month']
        for col in critical_cols:
            if col in missing.index:
                issue = f"Missing values in critical column: {col}"
                report['issues'].append(issue)
                print(f"\n❌ CRITICAL: {issue}")
    else:
        print("\n✅ No missing values found!")

    # 3. Check data types
    print("\n" + "="*70)
    print("STEP 3: VALIDATING DATA TYPES")
    print("="*70)

    print("\nColumn data types:")
    dtype_summary = df.dtypes.value_counts()
    print(dtype_summary)

    # Check if numeric columns are actually numeric
    expected_numeric = ['Competitor Loans this Month', 'UWM GR (9 Mo)',
                       'Google Reviews (since Jan 1, 2022)', 'UWM Loans (9 Mo)']

    for col in expected_numeric:
        if col in df.columns:
            if df[col].dtype == 'object':
                issue = f"{col} is stored as text instead of number"
                report['issues'].append(issue)
                print(f"\n❌ {issue}")

                # Try to convert
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    print(f"   ✓ Converted to numeric")
                except:
                    print(f"   ❌ Could not convert")

    # 4. Validate months
    print("\n" + "="*70)
    print("STEP 4: VALIDATING MONTH DATA")
    print("="*70)

    if 'Month' in df.columns:
        unique_months = df['Month'].unique()
        print(f"\nFound {len(unique_months)} unique months:")
        print(sorted(unique_months))

        if len(unique_months) < 6:
            warning = f"Only {len(unique_months)} months of data (recommend 6+)"
            report['warnings'].append(warning)
            print(f"\n⚠️  {warning}")
        else:
            print(f"\n✅ Sufficient training data ({len(unique_months)} months)")

    # 5. Check for duplicates
    print("\n" + "="*70)
    print("STEP 5: CHECKING FOR DUPLICATES")
    print("="*70)

    if 'Account Name' in df.columns and 'Month' in df.columns:
        duplicates = df.duplicated(subset=['Account Name', 'Month'], keep=False)
        dup_count = duplicates.sum()

        if dup_count > 0:
            issue = f"Found {dup_count} duplicate broker-month combinations"
            report['issues'].append(issue)
            print(f"\n❌ {issue}")
            print("\nDuplicate examples:")
            print(df[duplicates][['Account Name', 'Month']].head())
        else:
            print("\n✅ No duplicates found!")

    # Final report
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)

    print(f"\n📊 Final data shape: {df.shape}")

    if report['issues']:
        print(f"\n❌ Found {len(report['issues'])} critical issues:")
        for i, issue in enumerate(report['issues'], 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ No critical issues found!")

    if report['warnings']:
        print(f"\n⚠️  {len(report['warnings'])} warnings:")
        for i, warning in enumerate(report['warnings'], 1):
            print(f"   {i}. {warning}")

    if report['percentage_columns_cleaned']:
        print(f"\n🔧 Cleaned {len(report['percentage_columns_cleaned'])} percentage columns")

    print("\n" + "="*70)

    if not report['issues']:
        print("✅ DATA IS READY FOR MODELING!")
    else:
        print("⚠️  PLEASE FIX CRITICAL ISSUES BEFORE MODELING")

    print("="*70)

    return df, report


# Example usage:
if __name__ == "__main__":
    # Test the validation
    file_path = '../data/raw/Master_One_Sheet.xlsx'

    try:
        cleaned_data, validation_report = validate_and_clean_broker_data(file_path)

        # Save cleaned data
        output_path = '../data/interim/cleaned_broker_data.xlsx'
        cleaned_data.to_excel(output_path, index=False)
        print(f"\n💾 Cleaned data saved to: {output_path}")

    except FileNotFoundError:
        print(f"\n❌ File not found: {file_path}")
        print("Please ensure your Excel file is in the correct location.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
