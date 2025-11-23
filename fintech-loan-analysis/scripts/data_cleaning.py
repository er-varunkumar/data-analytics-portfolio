"""
Simple Data Cleaning Script for FinTech Loan Analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

def main():
    print("Starting Simple Data Cleaning...")
    print("=" * 60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_path = project_root / "data" / "raw" / "lending_club_raw.csv"
    cleaned_path = project_root / "data" / "cleaned_data.csv"
    results_dir = project_root / "results"
    
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Looking for data at: {data_path}")
    
    if not data_path.exists():
        print(f"ERROR: Data file not found: {data_path}")
        print("Available files in data/raw/:")
        raw_dir = project_root / "data" / "raw"
        if raw_dir.exists():
            for file in raw_dir.iterdir():
                print(f"  - {file.name}")
        return None
    
    try:
        # Load data
        print("Loading dataset...")
        df = pd.read_csv(data_path, low_memory=False)
        original_shape = df.shape
        print(f"Original: {original_shape[0]:,} rows, {original_shape[1]} cols")
        
        # Cleaning steps
        steps = []
        
        # 1. Remove empty columns
        start_cols = len(df.columns)
        df = df.dropna(axis=1, how='all')
        removed_empty = start_cols - len(df.columns)
        if removed_empty > 0:
            steps.append(f"Removed {removed_empty} empty columns")
        
        # 2. Remove high missing columns (>80%)
        missing_pct = df.isnull().sum() / len(df)
        high_missing = missing_pct[missing_pct > 0.8].index
        df = df.drop(columns=high_missing)
        if len(high_missing) > 0:
            steps.append(f"Removed {len(high_missing)} columns with >80% missing")
        
        # 3. Remove duplicates
        start_rows = len(df)
        df = df.drop_duplicates()
        removed_dupes = start_rows - len(df)
        if removed_dupes > 0:
            steps.append(f"Removed {removed_dupes} duplicate rows")
        
        # 4. Clean key columns
        key_cols = ['loan_amnt', 'term', 'int_rate', 'grade', 'loan_status']
        for col in key_cols:
            if col in df.columns:
                missing = df[col].isnull().sum()
                if missing > 0:
                    df = df.dropna(subset=[col])
                    steps.append(f"Removed {missing} rows with missing {col}")
        
        # 5. Convert percentages
        if 'int_rate' in df.columns:
            df['int_rate'] = df['int_rate'].astype(str).str.rstrip('%').astype(float)
            steps.append("Converted int_rate to numeric")
        
        if 'revol_util' in df.columns:
            df['revol_util'] = df['revol_util'].astype(str).str.rstrip('%').astype(float)
            steps.append("Converted revol_util to numeric")
        
        # Save cleaned data
        df.to_csv(cleaned_path, index=False)
        final_shape = df.shape
        
        # Generate report
        report_lines = []
        report_lines.append("DATA CLEANING REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("SUMMARY")
        report_lines.append("-" * 10)
        report_lines.append(f"Original: {original_shape[0]:,} rows, {original_shape[1]} cols")
        report_lines.append(f"Final:    {final_shape[0]:,} rows, {final_shape[1]} cols")
        report_lines.append(f"Reduction: {original_shape[0] - final_shape[0]:,} rows, {original_shape[1] - final_shape[1]} cols")
        report_lines.append("")
        report_lines.append("STEPS PERFORMED")
        report_lines.append("-" * 15)
        for step in steps:
            report_lines.append(f"- {step}")
        
        report_path = results_dir / "cleaning_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        # Print summary
        print("\n" + "=" * 60)
        print("CLEANING COMPLETE")
        print("=" * 60)
        print(f"Original: {original_shape[0]:,} rows, {original_shape[1]} cols")
        print(f"Final:    {final_shape[0]:,} rows, {final_shape[1]} cols")
        print(f"Steps applied: {len(steps)}")
        print(f"Cleaned data: {cleaned_path}")
        print(f"Ready for data_transformation.py")
        
        return df
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    main()