## 1. Comando para levantar el servidor
> uv run fastapi dev


## 3. Mantener dependencias organizadas
> uv sync
> uv tree

## 4. MIGRACIONES CON ALEMBIC
Generas migración:
> alembic revision --autogenerate -m "cambio"
> alembic revision --autogenerate -m "create users table"

Ejecutas migración:
> alembic upgrade head

Revertir migración:
> alembic downgrade -1
> alembic downgrade *Code*

## 5. Levantas el servidor con:
> uv run fastapi dev


-- Init roles
> python -m app.db.init.init_roles


# FUNCIONES DEL SISTEMA

1. Administrar roles de usuarios (Admin)
    - Crear, leer y eliminar
    - Consultar roles (N° de usuarios) (Todos)
    - Consulta rol by id -> detalle de usuarios (nombre, usuario)

2. Administrar usuarios (Admin, Director)
    - Crear, leer y eliminar
    - Consulta de usuarios (Filtr por rol)
    - Consulta usuarios por id -> Nombre de rol, Docente o Estudiante
    - Registro de estudiante con su usuario
    - Registro de docente con su usuario
    - Registro de director con su usuario

3. Administrar cursos (Admin, Director)
    - Registrar y leer periodos (Admin, Director)
    - registrar cursos (Admin, Director)
    - Listado de cursos dependiendo de rol (Todos)
    - Eliminacion de curso (Admin)

4. Administrador de matriculas (Admin, Director)
    - Registrar matriculas (Admin, Director)
      Validacion si el usuario ya esta matriculado en el curso
    - listado de matriculas de acuerdo al curso (Admin, Director, Docente)
    - listado de matriculas del estudiante (Todos)
    - eliminacion de matricula

5. Adminitracion de clases (Docente)
    - Registrar clases (Docente)
      Validacion si el curso está activo
      Validar si el curso lo dicta el docente
      Ingresar fecha de inicio y fin, links de videos y materiales
    - Listado de clases (Docente y Alumno)
      Validar si el docente dicta el curso
      Validar si el alumno está matriculado en el curso
    - Eliminacion de clases (Docente)
      Validar si el docente dicta el curso
      Verificar si existen clases y evaluaciones asociadas

6. Administrador de evaluaciones (Docente)
    - Registrar evaluaciones (Docente)
      Validar si el docente dicta el curso
      validar si cada detalle de evaluacion tenga al estudiante matriculado
      validar la nota sea entre 0 y 20
    
    - Listado de evaluaciones (Docente y Alumno)
      Validar si el docente dicta el curso
      Validar si el alumno está matriculado en el curso

7. Reportes
    - Reporte de notas (Docente y Alumno)
      De acuerdo a la evaluacion, al curso y el estudiante
    - Reporte de matriculas (Docente, Director, Admin)
      De acuerdo al curso 