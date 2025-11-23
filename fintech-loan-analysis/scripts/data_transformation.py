"""
Simple Data Transformation Script for FinTech Loan Analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

def main():
    print("Starting Simple Data Transformation...")
    print("=" * 60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    cleaned_path = project_root / "data" / "cleaned_data.csv"
    processed_path = project_root / "data" / "processed_data.csv"
    results_dir = project_root / "results"
    
    print(f"Looking for cleaned data at: {cleaned_path}")
    
    if not cleaned_path.exists():
        print(f"ERROR: Cleaned data not found: {cleaned_path}")
        print("Run data_cleaning.py first!")
        return None
    
    try:
        # Load cleaned data
        print("Loading cleaned data...")
        df = pd.read_csv(cleaned_path, low_memory=False)
        print(f"Data shape: {df.shape}")
        
        # Transformations
        transformations = []
        new_features = []
        
        # 1. Target variable
        if 'loan_status' in df.columns:
            good_loans = ['Fully Paid', 'Current']
            df['is_good_loan'] = df['loan_status'].isin(good_loans).astype(int)
            good_count = df['is_good_loan'].sum()
            bad_count = len(df) - good_count
            transformations.append(f"Target: {good_count:,} good vs {bad_count:,} bad loans")
            new_features.append('is_good_loan')
        
        # 2. Risk categories
        if 'grade' in df.columns:
            risk_map = {'A': 'Low', 'B': 'Low', 'C': 'Medium', 'D': 'Medium', 'E': 'High', 'F': 'High', 'G': 'High'}
            df['risk_category'] = df['grade'].map(risk_map)
            transformations.append("Added risk categories")
            new_features.append('risk_category')
        
        # 3. Income ratio
        if 'annual_inc' in df.columns and 'loan_amnt' in df.columns:
            df['income_loan_ratio'] = df['annual_inc'] / df['loan_amnt']
            transformations.append("Added income to loan ratio")
            new_features.append('income_loan_ratio')
        
        # 4. Employment years
        if 'emp_length' in df.columns:
            df['emp_years'] = df['emp_length'].str.extract('(\d+)').fillna(0).astype(float)
            df.loc[df['emp_length'].str.contains('\+', na=False), 'emp_years'] = 10
            transformations.append("Converted employment length to years")
            new_features.append('emp_years')
        
        # 5. Loan size categories
        if 'loan_amnt' in df.columns:
            bins = [0, 5000, 15000, 25000, 35000, float('inf')]
            labels = ['Very Small', 'Small', 'Medium', 'Large', 'Very Large']
            df['loan_size_category'] = pd.cut(df['loan_amnt'], bins=bins, labels=labels)
            transformations.append("Added loan size categories")
            new_features.append('loan_size_category')
        
        # Save processed data
        df.to_csv(processed_path, index=False)
        
        # Generate report
        report_lines = []
        report_lines.append("DATA TRANSFORMATION REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("TRANSFORMATIONS")
        report_lines.append("-" * 15)
        for transform in transformations:
            report_lines.append(f"- {transform}")
        report_lines.append("")
        report_lines.append("NEW FEATURES")
        report_lines.append("-" * 12)
        for feature in new_features:
            report_lines.append(f"- {feature}")
        report_lines.append("")
        report_lines.append(f"Final dataset: {df.shape[0]:,} rows, {df.shape[1]} columns")
        
        report_path = results_dir / "transformation_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        # Print summary
        print("\n" + "=" * 60)
        print("TRANSFORMATION COMPLETE")
        print("=" * 60)
        print(f"New features: {len(new_features)}")
        print(f"Final data: {df.shape[0]:,} rows, {df.shape[1]} columns")
        print(f"Processed data: {processed_path}")
        print(f"All done! Ready for analysis.")
        
        return df
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    main()