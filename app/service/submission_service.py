from app.domain.models import Submission
from app.service.errors import ForbiddenError, NotFoundError, OcrError, ValidationError
from app.service.ports import (AnswerGrader, AssignmentRepository, FileStorage,
                               OcrEngine, SubmissionRepository)

ALLOWED_MIME = {"image/png", "image/jpeg", "image/webp"}
MAX_SCORE = 10.0


class SubmissionService:
    def __init__(self, submissions: SubmissionRepository, assignments: AssignmentRepository,
                 ocr: OcrEngine, grader: AnswerGrader, storage: FileStorage):
        self._subs, self._assignments = submissions, assignments
        self._ocr, self._grader, self._storage = ocr, grader, storage

    def submit(self, user_id: int, assignment_id: int, image: bytes, mime_type: str) -> Submission:
        if mime_type not in ALLOWED_MIME:
            raise ValidationError("Chỉ chấp nhận ảnh PNG/JPEG/WEBP")
        if not image:
            raise ValidationError("File rỗng")
        assignment = self._assignments.get(assignment_id)
        if not assignment:
            raise NotFoundError("Không tìm thấy bài tập")

        path = self._storage.save(image, mime_type)
        sub = Submission(assignment_id=assignment_id, user_id=user_id, image_path=path)
        try:
            ocr = self._ocr.extract(image, mime_type)
            verdict = self._grader.grade(assignment.correct_answer, ocr.final_answer)
            sub.ocr_text, sub.extracted_answer = ocr.text, ocr.final_answer
            sub.is_correct, sub.feedback = verdict.is_correct, verdict.feedback
            sub.score = MAX_SCORE if verdict.is_correct else 0.0
            sub.status = "GRADED"
        except OcrError as e:
            sub.status, sub.feedback = "FAILED", f"Lỗi nhận dạng: {e}"
        return self._subs.add(sub)

    def get(self, user_id: int, submission_id: int) -> Submission:
        sub = self._subs.get(submission_id)
        if not sub:
            raise NotFoundError("Không tìm thấy bài nộp")
        if sub.user_id != user_id:
            raise ForbiddenError("Không có quyền xem bài nộp này")
        return sub

    def list_mine(self, user_id: int) -> list[Submission]:
        return self._subs.list_by_user(user_id)

    def delete(self, user_id: int, submission_id: int) -> None:
        sub = self.get(user_id, submission_id)
        self._subs.delete(sub.id)
        self._storage.delete(sub.image_path)
