from fastapi import FastAPI

from app.config.database import Base, engine
from app.models.department_model import Department
from app.models.user_model import User
from app.models.task_model import Task
from app.models.notification_model import Notification

from app.routes.auth_routes import router as auth_router
from app.routes.department_routes import router as department_router
from app.routes.user_routes import router as user_router
from app.routes.task_routes import router as task_router
from app.routes.notification_routes import router as notification_router
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(department_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(notification_router)


@app.get("/")
def test_connection():
    return {
        "message": "Database connected successfully"
    }