import anthropic
import json
from core.config import settings
from models.schemas import StudyResponse, QuizQuestion, Difficulty

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

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
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    data = json.loads(raw)

    return StudyResponse(
        topic=topic,
        summary=data["summary"],
        difficulty=difficulty,
        questions=[QuizQuestion(**q) for q in data["questions"]],
        estimated_read_minutes=data["estimated_read_minutes"]
    )


async def generate_study_content(topic: str, difficulty: Difficulty, num_questions: int) -> StudyResponse:
    return await generate_study_material(topic, difficulty, num_questions)