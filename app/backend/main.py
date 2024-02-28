from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.backend.db.session import engine
from app.backend.db.base import Base
from app.backend.auth.routers import user_router
from app.backend.core.config import settings
from app.backend.auth.utils import JWT_SECRET_KEY, ALGORITHM

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully and updated if necessary.")
    except Exception as e:
        print("Error creating tables:", e)
        


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url="/api/v1/openapi.json",
        secret_key=JWT_SECRET_KEY
    )
    app.add_middleware(
        CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    create_tables()  

    return app


app = start_application()

app.include_router(user_router)

