from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.container import Container
from app.api.middleware import AuthMiddleware
from app.api.routers import assignments, auth, submissions
from app.config import Settings
from app.service import errors

_STATUS = {errors.ValidationError: 422, errors.AuthError: 401, errors.ForbiddenError: 403,
           errors.NotFoundError: 404, errors.ConflictError: 409}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    container = Container(settings)
    app = FastAPI(title="Math Grader API",
                  description="Dịch vụ backend chấm bài tập toán từ ảnh chụp (OCR bằng Gemini).",
                  version="1.0.0")
    app.state.container = container
    app.add_middleware(AuthMiddleware, token_provider=container.tokens)

    @app.exception_handler(errors.DomainError)
    async def domain_error_handler(_: Request, exc: errors.DomainError):
        return JSONResponse({"detail": str(exc)}, status_code=_STATUS.get(type(exc), 400))

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(assignments.router)
    app.include_router(submissions.router)
    return app


def app_factory() -> FastAPI:  # uvicorn app.api.main:app_factory --factory
    return create_app()
