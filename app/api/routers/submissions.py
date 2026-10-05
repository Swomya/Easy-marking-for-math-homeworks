from fastapi import APIRouter, Depends, File, Form, Request, Response, UploadFile, status

from app.api.deps import bearer_doc, current_user_id, get_db
from app.api.schemas import SubmissionOut

router = APIRouter(prefix="/submissions", tags=["Submissions"], dependencies=[Depends(bearer_doc)])


@router.post("", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED,
             summary="Nộp ảnh bài làm -> OCR (Gemini) -> chấm điểm")
def submit(request: Request, assignment_id: int = Form(...), file: UploadFile = File(...),
           db=Depends(get_db), user_id: int = Depends(current_user_id)):
    svc = request.app.state.container.submission_service(db)
    return svc.submit(user_id, assignment_id, file.file.read(), file.content_type or "")


@router.get("", response_model=list[SubmissionOut])
def list_my_submissions(request: Request, db=Depends(get_db), user_id: int = Depends(current_user_id)):
    return request.app.state.container.submission_service(db).list_mine(user_id)


@router.get("/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id: int, request: Request, db=Depends(get_db),
                   user_id: int = Depends(current_user_id)):
    return request.app.state.container.submission_service(db).get(user_id, submission_id)


@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submission(submission_id: int, request: Request, db=Depends(get_db),
                      user_id: int = Depends(current_user_id)):
    request.app.state.container.submission_service(db).delete(user_id, submission_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
