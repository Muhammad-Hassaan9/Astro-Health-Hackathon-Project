from pydantic import BaseModel, Field, ConfigDict

class AIQuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    health_context: dict | None = None

    model_config = ConfigDict(str_strip_whitespace=True)

class AIGuidanceResponse(BaseModel):
    answer: str