from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from core import settings

api_key_header = APIKeyHeader(name="x-auth-token", auto_error=False)


def static_auth_token(
    api_key: str = Security(api_key_header),
) -> str:
    if api_key == settings.x_api_key:
        return api_key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")
