import pandas as pd
import glob
import os
from typing import Dict, List, Optional

class DataLoader:
    """
    Intelligent Data Loader for the UIDAI Hackathon.
    Handles multi-file CSV ingestion, schema unification, and basic cleanup.
    """
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        # Mapping friendly names to folder names
        self.categories = {
            "enrolment": "api_data_aadhar_enrolment",
            "demographic": "api_data_aadhar_demographic",
            "biometric": "api_data_aadhar_biometric"
        }

    def load_category(self, category: str) -> pd.DataFrame:
        """
        Loads all CSV files for a specific category into a single DataFrame.
        """
        if category not in self.categories:
            raise ValueError(f"Category '{category}' not found. Available: {list(self.categories.keys())}")
        
        folder_name = self.categories[category]
        search_path = os.path.join(self.base_path, folder_name, "*.csv")
        files = glob.glob(search_path)
        
        if not files:
            print(f"Warning: No CSV files found for {category} in {search_path}")
            return pd.DataFrame()

        print(f"Loading {len(files)} files for category: {category}...")
        
        dfs = []
        for file in files:
            try:
                # Use low_memory=False to handle mixed types during initial load
                df = pd.read_csv(file, low_memory=False)
                dfs.append(df)
                print(f" - Loaded {os.path.basename(file)}: {df.shape}")
            except Exception as e:
                print(f" - Error loading {file}: {e}")
        
        if not dfs:
            return pd.DataFrame()
            
        # Concatenate all
        full_df = pd.concat(dfs, ignore_index=True)
        print(f"Total rows for {category}: {len(full_df)}")
        
        return full_df

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """
        Loads all categories and returns a dictionary of DataFrames.
        """
        data = {}
        for cat in self.categories:
            data[cat] = self.load_category(cat)
        return data

# Quick test if run directly
if __name__ == "__main__":
    # Assuming run from the project root
    loader = DataLoader(".")
    loader.load_all()
