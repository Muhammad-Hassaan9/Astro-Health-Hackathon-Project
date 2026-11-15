import json
import re

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
- Explain the astronaut's actual available health readings.
- Use the latest readings provided in the health context.
- Mention the value and unit when relevant to the question.
- Mention whether a reading is simulated, manual, or sensor-based when relevant.
- Never invent or assume missing readings.
- If a relevant reading is unavailable, clearly say so.
- If a reading is old, mention its timestamp and do not call it current.
- Provide general wellness and safety information.
- Never diagnose diseases or prescribe medication.
- Never claim to replace a qualified medical professional.
- If readings appear concerning or the astronaut reports serious symptoms,
  advise contacting the mission medical officer.

RESPONSE FORMATTING RULES:
- Respond in simple, professional English.
- Use plain text only.
- Do not use Markdown formatting.
- Do not create Markdown tables.
- Do not use bold, italic, headings with #, backticks, or decorative symbols.
- Avoid unusual Unicode characters, fancy quotation marks, and long dashes.
- Use ordinary punctuation.
- Use short paragraphs.
- Use simple numbered points or hyphen bullets only when necessary.
- Keep the answer concise and directly answer the question.
"""


def clean_ai_response(answer: str) -> str:
    """Remove unnecessary Markdown and decorative formatting."""

    if not answer:
        return ""

    cleaned_lines = []

    for line in answer.splitlines():
        line = line.strip()

        if not line:
            continue

        # Remove Markdown table separator rows.
        if re.fullmatch(r"[\s|:\-]+", line):
            continue

        # Convert Markdown table rows into readable plain text.
        if "|" in line:
            cells = [
                cell.strip()
                for cell in line.strip("|").split("|")
                if cell.strip()
            ]

            if cells:
                line = " - ".join(cells)

        # Remove Markdown heading and emphasis syntax.
        line = re.sub(r"^#{1,6}\s*", "", line)
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"__(.*?)__", r"\1", line)
        line = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", line)
        line = line.replace("`", "")

        # Normalize unusual punctuation.
        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u00a0": " ",
            "\u2248": "approximately ",
            "\u2022": "-",
        }

        for old, new in replacements.items():
            line = line.replace(old, new)

        # Remove excessive spaces.
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


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
The following health information belongs to the authenticated astronaut.

Use this information to answer the question accurately.
Do not invent readings or assume that missing values are available.

HEALTH INFORMATION:
{json.dumps(context, indent=2, default=str)}

ASTRONAUT'S QUESTION:
{question.strip()}

Answer directly using the latest relevant readings.
If the relevant reading is missing, say that it is not available.
Follow all plain-text formatting rules.
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

        return clean_ai_response(answer.strip())

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