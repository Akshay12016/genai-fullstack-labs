from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/feedback", tags=["Feedback"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.FeedbackResponse)
def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db)
):
    return crud.create_feedback(db, feedback)


@router.get("/{feedback_id}", response_model=schemas.FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = crud.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.get("/", response_model=list[schemas.FeedbackResponse])
def list_feedbacks(db: Session = Depends(get_db)):
    return crud.get_all_feedbacks(db)


@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = crud.delete_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}
