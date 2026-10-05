from app.domain.models import Assignment
from app.service.errors import NotFoundError, ValidationError
from app.service.ports import AssignmentRepository


class AssignmentService:
    def __init__(self, repo: AssignmentRepository):
        self._repo = repo

    def create(self, user_id: int, title: str, question: str, correct_answer: str) -> Assignment:
        if not title.strip() or not correct_answer.strip():
            raise ValidationError("Tiêu đề và đáp án không được rỗng")
        return self._repo.add(Assignment(title=title, question=question,
                                         correct_answer=correct_answer, created_by=user_id))

    def get(self, assignment_id: int) -> Assignment:
        a = self._repo.get(assignment_id)
        if not a:
            raise NotFoundError("Không tìm thấy bài tập")
        return a

    def list(self) -> list[Assignment]:
        return self._repo.list()
