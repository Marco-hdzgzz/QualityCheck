from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    #relaciones
    roles = relationship("usuarioRol", back_populates="usuario")

class rol(Base):
    __tablename__ = "roles"

    id_rol = Column (Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    #relaciones
    usuarios = relationship("usuarioRol", back_populates="rol")

class usuarioRol(Base):
    __tablename__ = "usuario_roles"

    id_usuario_rol = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    #relaciones
    usuario = relationship("Usuario")
    rol = relationship("rol")


class Maquina(Base):
    __tablename__ = "maquinas"

    id_maquina = Column(Integer, primary_key=True, index=True)
    codigo_maquina = Column(String(20), unique=True, nullable=False, index=True) # Ej: MAQ-001
    nombre = Column(String(150), nullable=False) # Ej: Torno CNC 03
    tipo = Column(String(100), nullable=False)   # Ej: Torno CNC
    marca = Column(String(100))                  # Ej: Haas
    modelo = Column(String(100))                 # Ej: ST-20
    numero_serie = Column(String(100), unique=True)
    area = Column(String(100), nullable=False)   # Ej: Producción
    ubicacion = Column(String(150))              # Ej: Línea 2
    estado = Column(String(50), default="Operativa", index=True) # Operativa, En revisión, Fuera de servicio
    activa = Column(Boolean, default=True)

class CriterioInspeccion(Base):
    __tablename__ = "criterios_inspeccion"

    id_criterio = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(100), nullable=False) #como: Seguridad, Calidad, Mantenimiento
    nombre_criterio = Column(String(150), nullable=False)
    description = Column(String, nullable=True)
    activo = Column(Boolean, default=True)

class Inspeccion(Base):
    __tablename__ = "revisiones"

    id_inspeccion = Column(Integer, primary_key=True, index=True)
    codigo_inspeccion = Column(String(20), unique=True, nullable=False) # Ej: INS-00001
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"), nullable=False)
    id_inspector = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    tipo_inspeccion = Column(String(50), nullable=False) # Preventiva, Correctiva, Rutina
    fecha_inspeccion = Column(DateTime, default=datetime.utcnow)
    resultado_final = Column(String(50)) # Aprobada, Requiere atención, No aprobada
    observaciones_generales = Column(String(500))

    #relaciones con tablas padre
    maquina = relationship("Maquina")
    inspector = relationship("Usuario")

    #relaciones con tablas hijo
    hallazgos = relationship("Hallazgo", back_populates="inspeccion")



class Hallazgo(Base):
    __tablename__ = "hallazgos"

    id_hallazgo = Column(Integer, primary_key=True, index=True)
    id_inspeccion = Column(Integer, ForeignKey("revisiones.id_inspeccion"), nullable=False)
    id_criterio = Column(Integer, ForeignKey("criterios_inspeccion.id_criterio"), nullable=False)
    nivel_severidad = Column(String(50), nullable=False) # Bajo, Medio, Alt
    descripcion = Column(String(500), nullable=False)
    estado = Column(String(50), default="Abierto") # Abierto, En proceso, Cerrado

    #relaciones
    inspeccion = relationship("Inspeccion", back_populates="hallazgos")
    acciones = relationship("AccionCorrectiva", back_populates="hallazgo")

class AccionCorrectiva(Base):
    __tablename__ = "acciones_correctivas"

    id_accion = Column(Integer, primary_key=True, index=True)
    id_hallazgo = Column(Integer, ForeignKey("hallazgos.id_hallazgo"), nullable=False)
    descripcion_accion= Column(String(500), nullable=False)
    responsable= Column(String(150), nullable=False)
    fecha_compromiso= Column(DateTime, nullable=False)
    completada= Column(Boolean, default=False)

    #relaciones
    hallazgo = relationship("Hallazgo", back_populates="acciones")

