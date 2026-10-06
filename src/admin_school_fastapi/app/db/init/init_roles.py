# app/db/init_db.py
from admin_school_fastapi.app.db.session import get_db_context
from admin_school_fastapi.app.db.models.rol_model import Rol
from admin_school_fastapi.app.db.models.usuario_model import Usuario, RoleEnum
from admin_school_fastapi.app.core.utils.hashing import get_password_hash

def init_roles():
    """Crea los roles base si no existen en la DB."""
    default_roles = [
        {"nombre": "Administrador", "descripcion": "Control total del sistema"},
        {"nombre": "Director", "descripcion": "Gestión académica y administrativa"},
        {"nombre": "Docente", "descripcion": "Gestión de cursos y evaluaciones"},
        {"nombre": "Estudiante", "descripcion": "Acceso a sus notas y evaluaciones"},
    ]

    default_users = [
        {"nombre": "Administrador", "email": "admin@email.com", "password": "123456", "rol_id": RoleEnum.ADMIN},
        {"nombre": "Director", "email": "director@email.com", "password": "123456", "rol_id": RoleEnum.DIRECTOR}
    ]

    with get_db_context() as db:
        for role_data in default_roles:
            role = db.query(Rol).filter_by(nombre=role_data["nombre"]).first()
            if not role:
                print("Creando rol", role_data["nombre"])
                new_role = Rol(**role_data)
                db.add(new_role)
            else:
                print("Rol", role_data["nombre"], "ya existe")

        for user_data in default_users:
            user = db.query(Usuario).filter_by(email=user_data["email"]).first()
            if not user:
                print("Creando usuario", user_data["nombre"])
                new_user = Usuario(
                    nombre=user_data["nombre"],
                    email=user_data["email"],
                    rol_id=user_data["rol_id"]
                )
                hashed_password = get_password_hash(user_data["password"])
                new_user.password_hash = hashed_password
                db.add(new_user)
            else:
                print("Usuario", user_data["nombre"], "ya existe")
        db.commit()


if __name__ == "__main__":
    print("🔄 Inicializando roles...")
    init_roles()
    print("✅ Roles creados correctamente (si no existían).")


