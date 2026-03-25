import json
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

@router.post("/", response_model=StudyResponse, responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}, summary="Generate study material for a topic")
async def generate_study_material(request: StudyRequest, api_key: str= Depends(verify_api_key)):
    try:
        result=await generate_study_content(topic=request.topic, difficulty=request.difficulty, num_questions=request.num_questions)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="LLM returned malformed JSON"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", summary="Check if API is running")
async def health():
    return {"status": "ok", "service": settings.app_name}