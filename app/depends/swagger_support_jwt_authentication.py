from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi_users.authentication import JWTAuthentication
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.websockets import WebSocket


class SwaggerSupportHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None) -> Optional[str]:
        if request:
            authorization: str = request.headers.get("Authorization")
        elif websocket:
            authorization: str = "Bearer " + websocket.query_params.get("token")
        else:
            raise Exception('request or websocket must exist')

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class SwaggerSupportJWTAuthentication(JWTAuthentication):
    scheme: SwaggerSupportHTTPBearer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheme: SwaggerSupportHTTPBearer = SwaggerSupportHTTPBearer()
