from fastapi import APIRouter, Depends, HTTPException, status, Header
from models.schemas import StudyRequest, StudyResponse, ErrorResponse
from services.llm import generate_study_content
from core.config import settings