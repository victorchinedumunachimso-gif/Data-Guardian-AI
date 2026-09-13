from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Any

from app.services.pdf_report_service import PDFReportService

router = APIRouter()


def find_executive_report(data: Any):

    if isinstance(data, dict):

        if "overall_quality" in data:
            return data

        for value in data.values():
            found = find_executive_report(value)

            if found is not None:
                return found

    elif isinstance(data, list):

        for item in data:
            found = find_executive_report(item)

            if found is not None:
                return found

    return None


@router.post("/generate")
async def generate_report(data: Any):

    try:

        print("📥 PDF REQUEST RECEIVED")
        print("📦 Type:", type(data))

        report = find_executive_report(data)

        if report is None:
            raise HTTPException(
                status_code=400,
                detail="Could not find executive report data."
            )

        print("✅ Executive report found")

        pdf_service = PDFReportService(report)

        pdf_buffer = pdf_service.generate()

        print("✅ PDF generated successfully")

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    'attachment; filename="data_guardian_executive_report.pdf"'
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        print("❌ PDF generation error:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )