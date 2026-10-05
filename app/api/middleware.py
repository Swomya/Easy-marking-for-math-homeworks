"""Xác thực JWT tập trung: viết MỘT lần, áp cho mọi endpoint không nằm trong danh sách công khai."""
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

PUBLIC_EXACT = {"/", "/health", "/docs", "/redoc", "/openapi.json"}
PUBLIC_PREFIX = ("/auth/",)
PUBLIC_GET_PREFIX = ("/assignments",)  # xem danh sách/chi tiết bài tập không cần đăng nhập


def is_public(method: str, path: str) -> bool:
    if method == "OPTIONS" or path in PUBLIC_EXACT or path.startswith(PUBLIC_PREFIX):
        return True
    return method == "GET" and path.startswith(PUBLIC_GET_PREFIX)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, token_provider):
        super().__init__(app)
        self._tokens = token_provider

    async def dispatch(self, request: Request, call_next):
        if is_public(request.method, request.url.path):
            return await call_next(request)
        header = request.headers.get("Authorization", "")
        user_id = self._tokens.decode(header[7:]) if header.startswith("Bearer ") else None
        if user_id is None:
            return JSONResponse({"detail": "Chưa đăng nhập hoặc token không hợp lệ"}, status_code=401,
                                headers={"WWW-Authenticate": "Bearer"})
        request.state.user_id = user_id
        return await call_next(request)
