from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_csrf import CSRFMiddleware
from app.backend.db.session import engine
from app.backend.db.base import Base
from app.backend.auth.routers import user_router
from app.backend.auth.models import Token
from jose import jwt
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

    class CSRFMiddlewareWrapper(BaseHTTPMiddleware):
        def __init__(self, app, secret_key):
            super().__init__(app)
            self.csrf_middleware = CSRFMiddleware(app, secret=secret_key)

        async def __call__(self, scope, receive, send):
            await self.csrf_middleware(scope, receive, send)

    app.add_middleware(CSRFMiddlewareWrapper, secret_key=JWT_SECRET_KEY)
    origins = [
    "http://localhost:3000",  # Przykład, jeśli frontend działa na innym porcie
    "http://localhost:8008",  # Adres i port, na którym działa FastAPI
                ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    create_tables()  

    return app
app = start_application()

app.include_router(user_router)

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        data= kwargs['session'].query(Token).filter_by(user_id=user_id,access_toke=kwargs['dependencies'],status=True).first()
        if data:
            return func(kwargs['dependencies'],kwargs['session'])
        else:
            return {'msg': "Token blocked"}
    return wrapper
