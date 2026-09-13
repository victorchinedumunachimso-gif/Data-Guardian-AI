from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.upload_service import save_file
from app.services.reader_service import read_dataset
from app.core.validator import DataValidator

router = APIRouter()

@router.post("/")
async def validate_dataset(file: UploadFile = File(...)):
    try:
        saved = save_file(file)
        df = read_dataset(saved["path"])
        validator=DataValidator(df)
        return validator.validate()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )