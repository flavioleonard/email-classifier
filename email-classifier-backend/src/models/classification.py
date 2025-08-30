from pydantic import BaseModel

class ClassificationResult(BaseModel):
    category: str | None
    suggested_response: str