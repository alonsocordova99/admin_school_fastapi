from pydantic import BaseModel


class ApiReponseSchema(BaseModel):
    status_code: int
    success: bool
    mensaje: str