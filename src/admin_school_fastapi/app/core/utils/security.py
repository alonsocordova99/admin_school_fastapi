from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from admin_school_fastapi.app.services import users_services as crud_user
from admin_school_fastapi.app.db.models.usuario_model import Usuario
from admin_school_fastapi.app.core.helpers.errors_helper import exception_response_auth
from admin_school_fastapi.app.core.utils.jwt_coding import encode_jwt, decode_jwt

# Clave secreta (puedes moverla a tu .env)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise exception_response_auth()
    user = crud_user.get_user(user_id)
    if user is None:
        raise exception_response_auth()
    return user


def create_access_token(user: Usuario):
    data = {
        "sub": str(user.id),
        "email": user.email
    }
    return encode_jwt(data=data)
