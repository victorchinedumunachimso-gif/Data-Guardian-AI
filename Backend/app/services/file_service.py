import os 
import shutil
import pandas as pd
from fastapi import UploadFile

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(file: UploadFile):
    """
    Save uploaded file to the uploads folder
    """
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

def read_dataset(file_path: str):
    """
    Read CSV or Excel dataset
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    
    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)
    
    else:
        raise ValueError("Unsopported file format.")
    
    return df

