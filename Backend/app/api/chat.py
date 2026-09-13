# ========================================
# Data Guardian AI
# AI Chat API
# ========================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.core.chat_engine import ChatEngine


router = APIRouter()


class ChatRequest(BaseModel):

    prompt: str

    analysis_result: Dict[str, Any]


@router.post("/chat")
async def chat(request: ChatRequest):

    try:

        if not request.prompt.strip():

            raise HTTPException(
                status_code=400,
                detail="Please enter a question."
            )

        analysis = request.analysis_result

        # ========================================
        # Handle complete /analyze response
        # ========================================

        if "executive_report" in analysis:

            report = analysis["executive_report"]

            analysis = {

                "quality_score": {
                    "quality_score":
                        report.get(
                            "overall_quality",
                            {}
                        ).get(
                            "score",
                            0
                        ),

                    "grade":
                        report.get(
                            "overall_quality",
                            {}
                        ).get(
                            "grade",
                            "Unknown"
                        )
                },

                "validation":
                    report.get(
                        "validation",
                        {}
                    ),

                "outliers":
                    report.get(
                        "outliers",
                        {}
                    ),

                "business_impact":
                    report.get(
                        "business_impact",
                        {}
                    ),

                "ai_insights":
                    report.get(
                        "ai_insights",
                        {}
                    )
            }

        # ========================================
        # Make sure required fields exist
        # ========================================

        analysis.setdefault(
            "quality_score",
            {
                "quality_score": 0,
                "grade": "Unknown"
            }
        )

        analysis.setdefault(
            "validation",
            {}
        )

        analysis.setdefault(
            "outliers",
            {
                "total_outliers": 0
            }
        )

        analysis.setdefault(
            "business_impact",
            {
                "total_issues": 0
            }
        )

        analysis.setdefault(
            "ai_insights",
            {
                "insights": []
            }
        )

        # ========================================
        # Run Chat Engine
        # ========================================

        chat = ChatEngine(

            prompt=request.prompt,

            analysis_result=analysis

        )

        response = chat.respond()

        # ========================================
        # Return response
        # ========================================

        return {

            "status": "Completed",

            "prompt": request.prompt,

            "chat_response": response

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )