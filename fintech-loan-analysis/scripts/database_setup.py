"""
Database Setup Script for FinTech Loan Analysis
"""

import pandas as pd
import sqlite3
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def setup_database():
    print("🗄️  Setting up database...")
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    processed_path = project_root / "data" / "processed_data.csv"
    db_path = project_root / "database" / "loan_analysis.db"
    
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not processed_path.exists():
        print("ERROR: Processed data not found. Run data_transformation.py first!")
        return None
    
    try:
        # Load processed data
        print("Loading processed data...")
        df = pd.read_csv(processed_path)
        
        # Create SQLite database
        conn = sqlite3.connect(db_path)
        
        # Store data in database
        df.to_sql('loans', conn, if_exists='replace', index=False)
        
        # Create some useful views
        cursor = conn.cursor()
        
        # View for loan risk analysis
        cursor.execute('''
        CREATE VIEW IF NOT EXISTS loan_risk_analysis AS
        SELECT 
            risk_category,
            loan_size_category,
            AVG(int_rate) as avg_interest_rate,
            AVG(income_loan_ratio) as avg_income_ratio,
            AVG(is_good_loan) as good_loan_rate,
            COUNT(*) as loan_count
        FROM loans
        GROUP BY risk_category, loan_size_category
        ''')
        
        # View for borrower analysis
        cursor.execute('''
        CREATE VIEW IF NOT EXISTS borrower_analysis AS
        SELECT 
            home_ownership,
            emp_years,
            AVG(annual_inc) as avg_income,
            AVG(dti) as avg_dti,
            AVG(is_good_loan) as good_loan_rate,
            COUNT(*) as borrower_count
        FROM loans
        GROUP BY home_ownership, emp_years
        ''')
        
        conn.commit()
        conn.close()
        
        print("Database setup complete!")
        print(f"Database location: {db_path}")
        print("Tables created: loans")
        print("Views created: loan_risk_analysis, borrower_analysis")
        
        return db_path
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    setup_database()