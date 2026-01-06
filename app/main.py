from fastapi import FastAPI
from . routers import user, course, auth
from . import models
from . database import engine
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)

# # Database Connection
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             port=5433,       
#             database="aiquest",
#             user="postgres",
#             password="1234",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("✅ Successfully connected to database")
#         break
#     except Exception as error:
#         print("❌ Database connection failed")
#         print("Error:", error)
#         time.sleep(2)

# @app.get("/")
# def aiquist():
#     cursor.execute("SELECT * FROM course")
#     data = cursor.fetchall()
#     return {"Data": data}

# # GET all courses (READ)
# @app.get("/courses")
# def get_courses():
#     cursor.execute("SELECT * FROM course ORDER BY id ASC")
#     data = cursor.fetchall()
#     return data

# # POST new course (CREATE)
# @app.post("/courses")
# def create_course(course: Course):
#     cursor.execute(
#         """
#         INSERT INTO course (name, "Instructor", "Duration", website)
#         VALUES (%s, %s, %s, %s)
#         RETURNING *
#         """,
#         (course.name, course.instructor, course.duration, str(course.website))
#     )
#     new_course = cursor.fetchone()
#     conn.commit()
#     return new_course

# # GET single course by id
# @app.get("/courses/{course_id}")
# def get_course(course_id: int):
#     cursor.execute(
#         "SELECT * FROM course WHERE id = %s",
#         (course_id,)
#     )
#     course = cursor.fetchone()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")
#     return course

# @app.delete('/courses/{course_id}')
# def delete_course(course_id: int):
#     cursor.execute(
#         "DELETE FROM course WHERE id = %s RETURNING *",
#         (course_id,)
#     )
#     deleted_course = cursor.fetchone()
#     conn.commit()

#     if deleted_course is None:
#         raise HTTPException(status_code=404, detail="Course not found")
    
#     return {
#         "message": "Course deleted successfully",
#         "data": deleted_course
#     }

# @app.put("/courses/{course_id}")
# def update_course(course_id: int, course: Course):
#     cursor.execute(
#         """
#         UPDATE public.course
#         SET 
#             name = %s,
#             "Instructor" = %s,
#             "Duration" = %s,
#             website = %s
#         WHERE id = %s
#         RETURNING *
#         """,
#         (
#             course.name,
#             course.instructor,
#             course.duration,
#             str(course.website),
#             course_id
#         )
#     )

#     updated_course = cursor.fetchone()
#     conn.commit()

#     if updated_course is None:
#         raise HTTPException(status_code=404, detail="Course not found")

#     return {
#         "message": "Course updated successfully",
#         "data": updated_course
#     }