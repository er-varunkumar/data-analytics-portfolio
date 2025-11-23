"""
Exploratory Data Analysis Script
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def perform_eda():
    print("📊 Starting Exploratory Data Analysis...")
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    processed_path = project_root / "data" / "processed_data.csv"
    results_dir = project_root / "results"
    
    if not processed_path.exists():
        print("Processed data not found!")
        return None
    
    try:
        df = pd.read_csv(processed_path)
        
        # Basic analysis
        print("\n1. TARGET VARIABLE DISTRIBUTION")
        if 'is_good_loan' in df.columns:
            target_dist = df['is_good_loan'].value_counts()
            print(f"Good loans: {target_dist.get(1, 0):,} ({target_dist.get(1, 0)/len(df)*100:.1f}%)")
            print(f"Bad loans:  {target_dist.get(0, 0):,} ({target_dist.get(0, 0)/len(df)*100:.1f}%)")
        
        print("\n2. LOAN AMOUNT ANALYSIS")
        if 'loan_amnt' in df.columns:
            print(f"Average loan: ${df['loan_amnt'].mean():,.0f}")
            print(f"Min loan: ${df['loan_amnt'].min():,.0f}")
            print(f"Max loan: ${df['loan_amnt'].max():,.0f}")
        
        print("\n3. INTEREST RATE ANALYSIS")
        if 'int_rate' in df.columns:
            print(f"Average interest rate: {df['int_rate'].mean():.1f}%")
            print(f"Range: {df['int_rate'].min():.1f}% - {df['int_rate'].max():.1f}%")
        
        print("\n4. RISK CATEGORY BREAKDOWN")
        if 'risk_category' in df.columns:
            risk_counts = df['risk_category'].value_counts()
            for risk, count in risk_counts.items():
                print(f"{risk}: {count:,} loans ({count/len(df)*100:.1f}%)")
        
        # Save analysis report
        report_lines = []
        report_lines.append("EXPLORATORY DATA ANALYSIS REPORT")
        report_lines.append("=" * 50)
        
        if 'is_good_loan' in df.columns:
            report_lines.append(f"Good loan rate: {target_dist.get(1, 0)/len(df)*100:.1f}%")
        
        if 'risk_category' in df.columns:
            report_lines.append("\nRISK DISTRIBUTION:")
            for risk, count in risk_counts.items():
                report_lines.append(f"  {risk}: {count/len(df)*100:.1f}%")
        
        report_path = results_dir / "eda_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"\nEDA report saved: {report_path}")
        return df
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    perform_eda()