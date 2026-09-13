import os 
import uuid
import shutil
import pathlib 

from fastapi import UploadFile

UPLOAD_FOLDER = pathlib.Path("app/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_FILE_SIZE = 100 * 1024 * 1024

def save_file(file: UploadFile):
    extension = pathlib.Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only CSV and Excel files are allowed")
    
    unique_name = f"{uuid.uuid4().hex}{extension}"

    destination = UPLOAD_FOLDER / unique_name

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return{
        "original_name": file.filename,
        "saved_name": unique_name,
        "path": str(destination)
    }
