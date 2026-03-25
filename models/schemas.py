from pydantic import BaseModel, Field
from enum import Enum

class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class StudyMaterial(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200, description="The topic to study")
    difficulty: Difficulty = Difficulty.medium
    num_questions: int = Field(default=5, ge=1, le=10)

class StudyRequest(StudyMaterial):
    pass

class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_index: int
    explanation: str

class StudyResponse(BaseModel):
    topic: str
    summary: str
    difficulty: Difficulty
    questions: list[QuizQuestion]
    estimated_read_minutes: int

class ErrorResponse(BaseModel):
    detail: str
    code: str
