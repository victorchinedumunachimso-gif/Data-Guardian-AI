import pandas as pd

def read_dataset(path: str):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    
    elif path.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    
    raise ValueError("Unsupported file format.")
