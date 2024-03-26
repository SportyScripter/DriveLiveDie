import requests
from auth.models import User , Token
from main import app
from auth.utils import get_hashed_password
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.session import engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)

def create_test_user(db):
    test_user = User(
                    username="testuser",
                    email="test@example.com",
                    password="test123",
                    hashed_password=get_hashed_password("test123"),
                    name = "Test",
                    last_name = "User",
                    role = "admin",
                    )
    db.add(test_user)
    db.commit()


def test_login_success():
    db_session = SessionLocal()
    # Ustawienie danych testowych
    create_test_user(db_session)
    login_data = {"email": "test@example.com", "password": "test123"}

    # Wysłanie zapytania do endpointu
    response = client.post("/auth/login", json=login_data)

    # Sprawdzenie, czy odpowiedź jest poprawna
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def delete_test_token(db):
    user = db.query(User).filter(User.email == "test@example.com").first()
    db.query(Token).filter(Token.user_id == user.id).delete()
    db.commit()
    return user.id

def test_delete_token():
    db_session = SessionLocal()
    user_id = delete_test_token(db_session)
    assert db_session.query(Token).filter(Token.user_id == user_id).first() is None

def delete_test_user(db):
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()

def test_delete_test_user():
    db_session = SessionLocal()
    delete_test_user(db_session)
    assert db_session.query(User).filter(User.email == "test@example.com").first() is None

def logaout_success():
    db_session = SessionLocal()
    create_test_user(db_session)
    login_data = {"email": "test@example.com", "password": "test123"}
    response = client.post("/auth/login", json=login_data)  
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}





