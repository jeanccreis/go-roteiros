from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials
        payload = decode_token(token)
        if payload is None:
            raise HTTPException(status_code=403, detail="Token inválido ou expirado")
        return payload
