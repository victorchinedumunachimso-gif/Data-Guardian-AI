from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.test import router as test_router
from app.api.upload import router as upload_router
from app.api.profile import router as profile_router
from app.api.validation import router as validation_router
from app.api.scoring import router as score_router
from app.api.insights import router as insights_router
from app.api.cleaning import router as cleaning_router
from app.api import analyze
from app.api.chat import router as chat_router
from app.api.reports import router as reports_router

# ==========================================
# Create FastAPI Application
# ==========================================

app = FastAPI(
    title="Data Guardian AI",
    description="AI Powered Platform for Data Quality Assessment",
    version="1.0.0"
)


# ==========================================
# CORS Configuration
# ==========================================

app.add_middleware(
    CORSMiddleware,

    # Development Mode
    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# Register API Routers
# ==========================================

app.include_router(
    test_router,
    prefix="/api/v1/test",
    tags=["Test"]
)

app.include_router(
    upload_router,
    prefix="/api/v1/upload",
    tags=["Upload"]
)

app.include_router(
    profile_router,
    prefix="/api/v1/profile",
    tags=["Dataset Profiler"]
)

app.include_router(
    validation_router,
    prefix="/api/v1/validation",
    tags=["Validation"]
)

app.include_router(
    score_router,
    prefix="/api/v1/scoring",
    tags=["Quality Score"]
)

app.include_router(
    insights_router,
    prefix="/api/v1/insights",
    tags=["AI Insights"]
)

app.include_router(
    cleaning_router,
    prefix="/api/v1/cleaning",
    tags=["Data Cleaning"]
)

app.include_router(
    analyze.router,
    prefix="/api/v1",
    tags=["AI Analysis"]
)
app.include_router(
    chat_router,
    prefix="/api/v1",
    tags=["AI Chat"]
)
app.include_router(
    reports_router,
    prefix="/api/v1",
    tags=["Reports"]
)

# ==========================================
# Home Endpoint
# ==========================================

@app.get("/", tags=["Home"])
async def home():

    return {

        "application": "Data Guardian AI",

        "version": "1.0.0",

        "status": "Running",

        "message": "Welcome to Data Guardian AI 🚀"

    }


# ==========================================
# Health Check
# ==========================================

@app.get("/health", tags=["Health"])
async def health_check():

    return {

        "status": "healthy",

        "server": "online"

    }