from fastapi import FastAPI
from app.database import SessionLocal, Base , engine


app = FastAPI()

# Inicjalizacja bazy danych
Base.metadata.create_all(bind=engine)




