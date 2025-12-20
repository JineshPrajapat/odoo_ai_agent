from fastapi import FastAPI

from app.api.v1 import chat, health, auth, odoo, agent_test

from app.core.startup import check_odoo_connection, check_db_connection
from app.modules.auth.middleware import AuthMiddleware
from app.exceptions.app_exceptions import AppException, generic_exception_handler, app_exception_handler
from app.odoo.registry.registry_builder import build_registry

app = FastAPI(title="Odoo AI Agent MVP")

# app.add_middleware(AuthMiddleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.on_event("startup")
def startup():
    check_db_connection()
    check_odoo_connection()
    # build_registry()


app.include_router(auth.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(odoo.router, prefix="/api/v1")
app.include_router(agent_test.router, prefix="/api/v1")