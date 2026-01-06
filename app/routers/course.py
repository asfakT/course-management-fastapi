from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, responses, Depends, APIRouter
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database
from .. database import engine, get_db


router = APIRouter(
    prefix = "/course",
    tags= ['Course']
)


@router.get("/", response_model= List[schemas.CourseResponse])
def course(db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user), limit: int = 6, search: Optional[str]=""):
    # courses = db.query(models.Course).all()
    courses = db.query(models.Course).filter(models.Course.creator_id == current_user.id).filter(models.Course.name.contains(search)).limit(limit).all()
    return courses

@router.get("/{id}", response_model= schemas.CourseResponse)
def aiquest_course(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == id).first()

    if course is None:
       raise HTTPException(status_code=404, detail="Course not found")
    
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized action")
    return course

@router.post('/', response_model= schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_course = models.Course(**course.model_dump(), creator_id = current_user.id)
    new_course.website = str(new_course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.put("/{id}", response_model=schemas.CourseResponse)
def update_aiquest_course(id:int, updated_course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()

    if course is None:
       raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = updated_course.model_dump()
    update_data["website"] = str(update_data["website"])
    course_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{id}")
def delete_aiquest_course(id: int, db: Session = Depends(get_db), dp: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == id).first()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized action")

    db.delete(course)
    db.commit()

    return {
        "message": "Course deleted successfully",
        "deleted_id": id
    }