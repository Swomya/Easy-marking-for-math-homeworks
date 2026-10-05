from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=50, examples=["hocsinh01"])
    password: str = Field(min_length=6, max_length=72, examples=["matkhau123"])


class UserOut(BaseModel):
    id: int
    username: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AssignmentIn(BaseModel):
    title: str = Field(examples=["Giải phương trình bậc nhất"])
    question: str = Field(examples=["Giải: 2x + 4 = 12"])
    correct_answer: str = Field(examples=["4"])


class AssignmentOut(BaseModel):
    id: int
    title: str
    question: str
    correct_answer: str
    created_by: int
    created_at: datetime


class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    status: str
    ocr_text: str
    extracted_answer: str
    is_correct: Optional[bool]
    score: Optional[float]
    feedback: str
    created_at: datetime
