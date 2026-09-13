from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def test_api():
    return{
        "status": "success",
        "message": "API Version 1 is working."
    }
