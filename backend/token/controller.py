from fastapi import Depends, APIRouter, HTTPException, status

from token.model import AccessTokenRequest, RefreshTokenRequest

token_controller = APIRouter(prefix="/token", tags=["Login"])

@token_controller.get("/access")
def get_access_token(req: AccessTokenRequest):
    return

@token_controller.get("/refresh")
def get_refresh_token(req: RefreshTokenRequest):
    return


