from fastapi import APIRouter, Depends, HTTPException, status, Header
from models.schemas import StudyRequest, StudyResponse, ErrorResponse
from services.llm import generate_study_content
from core.config import settings

router = APIRouter(prefix="/study", tags=["Study"])

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return x_api_key