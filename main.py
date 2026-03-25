from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import study
from core.config import settings

app = FastAPI(title=settings.app_name, 
                description="Generate summaries and quizzes for any topic using AI",
                version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],    
    allow_headers=["*"],
)

app.include_router(study.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}!"}

