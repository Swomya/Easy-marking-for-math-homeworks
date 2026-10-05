"""Cài đặt các Repository (port) bằng SQLAlchemy; map giữa ORM row <-> domain model."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Assignment, Submission, User
from app.repository.orm import AssignmentRow, SubmissionRow, UserRow
from app.service import ports


def _to_domain(row, cls):
    return cls(**{c.name: getattr(row, c.name) for c in row.__table__.columns})


class SqlUserRepository(ports.UserRepository):
    def __init__(self, db: Session): self._db = db

    def add(self, user: User) -> User:
        row = UserRow(username=user.username, password_hash=user.password_hash)
        self._db.add(row); self._db.commit()
        user.id = row.id
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        row = self._db.scalar(select(UserRow).where(UserRow.username == username))
        return _to_domain(row, User) if row else None


class SqlAssignmentRepository(ports.AssignmentRepository):
    def __init__(self, db: Session): self._db = db

    def add(self, a: Assignment) -> Assignment:
        row = AssignmentRow(title=a.title, question=a.question, correct_answer=a.correct_answer,
                            created_by=a.created_by, created_at=a.created_at)
        self._db.add(row); self._db.commit()
        a.id = row.id
        return a

    def get(self, assignment_id: int) -> Optional[Assignment]:
        row = self._db.get(AssignmentRow, assignment_id)
        return _to_domain(row, Assignment) if row else None

    def list(self) -> list[Assignment]:
        rows = self._db.scalars(select(AssignmentRow).order_by(AssignmentRow.id.desc())).all()
        return [_to_domain(r, Assignment) for r in rows]


class SqlSubmissionRepository(ports.SubmissionRepository):
    def __init__(self, db: Session): self._db = db

    def add(self, s: Submission) -> Submission:
        data = {k: v for k, v in s.__dict__.items() if k != "id"}
        row = SubmissionRow(**data)
        self._db.add(row); self._db.commit()
        s.id = row.id
        return s

    def get(self, submission_id: int) -> Optional[Submission]:
        row = self._db.get(SubmissionRow, submission_id)
        return _to_domain(row, Submission) if row else None

    def list_by_user(self, user_id: int) -> list[Submission]:
        rows = self._db.scalars(select(SubmissionRow).where(SubmissionRow.user_id == user_id)
                                .order_by(SubmissionRow.id.desc())).all()
        return [_to_domain(r, Submission) for r in rows]

    def delete(self, submission_id: int) -> None:
        row = self._db.get(SubmissionRow, submission_id)
        if row:
            self._db.delete(row); self._db.commit()
