from fastapi.responses import JSONResponse
from fastapi import HTTPException

def error_response_server(code: int=500, mensaje: str=""):
    return JSONResponse(
        status_code=code,
        content={
            "status_code": code,
            "success": False,
            "error": mensaje,
        },
    )

def exception_response_server(code: int=500, mensaje: str=""):
    return HTTPException(
        status_code=code,
        detail=mensaje,   
    )

def exception_response_auth(code: int=401, mensaje: str="No se pudo validar las credenciales"):
    return HTTPException(
        status_code=code,
        detail=mensaje,  
        headers={"WWW-Authenticate": "Bearer"},
    )