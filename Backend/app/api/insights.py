from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.upload_service import save_file
from app.services.reader_service import read_dataset
from app.core.validator import DataValidator
from app.core.scorer import DataQualityScorer
from app.core.ai_insights import AIInsights

router = APIRouter()

@router.post("/")
async def generate_insights(file: UploadFile = File(...)):
    try:
        saved = save_file(file)

        df = read_dataset(saved["path"])

        validator = DataValidator(df)
        validation = validator.validate()

        scorer = DataQualityScorer(validation)
        score = scorer.calculate_score()

        ai = AIInsights(validation, score)

        return{
            "validation": validation,
            "score": score,
            "insights": ai.generate()
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )