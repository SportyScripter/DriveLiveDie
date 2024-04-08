from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from jose import jwt

from auth.schemas import (
    UserCreate,
    TokenSchema,
    RequestDetails,
    ChangePassword,
)
from db.session import get_db
from auth.utils import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    RoleChecker,
    get_current_active_user,
)
from auth.models import User, Token
from auth.auth_bearer import JWTBearer
from auth.utils import JWT_SECRET_KEY, ALGORITHM

user_router = APIRouter(prefix="/auth", tags=["auth"])


def check_is_correct_string(string: str):
    try:
        table_with_not_correct_characters = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
            "|",
            "\\",
            ":",
            ";",
            "'",
            '"',
            "<",
            ">",
            ",",
            ".",
            "?",
            "/",
            " ",
        ]
        if any(char in table_with_not_correct_characters for char in string):
            return False
        elif string.isnumeric():
            return False
    except Exception as e:
        return False
    return True


def password_is_correct(password: str):
    table_with_correct_chars = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "{",
        "}",
        "[",
        "]",
        "|",
        "\\",
        ":",
        ";",
        "'",
        '"',
        "<",
        ">",
        ",",
        ".",
        "?",
        "/",
    ]
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in table_with_correct_chars for char in password):
        return True
    return True


@user_router.post("/create-user")
async def register_user(
    authorization: Annotated[bool, Depends(RoleChecker(allowed_roles=["admin"]))],
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        if existing_user := db.query(User).filter_by(email=user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        if not check_is_correct_string(user.username):
            raise HTTPException(
                status_code=400, detail="Username can only contain letters and numbers"
            )
        if not check_is_correct_string(user.last_name):
            raise HTTPException(
                status_code=400, detail="Last name can only contain letters and numbers"
            )
        if not check_is_correct_string(user.name):
            raise HTTPException(
                status_code=400, detail="Name can only contain letters and numbers"
            )
        if not password_is_correct(user.password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number and one special character",
            )
        encrypted_password = get_hashed_password(user.password)
        new_user = User(
            **UserCreate(
                name=user.name,
                last_name=user.last_name,
                password=user.password,
                email=user.email,
                username=user.username,
                role=user.role,
            ).dict()
        )
        new_user.hashed_password = encrypted_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": "User created successfully",
            "data": {"username": new_user.username, "email": new_user.email},
        }
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")


@user_router.post("/login", response_model=TokenSchema)
async def login(request: RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email"
        )
    user.is_active = True
    hashed_pass = user.hashed_password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    token_db = Token(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        status=True,
    )
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.post("/change-password")
async def change_password(request: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email"
        )

    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password"
        )
    encrypted_password = get_hashed_password(request.new_password)
    user.hashed_password = encrypted_password
    user.password = request.new_password
    db.commit()
    return {"message": "Password changed successfully"}


@user_router.post("/logout")
async def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    try:
        token = dependencies  # Pobranie tokenu JWT zależności JWTBearer
        payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        user_id = payload["sub"]
        token_records = db.query(Token).filter(Token.user_id == user_id).all()
        user = db.query(User).filter(User.id == user_id).first()
        user.is_active = False
        for token_record in token_records:
            db.delete(token_record)
        db.commit()
        return {"message": "User logged out successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.get("/users/me")
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
