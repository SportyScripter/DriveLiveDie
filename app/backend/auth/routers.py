from fastapi import Depends, APIRouter, HTTPException , status
from sqlalchemy.orm import Session
from jose import jwt 
from datetime import datetime

from app.backend.auth.schemas import UserCreate , TokenSchema , RequestDetails, ChangePassword 
from app.backend.db.session import get_db 
from app.backend.core.config import settings 
from app.backend.auth.utils import  verify_password, create_access_token, create_refresh_token, get_hashed_password
from app.backend.auth.models import User, Token
from app.backend.auth.auth_bearer import JWTBearer

user_router = APIRouter(prefix= '/auth',tags=['auth'])

@user_router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        encrypted_password = get_hashed_password(user.password)
        new_user = User(username=user.username, email=user.email, hashed_password=encrypted_password, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "data": {"username": new_user.username, "email": new_user.email}}
    except Exception as e:
        raise HTTPException(status_code=403, detail="CSRF token verification failed")


@user_router.post("/login", response_model=TokenSchema)
async def login(request: RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    token_db = Token(user_id=user.id, access_token=access_token, refresh_token=refresh_token, status=True)
    db.add(token_db)
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}

@user_router.get('/getusers')
async def getusers(dependencies = Depends(JWTBearer()),session : Session  = Depends(get_db)):
    user = session.query(User).all()
    return user

@user_router.post('/change-password')
async def change_password(request: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    return {"message": "Password changed successfully"}

@user_router.post('/logout')
async def logout(dependencies = Depends(JWTBearer()), db: Session = Depends(get_db)):
    token = dependencies
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload['sub']
    token_record = db.querry(Token).all()
    info=[]
    for record in token_record:
            print("record", record)
            if (datetime.utcnow() - record.created_at).days > 1:
                info.append(record)
    if info:
        existing_token = db.query(Token).where(Token.user_id.in_(info)).delete()
        db.commit()
    existing_token = db.query(Token).filter(Token.user_id == user_id, Token.access_token == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
        return {"message": "User logged out successfully"}
    
    