from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.modules.auth.jwt import decode_token


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # Public routes (adjust as needed)
        if request.url.path.startswith(("/auth", "/health", "/docs", "/openapi", "/odoo")):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"},
            )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization format"},
            )

        token = auth_header.replace("Bearer ", "").strip()

        try:
            payload = decode_token(token)

            if payload.get("type") != "access":
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token type"},
                )

            user_id = payload.get("sub")
            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token payload"},
                )

            # Attach user context
            request.state.user_id = user_id

        except ValueError as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e)},
            )

        return await call_next(request)
