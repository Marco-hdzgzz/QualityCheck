from sqlalchemy.orm import Session
from models import Maquina, Inspeccion, Usuario, CriterioInspeccion, Hallazgo, AccionCorrectiva
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

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



# Obtener todas las máquinas activas
def obtener_todas_las_maquinas_activas(db: Session):
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

# Obtener únicamente las máquinas disponibles en el catálogo.
def obtener_todas_las_maquinas(db: Session):
    return (
        db.query(Maquina)
        .options(joinedload(Maquina.area_rel))
        .filter(Maquina.activa == True)
        .all()
    )

def obtener_maquina_por_codigo(db: Session, codigo_maquina: str):
    return (
        db.query(Maquina)
        .options(joinedload(Maquina.area_rel))  
        .filter(Maquina.codigo_maquina == codigo_maquina)
        .first()
    )

def actualizar_maquina(db: Session, id_maquina: int, datos: dict, criterios: list):
    # 1. Actualizar máquina
    maq_db = db.query(Maquina).filter(Maquina.id_maquina == id_maquina).first()
    if maq_db:
        for clave, valor in datos.items():
            setattr(maq_db, clave, valor)

        # 2. Reemplazar criterios antiguos por los nuevos
        db.query(CriterioInspeccion).filter(
            CriterioInspeccion.id_maquina == id_maquina
        ).delete()

        for crit in criterios:
            nuevo_crit = CriterioInspeccion(
                id_maquina=id_maquina,
                nombre_criterio=crit["nombre_criterio"],
                categoria=crit["categoria"],
                activo=True
            )
            db.add(nuevo_crit)

        db.commit()
        return maq_db
    return None

def eliminar_maquina(db: Session, id_maquina: int):
    """Elimina la máquina y los registros que dependen exclusivamente de ella."""
    maquina = db.query(Maquina).filter(Maquina.id_maquina == id_maquina).first()
    if not maquina:
        return False

    # Se eliminan primero los hijos para cumplir las llaves foráneas. Todo se
    # confirma junto; si ocurre un error, la sesión revierte la operación.
    ids_inspecciones = db.query(Inspeccion.id_inspeccion).filter(
        Inspeccion.id_maquina == id_maquina
    )
    ids_hallazgos = db.query(Hallazgo.id_hallazgo).filter(
        Hallazgo.id_inspeccion.in_(ids_inspecciones)
    )

    db.query(AccionCorrectiva).filter(
        AccionCorrectiva.id_hallazgo.in_(ids_hallazgos)
    ).delete(synchronize_session=False)
    db.query(Hallazgo).filter(
        Hallazgo.id_inspeccion.in_(ids_inspecciones)
    ).delete(synchronize_session=False)
    db.query(Inspeccion).filter(
        Inspeccion.id_maquina == id_maquina
    ).delete(synchronize_session=False)
    db.query(CriterioInspeccion).filter(
        CriterioInspeccion.id_maquina == id_maquina
    ).delete(synchronize_session=False)
    db.delete(maquina)
    db.commit()
    return True

def obtener_criterios_por_maquina(db: Session, id_maquina: int):
    """Obtiene los criterios activos asignados a una máquina específica."""
    return db.query(CriterioInspeccion).filter(
        CriterioInspeccion.id_maquina == id_maquina,
        CriterioInspeccion.activo == True
    ).all()

def crear_criterio_inspeccion(db: Session, id_maquina: int, nombre_criterio: str, categoria: str = "General"):
    """Inserta un nuevo criterio de inspección directamente en la base de datos."""
    nuevo_criterio = CriterioInspeccion(
        id_maquina=id_maquina,
        nombre_criterio=nombre_criterio,
        categoria=categoria,
        activo=True
    )
    db.add(nuevo_criterio)
    db.commit()
    db.refresh(nuevo_criterio)
    return nuevo_criterio

def eliminar_criterio_inspeccion(db: Session, id_criterio: int):
    """Elimina permanentemente un criterio de inspección por su ID."""
    criterio = db.query(CriterioInspeccion).filter(CriterioInspeccion.id_criterio == id_criterio).first()
    if criterio:
        db.delete(criterio)
        db.commit()
        return True
    return False

def guardar_inspeccion_completa(db: Session, datos_inspeccion: dict, resultados_criterios: list):
    # 1. Crear el registro principal de la inspección
    nueva_inspeccion = Inspeccion(**datos_inspeccion)
    db.add(nueva_inspeccion)
    db.flush()  # Obtener id_inspeccion

    hubo_fallas = False

    # 2. Guardar el detalle de cada criterio evaluado
    for item in resultados_criterios:
        detalle = Inspeccion(
            id_inspeccion=nueva_inspeccion.id_inspeccion,
            id_criterio=item["id_criterio"],
            cumple=item["cumple"],
            observaciones=item.get("observaciones")
        )
        if not item["cumple"]:
            hubo_fallas = True
        db.add(detalle)

    # 3. Determinar resultado y actualizar estado de la máquina
    maquina = db.query(Maquina).filter(Maquina.id_maquina == datos_inspeccion["id_maquina"]).first()
    if hubo_fallas:
        nueva_inspeccion.resultado_final = "Con Hallazgos / Mantenimiento Correctivo Requerido"
        if maquina:
            maquina.estado = "En revisión"
    else:
        nueva_inspeccion.resultado_final = "Aprobado (Sin hallazgos)"
        if maquina:
            maquina.estado = "Operativa"

    db.commit()
    return nueva_inspeccion


def obtener_criterios_activos(db: Session):
    ##el chechlist de criterios para mostrar al inspector
    return db.query(CriterioInspeccion).filter(CriterioInspeccion.activo == True).all()

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
