from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base import Base
from auth.routers import user_router
from core.config import settings
from auth.utils import JWT_SECRET_KEY, ALGORITHM
from auth.models import Token
from functools import wraps
from routes.vehicle import vehicle_router
import pytest

pytest.main()


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
        secret_key=JWT_SECRET_KEY,
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
app.include_router(vehicle_router)


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs["dependencies"], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload["sub"]
        data = (
            kwargs["session"]
            .query(Token)
            .filter_by(
                user_id=user_id, access_token=kwargs["dependencies"], status=True
            )
            .first()
        )
        if data:
            return func(kwargs["dependencies"], kwargs["session"])
        else:
            return {"msg": "Token blocked"}

    return wrapper
