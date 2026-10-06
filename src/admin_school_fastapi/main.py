from fastapi import FastAPI, HTTPException, Request
from admin_school_fastapi.app.db.session import engine
from admin_school_fastapi.app.db.base import Base
from admin_school_fastapi.app.routers import auth_router, clases_router, cursos_router, evaluaciones_router, roles_router
from admin_school_fastapi.app.routers import(
    users_router
)
from admin_school_fastapi.app.core.helpers.errors_helper import error_response_server
from admin_school_fastapi.app.core.utils.logging_config import logger

from admin_school_fastapi.app.routers import matricula_router


app = FastAPI(title="Sistema de Evaluaciones")

@app.on_event("startup")
async def startup():
    logger.info("*****************************************************")
    logger.info("Iniciando el servidor de la aplicacion")
    ## crear un fastapi en letras grandes
    logger.info("======================================================")
    logger.info("--  ____   ____   ____  ____   ____    ____  _____  --")
    logger.info("-- |      |    | |        |   |    |  |    |   |    --")
    logger.info("-- |____  |____| |____    |   |____|  |____|   |    --")
    logger.info("-- |      |    |      |   |   |    |  |        |    --")
    logger.info("-- |      |    |  ____|   |   |    |  |      __|__  --")
    logger.info("======================================================")
    logger.info("INICIO DE ACCESO A LA BASE DE DATOS")
    Base.metadata.create_all(bind=engine)
    logger.info("Fin a la base de datos - CORRECTO")

import json

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("------------------------------------------")
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return error_response_server(500, "Error interno del servidor")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response_server(exc.status_code, exc.detail)



app.include_router(roles_router.router)
app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(cursos_router.router)
app.include_router(clases_router.router)
app.include_router(evaluaciones_router.router)
app.include_router(matricula_router.router)
