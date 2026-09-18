from sqlalchemy.orm import Session
from models import Maquina, Inspeccion, Usuario, CriterioInspeccion, Hallazgo, AccionCorrectiva
from datetime import datetime

#OPERACIONES CRUD


# Verificar credenciales de usuario
def autenticar_usuario(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo, Usuario.activo == True).first()

def validar_login(db: Session, correo: str, contrasena: str):
    #para el inicio de sesion, que usuario y contraseña coincida
    usuario = autenticar_usuario(db, correo)

    if usuario and usuario.contrasena_hash == contrasena: 
        return usuario
    return None



# Obtener todas las máquinas registradas
def obtener_todas_las_maquinas(db: Session):
    return db.query(Maquina).filter(Maquina.activa == True).all()

# Obtener métricas para el Dashboard
def obtener_resumen_dashboard(db: Session):
    total_maquinas = db.query(Maquina).filter(Maquina.activa == True).count()
    operativas = db.query(Maquina).filter(Maquina.estado == "Operativa", Maquina.activa == True).count()
    en_revision = db.query(Maquina).filter(Maquina.estado == "En revisión", Maquina.activa == True).count()
    fuera_de_servicio = db.query(Maquina).filter(Maquina.estado == "Fuera de servicio", Maquina.activa == True).count()
    
    return {
        "total": total_maquinas,
        "operativas": operativas,
        "en_revision": en_revision,
        "fuera_de_servicio": fuera_de_servicio
    }

# Crear una nueva máquina en PostgreSQL
def crear_nueva_maquina(db: Session, datos_maquina: dict):
    nueva_maquina = Maquina(**datos_maquina)
    db.add(nueva_maquina)
    db.commit()
    db.refresh(nueva_maquina)
    return nueva_maquina

# Obtener todas las máquinas activas
def obtener_todas_las_maquinas(db: Session):
    return db.query(Maquina).filter(Maquina.activa == True).all()


def obtener_criterios_activos(db: Session):
    ##el chechlist de criterios para mostrar al inspector
    return db.query(CriterioInspeccion).filter(CriterioInspeccion.activo == True).all()

def crear_criterio(db: Session, categoria: str, nombre: str, descripcion: str = None):
    nuevo_criterio = CriterioInspeccion(
        categoria=categoria,
        nombre_criterio=nombre, 
        description=descripcion,
    )
    db.add(nuevo_criterio)
    db.commit()
    db.refresh(nuevo_criterio)
    return nuevo_criterio

def registrar_inspeccion_completa(db: Session, id_maquina: int, id_inspector: int, tipo: str, resultado: str, observaciones: str, lista_hallazgos: list =None):
    ##registrar la inspeccion y sus hallazgos asociados en una sola transaccion

    # 1. Generar código único de inspección (ej. INS-20260917-153022)
    codigo_unic = f"INS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    nueva_inspeccion = Inspeccion(
        codigo_inspeccion=codigo_unic,
        id_maquina=id_maquina,
        id_inspector=id_inspector,
        tipo_inspeccion=tipo,
        resultado_final=resultado,
        observaciones_generales=observaciones
    )
    db.add(nueva_inspeccion)
    db.commit()
    db.refresh(nueva_inspeccion)

    # 2. Registrar hallazgos si la inspección detectó fallas
    if lista_hallazgos:
        for item in lista_hallazgos:
            nuevo_hallazgo = Hallazgo(
                id_inspeccion=nueva_inspeccion.id_inspeccion,
                id_criterio=item.get("id_criterio"),
                nivel_severidad=item.get("nivel_severidad", "Media"),
                descripcion_falla=item.get("descripcion_falla"),
                estado="Abierto"
            )
            db.add(nuevo_hallazgo)
        db.commit()

    return nueva_inspeccion

def obtener_historial_revisiones_maquina(db: Session, id_maquina: int):
    #para obtener revisiones de una maquina en especifico
    return db.query(Inspeccion).filter(Inspeccion.id_maquina == id_maquina).order_by(Inspeccion.fecha_inspeccion.desc()).all()

def obtener_hallazgos_pendientes(db: Session):
    return db.query(Hallazgo).filter(Hallazgo.estado.in_(["Abierto", "En proceso"])).all()

# Obtener historial de revisiones
def obtener_historial_revisiones(db: Session, id_maquina: int | None = None):
    """Obtiene revisiones y prepara la tabla en bases instaladas previamente."""
    # `checkfirst` evita modificar la tabla cuando ya existe, pero permite que
    # instalaciones creadas antes de añadir el módulo de revisiones funcionen.
    Inspeccion.__table__.create(bind=db.get_bind(), checkfirst=True)

    consulta = db.query(Inspeccion)
    if id_maquina is not None:
        consulta = consulta.filter(Inspeccion.id_maquina == id_maquina)
    return consulta.order_by(Inspeccion.fecha_inspeccion.desc()).all()
