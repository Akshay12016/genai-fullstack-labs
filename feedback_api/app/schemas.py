from pydantic import BaseModel
from datetime import datetime


class FeedbackCreate(BaseModel):
    user_name: str
    message: str
    rating: int


class FeedbackResponse(FeedbackCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
