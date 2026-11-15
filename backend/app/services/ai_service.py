import json

from fastapi import HTTPException, status
from openai import (
    AsyncOpenAI,
    APITimeoutError,
    APIConnectionError,
    APIStatusError,
)

from app.core.config import settings

GROQ_MODEL = "openai/gpt-oss-20b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

SYSTEM_INSTRUCTION = """
You are AstroHealth's general astronaut wellness information assistant.

Your responsibilities:
- Explain health readings in simple and clear language.
- Provide general wellness and safety information.
- Use only the health information provided in the request.
- Never invent missing health readings.
- Never diagnose diseases or prescribe medication.
- Never claim to replace a qualified medical professional.
- If readings appear concerning, advise the astronaut to contact
  the mission medical officer.
- Clearly mention when the provided information is insufficient.
- Keep responses clear, concise and safety-focused.
"""

async def generate_health_guidance(
    question: str,
    health_context: dict | None = None,
) -> str:

    if not settings.GROQ_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured.",
        )

    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty.",
        )

    context = health_context or {}

    prompt = f"""
Health information:
{json.dumps(context, indent=2, default=str)}

Astronaut's question:
{question.strip()}

Provide a clear, concise and safety-focused response.
"""

    try:
        async with AsyncOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
            timeout=45.0,
            max_retries=0,
        ) as client:

            response = await client.responses.create(
                model=GROQ_MODEL,
                instructions=SYSTEM_INSTRUCTION,
                input=prompt,
                max_output_tokens=700,
            )

        answer = response.output_text

        if not answer or not answer.strip():
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI service returned an empty response.",
            )

        return answer.strip()

    except APITimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI service request timed out.",
        )

    except APIConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to the AI service.",
        )

    except APIStatusError as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
                if exc.status_code == 429
                else status.HTTP_502_BAD_GATEWAY
            ),
            detail="AI provider could not process the request.",
        )