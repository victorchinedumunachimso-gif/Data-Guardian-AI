from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.upload_service import save_file
from app.services.reader_service import read_dataset

from app.core.validator import DataValidator
from app.core.scorer import DataQualityScorer

router = APIRouter()


@router.post("/")
async def score_dataset(file: UploadFile = File(...)):

    try:
        saved = save_file(file)
        df = read_dataset(saved["path"])
        validator = DataValidator(df)
        validation_report = validator.validate()
        scorer = DataQualityScorer(validation_report)
        score = scorer.calculate_score()

        return{
            "validation": validation_report,
            "score": score
            }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail = str(e)
        )
        