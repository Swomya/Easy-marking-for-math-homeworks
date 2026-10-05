"""Thực thể nghiệp vụ thuần (dataclass) - không phụ thuộc framework/DB."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    username: str
    password_hash: str
    id: Optional[int] = None


@dataclass
class Assignment:
    title: str
    question: str
    correct_answer: str
    created_by: int
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Submission:
    assignment_id: int
    user_id: int
    image_path: str
    status: str = "PENDING"  # PENDING | GRADED | FAILED
    ocr_text: str = ""
    extracted_answer: str = ""
    is_correct: Optional[bool] = None
    score: Optional[float] = None
    feedback: str = ""
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
