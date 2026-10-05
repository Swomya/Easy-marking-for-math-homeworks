from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt

from app.service.ports import PasswordHasher, TokenProvider


class BcryptHasher(PasswordHasher):
    def hash(self, raw: str) -> str:
        return bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

    def verify(self, raw: str, hashed: str) -> bool:
        return bcrypt.checkpw(raw.encode(), hashed.encode())


class JwtTokenProvider(TokenProvider):
    def __init__(self, secret: str, expire_minutes: int = 60):
        self._secret, self._ttl = secret, expire_minutes

    def create(self, user_id: int) -> str:
        exp = datetime.now(timezone.utc) + timedelta(minutes=self._ttl)
        return jwt.encode({"sub": str(user_id), "exp": exp}, self._secret, algorithm="HS256")

    def decode(self, token: str) -> Optional[int]:
        try:
            return int(jwt.decode(token, self._secret, algorithms=["HS256"])["sub"])
        except (jwt.PyJWTError, KeyError, ValueError):
            return None
