import sys
import os
import pandas as pd

# Ensure we can import the package
sys.path.append(os.getcwd())

from aadhaar_eco.data.loader import DataLoader

def inspect_data():
    base_path = "C:\\Users\\goura\\OneDrive\\Desktop\\UIDAI Hackathon"
    loader = DataLoader(base_path)
    
    with open("ingestion_report.txt", "w") as f:
        f.write("--- Starting Data Inspection ---\n")
        data_map = loader.load_all()
        
        for category, df in data_map.items():
            f.write(f"\n\nCategory: {category}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Shape: {df.shape}\n")
            f.write("Columns:\n")
            f.write(str(df.columns.tolist()) + "\n")
            f.write("Head:\n")
            f.write(df.head(2).to_string() + "\n")
            
            # Buffer info output
            from io import StringIO
            buffer = StringIO()
            df.info(buf=buffer)
            f.write("Info:\n")
            f.write(buffer.getvalue() + "\n")

    print("Inspection complete. Check ingestion_report.txt")

if __name__ == "__main__":
    inspect_data()
