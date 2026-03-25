import json
from typing import Any

import requests

from core.config import settings
from models.schemas import StudyResponse, QuizQuestion, Difficulty


def _extract_generated_text(response_data: Any) -> str:
  if isinstance(response_data, dict):
    if "error" in response_data:
      raise RuntimeError(str(response_data["error"]))
    candidates = response_data.get("candidates", [])
    if candidates:
      content = candidates[0].get("content", {})
      parts = content.get("parts", [])
      if parts and isinstance(parts[0], dict) and "text" in parts[0]:
        return parts[0]["text"]
  raise RuntimeError("Unexpected response format from Gemini")


def _extract_json_object(text: str) -> str:
  start = text.find("{")
  end = text.rfind("}")
  if start == -1 or end == -1 or end <= start:
    return text.strip()
  return text[start : end + 1]

async def generate_study_material(topic: str, difficulty: Difficulty, num_questions: int) -> StudyResponse:

    prompt=f"""You are a study assistant. Given the topic below, return ONLY a JSON object.

Topic: {topic}
Difficulty: {difficulty}
Number of quiz questions: {num_questions}

Return this exact JSON structure, nothing else:
{{
  "summary": "2-3 paragraph explanation of the topic",
  "questions": [
    {{
      "question": "question text",
      "options": ["option A", "option B", "option C", "option D"],
      "correct_index": 0,
      "explanation": "why this is correct"
    }}
  ],
  "estimated_read_minutes": 3
}}"""
    
    response = requests.post(
      f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}",
      json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
          "temperature": 0.2,
          "maxOutputTokens": 1200,
        },
      },
      timeout=60,
    )
    response.raise_for_status()

    raw = _extract_generated_text(response.json())
    data = json.loads(_extract_json_object(raw))

    return StudyResponse(
        topic=topic,
        summary=data["summary"],
        difficulty=difficulty,
        questions=[QuizQuestion(**q) for q in data["questions"]],
        estimated_read_minutes=data["estimated_read_minutes"]
    )


async def generate_study_content(topic: str, difficulty: Difficulty, num_questions: int) -> StudyResponse:
    return await generate_study_material(topic, difficulty, num_questions)