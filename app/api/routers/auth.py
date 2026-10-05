from fastapi import APIRouter, Depends, Request, status

from app.api.deps import get_db
from app.api.schemas import Credentials, TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(body: Credentials, request: Request, db=Depends(get_db)):
    user = request.app.state.container.auth_service(db).register(body.username, body.password)
    return UserOut(id=user.id, username=user.username)


@router.post("/login", response_model=TokenOut)
def login(body: Credentials, request: Request, db=Depends(get_db)):
    token = request.app.state.container.auth_service(db).login(body.username, body.password)
    return TokenOut(access_token=token)
