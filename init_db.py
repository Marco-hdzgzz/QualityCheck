from database import engine, Base, SessionLocal
from models import Maquina, Usuario

def inicializar_bd():
    print("Creando tablas en PostgreSQL...")
    # Crea todas las tablas definidas en models.py si no existen
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")

    # Insertar datos de prueba opcionales
    db = SessionLocal()
    try:
        # Verificar si ya existe al menos un usuario
        usuario_existente = db.query(Usuario).first()
        if not usuario_existente:
            print("Creando usuario inicial de prueba...")
            usuario_admin = Usuario(
                nombre="Admin Prueba",
                correo="admin@qualitycheck.com",
                contrasena_hash="1234",  # Contraseña plana para pruebas iniciales
                activo=True
            )
            db.add(usuario_admin)
            db.commit()
            print("✅ Usuario creado con éxito: admin@qualitycheck.com / 1234")
        else:
            print("ℹ️ Ya existen usuarios en la base de datos.")
            
    except Exception as e:
        print(f"Error al insertar usuario de prueba: {e}")
        db.rollback()
    

    try:
        if not db.query(Maquina).first():
            maquina_demo = Maquina(
                codigo_maquina="MAQ-003",
                nombre="Torno CNC 03",
                tipo="Torno CNC",
                marca="Haas",
                modelo="ST-20",
                numero_serie="SN-99812",
                area="Producción",
                ubicacion="Línea 2",
                estado="Operativa"
            )
            db.add(maquina_demo)
            db.commit()
            print("Máquina de prueba insertada correctamente.")
    finally:
        db.close()

if __name__ == "__main__":
    inicializar_bd()
