from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import WheelSpecCreate
from . import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/forms/wheel-specifications")
def submit_spec(spec: WheelSpecCreate, db: Session = Depends(get_db)):
    saved = crud.create_wheel_spec(db, spec)
    return {
        "success": True,
        "message": "Wheel specification submitted successfully.",
        "data": {
            "formNumber": saved.formNumber,
            "submittedBy": saved.submittedBy,
            "submittedDate": str(saved.submittedDate),
            "status": "Saved"
        }
    }

@router.get("/api/forms/wheel-specifications")
def get_spec(formNumber: str, submittedBy: str, submittedDate: str, db: Session = Depends(get_db)):
    specs = crud.get_wheel_spec(db, formNumber, submittedBy, submittedDate)
    return {
        "success": True,
        "message": "Filtered wheel specification forms fetched successfully.",
        "data": [spec.__dict__ for spec in specs]
    }
