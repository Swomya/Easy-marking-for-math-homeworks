from fastapi import Request
from fastapi.security import HTTPBearer

# Chỉ để Swagger UI hiện nút "Authorize"; việc kiểm tra thật nằm ở AuthMiddleware.
bearer_doc = HTTPBearer(auto_error=False)


def get_db(request: Request):
    db = request.app.state.container.session_factory()
    try:
        yield db
    finally:
        db.close()


def current_user_id(request: Request) -> int:
    return request.state.user_id  # do AuthMiddleware gán
