from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from admin_school_fastapi.app.core.utils.config import settings


engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}  # Solo para SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
