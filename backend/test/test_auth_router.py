from auth.models import User, Token
from main import app
from auth.utils import get_hashed_password
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from db.session import engine
from auth.routers import check_is_correct_string, password_is_correct

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # create session
client = TestClient(app)  # create test client


def create_test_admin(db):  # method for creating test admin user
    test_user = User(
        username="testadmin",
        email="testadmin@example.com",
        password="test123",
        hashed_password=get_hashed_password("test123"),
        name="Test",
        last_name="User",
        role="admin",
    )
    db.add(test_user)
    db.commit()


def test_login_success():
    db_session = SessionLocal()
    create_test_admin(db_session)  # create admin user for testing
    login_data = {
        "email": "testadmin@example.com",
        "password": "test123",
    }  # login data for admin user
    response = client.post("/auth/login", json=login_data)  # login admin user
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def delete_test_token(db, email: str):  # method for deleting test token
    user = db.query(User).filter(User.email == email).first()
    db.query(Token).filter(Token.user_id == user.id).delete()
    db.commit()
    return user.id


def test_delete_token():  # test delete token
    db_session = SessionLocal()
    user_id = delete_test_token(db_session, email="testadmin@example.com")
    assert db_session.query(Token).filter(Token.user_id == user_id).first() is None


def delete_test_user(db, email: str):  # method for deleting test user
    db.query(User).filter(User.email == email).delete()
    db.commit()


def test_delete_test_adimn():  # test delete admin user
    db_session = SessionLocal()
    delete_test_user(db_session, email="testadmin@example.com")
    assert (
        db_session.query(User).filter(User.email == "testadmin@example.com").first()
        is None
    )


def test_logout_success():  # test logout with token
    db_session = SessionLocal()
    create_test_admin(db_session)  # create admin user for testing
    login_data = {
        "email": "testadmin@example.com",
        "password": "test123",
    }  # login data for admin user
    response = client.post("/auth/login", json=login_data)  # login admin user
    access_token = response.json()["access_token"]  # get access token
    response = client.post(
        "/auth/logout", headers={"Authorization": f"Bearer {access_token}"}
    )  # logout admin user
    delete_test_user(db_session, email="testadmin@example.com")  # delete admin user
    assert response.status_code == 200
    assert response.json() == {"message": "User logged out successfully"}


def test_logout_fail_not_authenticated():  # test logout without token
    response = client.post("/auth/logout", headers={"Authorization": "Bearer"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_logout_fail_invalid_token():  # test logout with invalid token
    response = client.post(
        "/auth/logout", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid token or expired token"}


def create_test_user_with_user_role():  # template for creating test user
    test_user = {
        "name": "TestUser",
        "last_name": "UserTest",
        "password": "Testuser123!",
        "email": "testuser@example.com",
        "username": "testuser",
    }
    return test_user


def test_create_user_success():
    db_session = SessionLocal()
    test_user = create_test_user_with_user_role()  # create temp user for testing
    create_test_admin(db_session)  # create admin user for testing
    login_data = {
        "email": "testadmin@example.com",
        "password": "test123",
    }  # login data for admin user
    response = client.post("/auth/login", json=login_data)  # login admin user
    access_token = response.json()["access_token"]  # get access token
    response_create_user = client.post(
        "/auth/create-user",
        json=test_user,
        headers={"Authorization": f"Bearer {access_token}"},
    )  # create user
    logout_response = client.post(
        "/auth/logout", headers={"Authorization": f"Bearer {access_token}"}
    )  # logout admin user
    delete_test_user(db_session, email="testadmin@example.com")  # delete admin user
    assert response_create_user.status_code == 200
    assert response_create_user.json() == {
        "message": "User created successfully",
        "data": {"username": "testuser", "email": "testuser@example.com"},
    }
    assert logout_response.status_code == 200


def test_delete_test_user():  # test delete user
    db_session = SessionLocal()
    delete_test_user(db_session, email="testuser@example.com")
    assert (
        db_session.query(User).filter(User.email == "testuser@example.com").first()
        is None
    )


def test_correct_string():  # test check_is_correct_string function
    assert check_is_correct_string("test") == True
    assert check_is_correct_string("test123") == True
    assert check_is_correct_string("123") == False
    assert check_is_correct_string("test123@") == False
    assert check_is_correct_string("test123!") == False
    assert check_is_correct_string("test123#") == False
    assert check_is_correct_string("test123$") == False
    assert check_is_correct_string("test123%") == False
    assert check_is_correct_string("test123^") == False
    assert check_is_correct_string("test123&") == False
    assert check_is_correct_string("test123*") == False
    assert check_is_correct_string(123) == False


def test_password_is_correct():  # test password_is_correct function
    assert password_is_correct("Test123") == False
    assert password_is_correct("test123") == False
    assert password_is_correct("TEST123") == False
    assert password_is_correct("test") == False
    assert password_is_correct("123") == False
    assert password_is_correct("test123@") == False
    assert password_is_correct("test123!") == False
    assert password_is_correct("test123#") == False
    assert password_is_correct("test123$") == False
    assert password_is_correct("test123%") == False
    assert password_is_correct("Test123!") == True
    assert password_is_correct("Test123#") == True
    assert password_is_correct("T12$") == False

def test_vehicles_fetch(): 
    response = client.get("/vehicles")  
    assert response.status_code == 200
    assert response.json() == []

def test_users_fetch(): 
    response = client.get("/users")  
    assert response.status_code == 200
    assert response.json() == []