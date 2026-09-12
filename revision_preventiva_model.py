from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class RevisionPreventiva:
    id: str
    maquina_id: str
    responsable_id: str
    tipo_revision: str
    descripcion: str
    fecha_programada: str
    estado: str = "Programada"
    fecha_realizada: Optional[str] = None
    resultado: Optional[str] = None
    observaciones: str = ""
    acciones_realizadas: str = ""
    proxima_revision: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
