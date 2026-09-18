import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# LA CONEXIÓN A LA BASE DE DATOS SE REALIZA EN ESTE ARCHIVO 

# Cargar variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No se encontró DATABASE_URL en el archivo .env")

# Crear el motor de conexión de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Crear la fábrica de sesiones para consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para definir nuestros modelos de datos
Base = declarative_base()

# Función helper para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()