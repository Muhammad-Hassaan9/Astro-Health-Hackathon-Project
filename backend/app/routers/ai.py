from fastapi import APIRouter, Depends
from app.dependencies import get_current_astronaut
from app.models.astronaut import Astronaut
from app.schemas.ai import AIQuestionRequest, AIGuidanceResponse
from app.services.ai_service import generate_health_guidance

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

@router.post("/guidance", response_model=AIGuidanceResponse)
async def get_health_guidance(
    request: AIQuestionRequest,
    current_astronaut: Astronaut = Depends(get_current_astronaut),
):
    answer = await generate_health_guidance(
        question=request.question,
        health_context=request.health_context,
    )

    return AIGuidanceResponse(answer=answer)