from pydantic import BaseModel

class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    text: str
    predicted_label: str
    scores: dict[str, float]
