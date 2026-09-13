from fastapi import APIRouter, UploadFile, File, HTTPException
import openpyxl
from app.services.upload_service import save_file
from app.services.reader_service import read_dataset

router = APIRouter()

@router.post("/")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        saved = save_file(file)

        df = read_dataset(saved["path"])

        return{
            "status": "Success",
            "original_filename": saved["original_name"],
            "saved_filename": saved["saved_name"],
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "data_types": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            }


    }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    