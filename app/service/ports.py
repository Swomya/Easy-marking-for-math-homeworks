"""Các cổng (interface) mà tầng nghiệp vụ cần. Tầng dưới sẽ cài đặt chúng."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from app.domain.models import Assignment, Submission, User


@dataclass
class OcrResult:
    text: str          # toàn bộ lời giải đã chép lại
    final_answer: str  # đáp án cuối cùng học sinh viết


@dataclass
class GradeVerdict:
    is_correct: bool
    feedback: str


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: ...
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: ...


class AssignmentRepository(ABC):
    @abstractmethod
    def add(self, a: Assignment) -> Assignment: ...
    @abstractmethod
    def get(self, assignment_id: int) -> Optional[Assignment]: ...
    @abstractmethod
    def list(self) -> list[Assignment]: ...


class SubmissionRepository(ABC):
    @abstractmethod
    def add(self, s: Submission) -> Submission: ...
    @abstractmethod
    def get(self, submission_id: int) -> Optional[Submission]: ...
    @abstractmethod
    def list_by_user(self, user_id: int) -> list[Submission]: ...
    @abstractmethod
    def delete(self, submission_id: int) -> None: ...


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, raw: str) -> str: ...
    @abstractmethod
    def verify(self, raw: str, hashed: str) -> bool: ...


class TokenProvider(ABC):
    @abstractmethod
    def create(self, user_id: int) -> str: ...
    @abstractmethod
    def decode(self, token: str) -> Optional[int]:
        """Trả về user_id nếu token hợp lệ, ngược lại None."""


class OcrEngine(ABC):
    @abstractmethod
    def extract(self, image: bytes, mime_type: str) -> OcrResult: ...


class AnswerGrader(ABC):
    @abstractmethod
    def grade(self, expected: str, actual: str) -> GradeVerdict: ...


class FileStorage(ABC):
    @abstractmethod
    def save(self, data: bytes, mime_type: str) -> str: ...
    @abstractmethod
    def delete(self, path: str) -> None: ...
