from sqlalchemy.orm import Session
from .models import WheelSpecification
from .schemas import WheelSpecCreate

def create_wheel_spec(db: Session, spec: WheelSpecCreate):
    db_spec = WheelSpecification(**spec.dict())
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

def get_wheel_spec(db: Session, formNumber: str, submittedBy: str, submittedDate: str):
    return db.query(WheelSpecification).filter_by(
        formNumber=formNumber,
        submittedBy=submittedBy,
        submittedDate=submittedDate
    ).all()
