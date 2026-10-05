"""Composition root: nơi DUY NHẤT nối interface với cài đặt cụ thể."""
from app.config import Settings
from app.infrastructure.mock_ocr import MockOcrEngine
from app.infrastructure.security import BcryptHasher, JwtTokenProvider
from app.infrastructure.storage import LocalFileStorage
from app.infrastructure.sympy_grader import SympyAnswerGrader
from app.repository.orm import make_session_factory
from app.repository.sql_repositories import (SqlAssignmentRepository, SqlSubmissionRepository,
                                             SqlUserRepository)
from app.service.assignment_service import AssignmentService
from app.service.auth_service import AuthService
from app.service.submission_service import SubmissionService


class Container:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session_factory = make_session_factory(settings.database_url)
        self.hasher = BcryptHasher()
        self.tokens = JwtTokenProvider(settings.jwt_secret, settings.jwt_expire_minutes)
        self.storage = LocalFileStorage(settings.upload_dir)
        self.grader = SympyAnswerGrader()
        if settings.ocr_engine == "mock":
            self.ocr = MockOcrEngine()
        else:
            from app.infrastructure.gemini_ocr import GeminiOcrEngine
            self.ocr = GeminiOcrEngine(settings.gemini_api_key, settings.gemini_model)

    # Mỗi request một DB session -> dựng service mới
    def auth_service(self, db):
        return AuthService(SqlUserRepository(db), self.hasher, self.tokens)

    def assignment_service(self, db):
        return AssignmentService(SqlAssignmentRepository(db))

    def submission_service(self, db):
        return SubmissionService(SqlSubmissionRepository(db), SqlAssignmentRepository(db),
                                 self.ocr, self.grader, self.storage)
