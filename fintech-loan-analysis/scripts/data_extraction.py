"""
Simple Data Extraction Script for FinTech Loan Analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

def main():
    print("🚀 Starting Simple Data Extraction...")
    print("=" * 60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_path = project_root / "data" / "raw" / "lending_club_raw.csv"
    results_dir = project_root / "results"
    
    results_dir.mkdir(exist_ok=True)
    
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
        # Load data with sampling
        print("Loading dataset...")
        df = pd.read_csv(data_path, low_memory=False)
        original_size = len(df)
        df = df.sample(frac=0.1, random_state=42)
        print(f"Sampled data: {len(df):,} rows (10% of {original_size:,})")
        
        # Generate report content
        report_lines = []
        report_lines.append("DATA EXTRACTION REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Basic info
        report_lines.append("BASIC INFORMATION")
        report_lines.append("-" * 20)
        report_lines.append(f"Rows: {df.shape[0]:,}")
        report_lines.append(f"Columns: {df.shape[1]}")
        report_lines.append(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        report_lines.append("")
        
        # Data types
        report_lines.append("DATA TYPES")
        report_lines.append("-" * 20)
        for dtype, count in df.dtypes.value_counts().items():
            report_lines.append(f"{str(dtype)}: {count} columns")
        report_lines.append("")
        
        # Missing values
        report_lines.append("MISSING VALUES")
        report_lines.append("-" * 20)
        missing_total = df.isnull().sum().sum()
        missing_cols = (df.isnull().sum() > 0).sum()
        missing_50 = ((df.isnull().sum() / len(df)) > 0.5).sum()
        report_lines.append(f"Total missing: {missing_total:,}")
        report_lines.append(f"Columns with missing: {missing_cols}")
        report_lines.append(f"Columns >50% missing: {missing_50}")
        report_lines.append("")
        
        # Key columns - FIXED: No special characters
        report_lines.append("KEY COLUMNS CHECK")
        report_lines.append("-" * 20)
        key_cols = ['loan_amnt', 'term', 'int_rate', 'grade', 'loan_status', 'emp_length', 'annual_inc']
        available_count = 0
        for col in key_cols:
            if col in df.columns:
                report_lines.append(f"[YES] {col}")
                available_count += 1
            else:
                report_lines.append(f"[NO]  {col}")
        report_lines.append(f"Available: {available_count}/{len(key_cols)} key columns")
        report_lines.append("")
        
        # First 10 columns
        report_lines.append("FIRST 10 COLUMNS")
        report_lines.append("-" * 20)
        for i, col in enumerate(df.columns[:10], 1):
            report_lines.append(f"{i}. {col}")
        
        # Save report with proper encoding
        report_path = results_dir / "extraction_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        # Print summary
        print("\n" + "=" * 60)
        print("EXTRACTION COMPLETE")
        print("=" * 60)
        print(f"Dataset: {df.shape[0]:,} rows, {df.shape[1]} columns")
        print(f"Missing values: {missing_total:,}")
        print(f"Available key columns: {available_count}/{len(key_cols)}")
        print(f"Report saved: {report_path}")
        print(f"Ready for data_cleaning.py")
        
        return df
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    main()