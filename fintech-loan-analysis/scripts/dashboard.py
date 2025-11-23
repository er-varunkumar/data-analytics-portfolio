"""
Simple Dashboard Script for Loan Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def create_dashboard():
    print("📈 Creating Dashboard Visualizations...")
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    processed_path = project_root / "data" / "processed_data.csv"
    dashboard_dir = project_root / "dashboard"
    dashboard_dir.mkdir(exist_ok=True)
    
    if not processed_path.exists():
        print("Processed data not found!")
        return None
    
    try:
        df = pd.read_csv(processed_path)
        
        # Set up plotting style - FIXED
        plt.style.use('default')  # Use default style
        sns.set_style("whitegrid")  # Set seaborn style
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 12
        
        # 1. Loan Status Distribution
        if 'is_good_loan' in df.columns:
            plt.figure(figsize=(10, 6))
            status_counts = df['is_good_loan'].value_counts()
            colors = ['#ff6b6b', '#51cf66']  # Red for bad, green for good
            bars = plt.bar(['Bad Loans (0)', 'Good Loans (1)'], status_counts.values, color=colors, alpha=0.7)
            plt.title('Loan Status Distribution', fontsize=16, fontweight='bold')
            plt.xlabel('Loan Status')
            plt.ylabel('Number of Loans')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:,}', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig(dashboard_dir / 'loan_status_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created Loan Status Distribution chart")
        
        # 2. Loan Amount by Risk Category
        if 'risk_category' in df.columns and 'loan_amnt' in df.columns:
            plt.figure(figsize=(12, 6))
            # Use proper order for risk categories
            risk_order = ['Low', 'Medium', 'High'] if 'Low' in df['risk_category'].unique() else sorted(df['risk_category'].unique())
            sns.boxplot(data=df, x='risk_category', y='loan_amnt', order=risk_order, palette='viridis')
            plt.title('Loan Amount Distribution by Risk Category', fontsize=16, fontweight='bold')
            plt.xlabel('Risk Category')
            plt.ylabel('Loan Amount ($)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(dashboard_dir / 'loan_amount_by_risk.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created Loan Amount by Risk Category chart")
        
        # 3. Interest Rate by Grade
        if 'grade' in df.columns and 'int_rate' in df.columns:
            plt.figure(figsize=(12, 6))
            # Ensure proper grade order
            grade_order = ['A','B','C','D','E','F','G']
            available_grades = [g for g in grade_order if g in df['grade'].unique()]
            sns.boxplot(data=df, x='grade', y='int_rate', order=available_grades, palette='coolwarm')
            plt.title('Interest Rate Distribution by Loan Grade', fontsize=16, fontweight='bold')
            plt.xlabel('Loan Grade')
            plt.ylabel('Interest Rate (%)')
            plt.tight_layout()
            plt.savefig(dashboard_dir / 'interest_rate_by_grade.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created Interest Rate by Grade chart")
        
        # 4. Good Loan Rate by Risk Category
        if 'risk_category' in df.columns and 'is_good_loan' in df.columns:
            plt.figure(figsize=(10, 6))
            good_loan_rates = df.groupby('risk_category')['is_good_loan'].mean().sort_values(ascending=False)
            colors = ['#51cf66', '#ffd43b', '#ff6b6b']  # Green, Yellow, Red
            
            bars = plt.bar(range(len(good_loan_rates)), good_loan_rates.values * 100, 
                          color=colors[:len(good_loan_rates)], alpha=0.7)
            plt.title('Good Loan Rate by Risk Category', fontsize=16, fontweight='bold')
            plt.xlabel('Risk Category')
            plt.ylabel('Good Loan Rate (%)')
            plt.xticks(range(len(good_loan_rates)), good_loan_rates.index)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}%', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig(dashboard_dir / 'good_loan_rate_by_risk.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created Good Loan Rate by Risk Category chart")
        
        # 5. Loan Purpose Distribution (Top 10)
        if 'purpose' in df.columns:
            plt.figure(figsize=(12, 6))
            purpose_counts = df['purpose'].value_counts().head(10)
            colors = plt.cm.Set3(range(len(purpose_counts)))
            
            bars = plt.bar(range(len(purpose_counts)), purpose_counts.values, color=colors, alpha=0.7)
            plt.title('Top 10 Loan Purposes', fontsize=16, fontweight='bold')
            plt.xlabel('Loan Purpose')
            plt.ylabel('Number of Loans')
            plt.xticks(range(len(purpose_counts)), purpose_counts.index, rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 100,
                        f'{height:,}', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            plt.savefig(dashboard_dir / 'loan_purpose_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created Loan Purpose Distribution chart")
        
        # 6. Annual Income Distribution
        if 'annual_inc' in df.columns:
            plt.figure(figsize=(10, 6))
            # Remove extreme outliers for better visualization
            income_clean = df[df['annual_inc'] <= df['annual_inc'].quantile(0.95)]['annual_inc']
            plt.hist(income_clean, bins=50, color='skyblue', alpha=0.7, edgecolor='black')
            plt.title('Annual Income Distribution (95th percentile)', fontsize=16, fontweight='bold')
            plt.xlabel('Annual Income ($)')
            plt.ylabel('Number of Borrowers')
            plt.tight_layout()
            plt.savefig(dashboard_dir / 'annual_income_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Created Annual Income Distribution chart")
        
        # 7. Create a summary statistics chart
        plt.figure(figsize=(12, 8))
        
        # Calculate key metrics
        metrics = []
        values = []
        
        if 'is_good_loan' in df.columns:
            metrics.append('Good Loan Rate')
            values.append(df['is_good_loan'].mean() * 100)
        
        if 'loan_amnt' in df.columns:
            metrics.append('Avg Loan Amount ($)')
            values.append(df['loan_amnt'].mean())
        
        if 'int_rate' in df.columns:
            metrics.append('Avg Interest Rate (%)')
            values.append(df['int_rate'].mean())
        
        if 'annual_inc' in df.columns:
            metrics.append('Avg Annual Income ($)')
            values.append(df['annual_inc'].mean())
        
        if 'dti' in df.columns:
            metrics.append('Avg Debt-to-Income (%)')
            values.append(df['dti'].mean())
        
        # Create horizontal bar chart for metrics
        y_pos = range(len(metrics))
        colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f']
        
        bars = plt.barh(y_pos, values, color=colors[:len(metrics)], alpha=0.7)
        plt.yticks(y_pos, metrics)
        plt.title('Key Portfolio Metrics', fontsize=16, fontweight='bold')
        plt.xlabel('Value')
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            if 'Rate' in metrics[i] or 'Interest' in metrics[i]:
                plt.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                        f'{value:.1f}%', ha='left', va='center')
            elif 'Amount' in metrics[i] or 'Income' in metrics[i]:
                plt.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                        f'${value:,.0f}', ha='left', va='center')
            else:
                plt.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                        f'{value:.1f}', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(dashboard_dir / 'key_metrics_summary.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Created Key Metrics Summary chart")
        
        # Create dashboard index file
        dashboard_index = dashboard_dir / "dashboard_index.txt"
        with open(dashboard_index, 'w') as f:
            f.write("DASHBOARD VISUALIZATIONS INDEX\n")
            f.write("=" * 40 + "\n\n")
            f.write("Available Charts:\n")
            f.write("1. loan_status_distribution.png - Loan performance overview\n")
            f.write("2. loan_amount_by_risk.png - Loan sizes by risk category\n")
            f.write("3. interest_rate_by_grade.png - Interest rates by loan grade\n")
            f.write("4. good_loan_rate_by_risk.png - Performance by risk level\n")
            f.write("5. loan_purpose_distribution.png - Top loan purposes\n")
            f.write("6. annual_income_distribution.png - Borrower income distribution\n")
            f.write("7. key_metrics_summary.png - Key portfolio metrics\n")
        
        print("\n" + "=" * 60)
        print("✅ DASHBOARD CREATION COMPLETE!")
        print("=" * 60)
        print(f"📊 Charts saved in: {dashboard_dir}")
        print(f"📋 Index file: {dashboard_index}")
        print(f"🎨 Total charts created: 7")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_dashboard()