from typing import List
from fastapi import FastAPI, HTTPException, status, responses, Depends, APIRouter
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import engine, get_db
from app.utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
