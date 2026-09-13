# ========================================
# Data Guardian AI
# ML Cleaning & Export API
# ========================================

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.services.upload_service import save_file
from app.services.reader_service import read_dataset
from app.core.ml_cleaner import MLCleaner


router = APIRouter()


# ========================================
# Folders
# ========================================

CLEANED_FOLDER = Path("app/cleaned")

CLEANED_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ========================================
# Clean Dataset
# ========================================

@router.post("/")
async def clean_dataset(
    file: UploadFile = File(...)
):

    try:

        # --------------------------------
        # 1. Save original file
        # --------------------------------

        saved = save_file(file)

        original_path = saved["path"]

        print(
            "📁 Original file:",
            original_path
        )


        # --------------------------------
        # 2. Read dataset
        # --------------------------------

        df = read_dataset(
            original_path
        )

        print(
            "📊 Dataset loaded:",
            df.shape
        )


        # --------------------------------
        # 3. Run ML Cleaner
        # --------------------------------

        cleaner = MLCleaner(df)

        cleaned_df, report = cleaner.clean()

        print(
            "🤖 ML cleaning completed"
        )

        print(
            "📊 Cleaned dataset:",
            cleaned_df.shape
        )


        # --------------------------------
        # 4. Generate unique filename
        # --------------------------------

        file_id = uuid4().hex

        csv_path = (
            CLEANED_FOLDER
            / f"cleaned_{file_id}.csv"
        )

        excel_path = (
            CLEANED_FOLDER
            / f"cleaned_{file_id}.xlsx"
        )


        # --------------------------------
        # 5. Export CSV
        # --------------------------------

        cleaned_df.to_csv(
            csv_path,
            index=False
        )


        # --------------------------------
        # 6. Export Excel
        # --------------------------------

        cleaned_df.to_excel(
            excel_path,
            index=False
        )


        print(
            "💾 Cleaned CSV:",
            csv_path
        )

        print(
            "💾 Cleaned Excel:",
            excel_path
        )


        # --------------------------------
        # 7. Verify cleaning
        # --------------------------------

        remaining_missing = int(
            cleaned_df.isna()
            .sum()
            .sum()
        )

        duplicate_rows = int(
            cleaned_df.duplicated()
            .sum()
        )


        # --------------------------------
        # 8. Return result
        # --------------------------------

        return {

            "status": "success",

            "message":
                "Dataset cleaned successfully.",

            "cleaning_report":
                report,

            "verification": {

                "rows_before":
                    int(len(df)),

                "rows_after":
                    int(len(cleaned_df)),

                "columns":
                    int(len(cleaned_df.columns)),

                "remaining_missing_values":
                    remaining_missing,

                "remaining_duplicate_rows":
                    duplicate_rows

            },

            "preview":
                cleaned_df
                .head(10)
                .to_dict(
                    orient="records"
                ),

            "downloads": {

    "csv":
        f"http://127.0.0.1:8000/api/v1/cleaning/download/csv/{file_id}",

    "excel":
        f"http://127.0.0.1:8000/api/v1/cleaning/download/excel/{file_id}"

}

        }


    except Exception as e:

        print(
            "❌ CLEANING ERROR:",
            str(e)
        )

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ========================================
# Download CSV
# ========================================

@router.get("/download/csv/{file_id}")
async def download_csv(
    file_id: str
):

    path = (
        CLEANED_FOLDER
        / f"cleaned_{file_id}.csv"
    )

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="Cleaned CSV file not found."
        )

    return FileResponse(

        path=path,

        media_type="text/csv",

        filename="cleaned_dataset.csv"

    )


# ========================================
# Download Excel
# ========================================

@router.get("/download/excel/{file_id}")
async def download_excel(
    file_id: str
):

    path = (
        CLEANED_FOLDER
        / f"cleaned_{file_id}.xlsx"
    )

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="Cleaned Excel file not found."
        )

    return FileResponse(

        path=path,

        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),

        filename="cleaned_dataset.xlsx"

    )