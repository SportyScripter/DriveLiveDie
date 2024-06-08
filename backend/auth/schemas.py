from pydantic import BaseModel, EmailStr
import datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    username: str
    role = str

UserCreate.update_forward_refs()


class RequestDetails(BaseModel):
    email: str
    password: str

RequestDetails.update_forward_refs()

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

TokenSchema.update_forward_refs()

class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str

ChangePassword.update_forward_refs()


class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime.datetime

TokenCreate.update_forward_refs()