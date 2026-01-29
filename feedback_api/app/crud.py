from sqlalchemy.orm import Session
from app.models import Feedback
from app.schemas import FeedbackCreate


def create_feedback(db: Session, feedback: FeedbackCreate):
    new_feedback = Feedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


def get_feedback(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def get_all_feedbacks(db: Session):
    return db.query(Feedback).all()


def delete_feedback(db: Session, feedback_id: int):
    feedback = get_feedback(db, feedback_id)
    if feedback:
        db.delete(feedback)
        db.commit()
    return feedback
