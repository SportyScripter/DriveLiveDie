import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.utils import JWT_SECRET_KEY, ALGORITHM


def decodeJWT(jwtoken: str):
    try:
        return jwt.decode(jwtoken, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code",
            )
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403,
                detail="Invalid authentication scheme",
            )
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(
                status_code=403,
                detail="Invalid token or expired token",
            )
        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:
        try:
            payload = decodeJWT(token)
        except Exception:
            payload = None
        return bool(payload)


jwt_bearer = JWTBearer()
