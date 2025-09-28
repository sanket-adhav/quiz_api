from pydantic import BaseModel
from typing import List

class QuizCreate(BaseModel):
    title: str

class OptionCreate(BaseModel):
    text: str
    is_correct: bool = False

class QuestionCreate(BaseModel):
    text: str
    options: List[OptionCreate] = []

class Answer(BaseModel):
    question_id: int
    option_id: int
