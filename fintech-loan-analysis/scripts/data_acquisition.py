# this will directly get data from kaggle source
import kagglehub
import pandas as pd
import os
import shutil
from pathlib import Path

def download_lending_club_data():
    """
    Download Lending Club loan data from Kaggle and save to data folder
    """
    try:
        print("Downloading Lending Club dataset from Kaggle...")
        
        # Download the dataset
        path = kagglehub.dataset_download("adarshsng/lending-club-loan-data-csv")
        print(f"Dataset downloaded to: {path}")
        
        # List files in the downloaded directory
        files = os.listdir(path)
        print(f"Files in dataset: {files}")
        
        # Create data folder if it doesn't exist
        data_folder = Path("data/raw")
        data_folder.mkdir(parents=True, exist_ok=True)

        # Find the main CSV file
        csv_files = [f for f in files if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV files found in the dataset")
        
        main_csv = csv_files[0]  # Usually the first CSV is the main data
        source_file_path = Path(path) / main_csv
        destination_file_path = data_folder / main_csv
        
        print(f"Moving data from: {source_file_path} to {destination_file_path}")
        
        # Move the CSV file to data folder
        shutil.move(str(source_file_path), str(destination_file_path))
        print(f"Moved: {main_csv} to data folder")
        
        # Load the data with appropriate data types to handle memory
        print("Loading dataset into pandas...")
        df = pd.read_csv(destination_file_path, low_memory=False)
        
        print(f"Dataset loaded successfully! Shape: {df.shape}")
        print(f"Columns: {len(df.columns)} columns")
        
        # Save a processed copy with consistent naming
        processed_path = data_folder / 'lending_club_raw.csv'
        df.to_csv(processed_path, index=False)
        print(f"Data saved to: {processed_path}")
        
        return df
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

def explore_dataset(df):
    """
    Basic exploration of the dataset
    """
    print("\n" + "="*50)
    print("DATASET EXPLORATION")
    print("="*50)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nColumn data types:")
    print(df.dtypes.value_counts())
    
    print("\nMissing values by column (top 10):")
    missing_data = df.isnull().sum().sort_values(ascending=False).head(10)
    print(missing_data)
    
    # Key columns to check for in Lending Club data
    key_columns = ['loan_amnt', 'term', 'int_rate', 'grade', 'emp_length', 
                   'home_ownership', 'annual_inc', 'loan_status']
    
    available_key_columns = [col for col in key_columns if col in df.columns]
    print(f"\nKey columns present: {available_key_columns}")
    
    # Check for missing key columns
    missing_key_columns = [col for col in key_columns if col not in df.columns]
    if missing_key_columns:
        print(f"Warning: Missing key columns: {missing_key_columns}")
    
    return df

if __name__ == "__main__":
    # Download and explore the data
    loan_data = download_lending_club_data()
    
    if loan_data is not None:
        explore_dataset(loan_data)
    else:
        print("Failed to download dataset")