

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.upload_service import save_file
from app.services.reader_service import read_dataset

from app.core.analyzer import DataAnalyzer
from app.core.ai_orchestrator import AIOrchestrator


router = APIRouter()


@router.post("/analyze")
async def analyze_dataset(

    file: UploadFile = File(...),

    prompt: str = Form(...)

):



    try:

        # =====================================
        # 1. SAVE DATASET
        # =====================================

        file_info = save_file(file)

        print("📁 File saved:", file_info["path"])


        # =====================================
        # 2. READ DATASET
        # =====================================

        df = read_dataset(
            file_info["path"]
        )

        print("📊 Dataset loaded")

        print(
            "Rows:",
            len(df),
            "Columns:",
            len(df.columns)
        )


        # =====================================
        # 3. RUN DATA ANALYSIS
        # =====================================

        analyzer = DataAnalyzer(
            dataframe=df
        )

        analysis_result = analyzer.analyze()

        print(
            "✅ Data analysis completed"
        )


        # =====================================
        # 4. RUN AI ORCHESTRATOR
        # =====================================

        orchestrator = AIOrchestrator(

            prompt=prompt,

            analysis_result=analysis_result

        )

        ai_result = orchestrator.execute()


        # =====================================
        # 5. RETURN COMPLETE RESULT
        # =====================================

        return {

            "status": "Completed",

            "prompt": prompt,

            "analysis": analysis_result,

            "ai": ai_result

        }


    except Exception as e:

        print(
            "❌ ANALYSIS ERROR:",
            str(e)
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )