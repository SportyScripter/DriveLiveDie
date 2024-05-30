from fastapi import Depends, APIRouter, HTTPException, status

user_controller = APIRouter(prefix="/users", tags=["Users"])


@user_controller.get("/")
def get_users():
    return 