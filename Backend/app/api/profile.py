from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.upload_service import save_file
from app.services.reader_service import read_dataset

from app.core.profiler import DataProfiler

router = APIRouter()

@router.post("/")
async def profile_dataset(file: UploadFile= File(...)):
    try:
        saved = save_file(file)
        df = read_dataset(saved["path"])
        profiler = DataProfiler(df)
        return profiler.profile()
    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )