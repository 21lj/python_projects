# handles API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db

router = APIRouter()

@router.get("/")
def health_check():
    return {"message": "User Management API running"}

@router.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@router.get("/user/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.put("/user/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user.name, user.email)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted"}

@router.get("/search", response_model=list[schemas.UserOut])
def search_user(name: str, db: Session = Depends(get_db)):
    return crud.search_users(db, name)

@router.post("/login")
def login(credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}

