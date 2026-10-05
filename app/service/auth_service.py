from app.domain.models import User
from app.service.errors import AuthError, ConflictError, ValidationError
from app.service.ports import PasswordHasher, TokenProvider, UserRepository


class AuthService:
    def __init__(self, users: UserRepository, hasher: PasswordHasher, tokens: TokenProvider):
        self._users, self._hasher, self._tokens = users, hasher, tokens

    def register(self, username: str, password: str) -> User:
        if len(username) < 3 or len(password) < 6:
            raise ValidationError("Username >= 3 ký tự, password >= 6 ký tự")
        if self._users.get_by_username(username):
            raise ConflictError("Username đã tồn tại")
        return self._users.add(User(username=username, password_hash=self._hasher.hash(password)))

    def login(self, username: str, password: str) -> str:
        user = self._users.get_by_username(username)
        if not user or not self._hasher.verify(password, user.password_hash):
            raise AuthError("Sai tên đăng nhập hoặc mật khẩu")
        return self._tokens.create(user.id)
