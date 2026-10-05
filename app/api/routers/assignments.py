from fastapi import APIRouter, Depends, Request, status

from app.api.deps import bearer_doc, current_user_id, get_db
from app.api.schemas import AssignmentIn, AssignmentOut

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post("", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(bearer_doc)])
def create_assignment(body: AssignmentIn, request: Request, db=Depends(get_db),
                      user_id: int = Depends(current_user_id)):
    return request.app.state.container.assignment_service(db).create(
        user_id, body.title, body.question, body.correct_answer)


@router.get("", response_model=list[AssignmentOut])
def list_assignments(request: Request, db=Depends(get_db)):
    return request.app.state.container.assignment_service(db).list()


@router.get("/{assignment_id}", response_model=AssignmentOut)
def get_assignment(assignment_id: int, request: Request, db=Depends(get_db)):
    return request.app.state.container.assignment_service(db).get(assignment_id)
