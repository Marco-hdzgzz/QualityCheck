import json
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import uuid4

from detalle_maquina import MAQUINAS
from revision_preventiva_model import RevisionPreventiva


ESTADOS_VALIDOS = {
    "Pendiente",
    "Programada",
    "En proceso",
    "Completada",
    "Vencida",
    "Cancelada",
}

TIPOS_REVISION = [
    "Inspección visual",
    "Lubricación",
    "Limpieza preventiva",
    "Calibración",
    "Revisión eléctrica",
    "Revisión mecánica",
    "Seguridad",
    "Otro",
]


class RevisionPreventivaService:
    """Capa de servicio para Revisiones Preventivas.

    El proyecto actual no incluye una base de datos conectada, por lo que esta
    implementación persiste únicamente las revisiones en un archivo JSON local.
    La UI depende de este servicio y no del archivo directamente, de modo que la
    persistencia pueda sustituirse después por Firestore/SQL sin rehacer la vista.
    """

    def __init__(self, ruta_datos=None):
        base = Path(__file__).resolve().parent
        self.ruta_datos = Path(ruta_datos) if ruta_datos else base / "data" / "revisiones_preventivas.json"
        self.ruta_datos.parent.mkdir(parents=True, exist_ok=True)
        if not self.ruta_datos.exists():
            self._guardar([])

    def _leer(self) -> list[dict]:
        try:
            contenido = self.ruta_datos.read_text(encoding="utf-8").strip()
            return json.loads(contenido) if contenido else []
        except (json.JSONDecodeError, OSError):
            return []

    def _guardar(self, registros: list[dict]):
        self.ruta_datos.write_text(
            json.dumps(registros, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _ahora() -> str:
        return datetime.now().isoformat(timespec="seconds")

    @staticmethod
    def _parse_fecha(valor: str, campo: str = "fecha") -> date:
        if not valor:
            raise ValueError(f"{campo} es obligatoria.")
        try:
            return datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError(f"{campo} debe tener formato AAAA-MM-DD.") from exc

    def _validar_maquina(self, maquina_id: str):
        if maquina_id not in MAQUINAS:
            raise ValueError("La máquina seleccionada no existe.")

    def _validar_datos(self, datos: dict, parcial=False):
        requeridos = [
            "maquina_id",
            "responsable_id",
            "tipo_revision",
            "descripcion",
            "fecha_programada",
        ]
        if not parcial:
            for campo in requeridos:
                if not str(datos.get(campo, "")).strip():
                    raise ValueError(f"El campo {campo} es obligatorio.")

        if "maquina_id" in datos:
            self._validar_maquina(str(datos["maquina_id"]).strip())

        if "fecha_programada" in datos:
            self._parse_fecha(str(datos["fecha_programada"]).strip(), "fecha_programada")

        if datos.get("proxima_revision"):
            proxima = self._parse_fecha(str(datos["proxima_revision"]).strip(), "proxima_revision")
            programada = self._parse_fecha(
                str(datos.get("fecha_programada", "")).strip(),
                "fecha_programada",
            )
            if proxima < programada:
                raise ValueError("La próxima revisión no puede ser anterior a la fecha programada.")

        if "estado" in datos and datos["estado"] not in ESTADOS_VALIDOS:
            raise ValueError("Estado de revisión no válido.")

    def _estado_calculado(self, registro: dict) -> dict:
        copia = dict(registro)
        estado = copia.get("estado", "Programada")
        if estado not in {"Completada", "Cancelada"}:
            try:
                programada = self._parse_fecha(copia.get("fecha_programada", ""))
                if programada < date.today():
                    copia["estado"] = "Vencida"
                elif estado == "Vencida":
                    copia["estado"] = "Programada"
            except ValueError:
                pass
        return copia

    def crear(self, **datos) -> dict:
        self._validar_datos(datos)
        ahora = self._ahora()
        revision = RevisionPreventiva(
            id=f"REV-{uuid4().hex[:8].upper()}",
            maquina_id=str(datos["maquina_id"]).strip(),
            responsable_id=str(datos["responsable_id"]).strip(),
            tipo_revision=str(datos["tipo_revision"]).strip(),
            descripcion=str(datos["descripcion"]).strip(),
            fecha_programada=str(datos["fecha_programada"]).strip(),
            estado=datos.get("estado", "Programada"),
            observaciones=str(datos.get("observaciones", "")).strip(),
            proxima_revision=(str(datos.get("proxima_revision", "")).strip() or None),
            created_at=ahora,
            updated_at=ahora,
        )
        registros = self._leer()
        registros.append(revision.to_dict())
        self._guardar(registros)
        return self._estado_calculado(revision.to_dict())

    def listar(self, estado=None, maquina_id=None, responsable_id=None) -> list[dict]:
        registros = [self._estado_calculado(r) for r in self._leer()]
        if estado:
            registros = [r for r in registros if r["estado"] == estado]
        if maquina_id:
            registros = [r for r in registros if r["maquina_id"] == maquina_id]
        if responsable_id:
            registros = [r for r in registros if r["responsable_id"] == responsable_id]
        return sorted(registros, key=lambda r: (r.get("fecha_programada", ""), r.get("created_at", "")))

    def obtener(self, revision_id: str) -> dict:
        for registro in self._leer():
            if registro.get("id") == revision_id:
                return self._estado_calculado(registro)
        raise ValueError("La revisión preventiva no existe.")

    def actualizar(self, revision_id: str, **cambios) -> dict:
        registros = self._leer()
        for indice, registro in enumerate(registros):
            if registro.get("id") != revision_id:
                continue
            if registro.get("estado") in {"Completada", "Cancelada"}:
                raise ValueError("No se puede editar una revisión completada o cancelada.")
            mezcla = dict(registro)
            mezcla.update({k: v for k, v in cambios.items() if v is not None})
            self._validar_datos(mezcla)
            mezcla["updated_at"] = self._ahora()
            registros[indice] = mezcla
            self._guardar(registros)
            return self._estado_calculado(mezcla)
        raise ValueError("La revisión preventiva no existe.")

    def completar(
        self,
        revision_id: str,
        resultado: str,
        observaciones: str = "",
        acciones_realizadas: str = "",
        proxima_revision: str | None = None,
        responsable_id: str | None = None,
    ) -> dict:
        if not str(resultado).strip():
            raise ValueError("El resultado es obligatorio para completar la revisión.")
        registros = self._leer()
        for indice, registro in enumerate(registros):
            if registro.get("id") != revision_id:
                continue
            if registro.get("estado") == "Cancelada":
                raise ValueError("Una revisión cancelada no puede completarse.")
            if proxima_revision:
                self._parse_fecha(proxima_revision, "proxima_revision")
            registro.update(
                {
                    "estado": "Completada",
                    "fecha_realizada": date.today().isoformat(),
                    "resultado": resultado.strip(),
                    "observaciones": observaciones.strip(),
                    "acciones_realizadas": acciones_realizadas.strip(),
                    "proxima_revision": proxima_revision or registro.get("proxima_revision"),
                    "responsable_id": (responsable_id or registro.get("responsable_id", "")).strip(),
                    "updated_at": self._ahora(),
                }
            )
            registros[indice] = registro
            self._guardar(registros)
            return registro
        raise ValueError("La revisión preventiva no existe.")

    def cancelar(self, revision_id: str, observaciones: str = "") -> dict:
        registros = self._leer()
        for indice, registro in enumerate(registros):
            if registro.get("id") != revision_id:
                continue
            if registro.get("estado") == "Completada":
                raise ValueError("Una revisión completada no puede cancelarse.")
            registro["estado"] = "Cancelada"
            if observaciones.strip():
                registro["observaciones"] = observaciones.strip()
            registro["updated_at"] = self._ahora()
            registros[indice] = registro
            self._guardar(registros)
            return registro
        raise ValueError("La revisión preventiva no existe.")

    def eliminar(self, revision_id: str):
        registros = self._leer()
        encontrado = next((r for r in registros if r.get("id") == revision_id), None)
        if not encontrado:
            raise ValueError("La revisión preventiva no existe.")
        if encontrado.get("estado") not in {"Pendiente", "Programada", "Cancelada"}:
            raise ValueError("Solo se pueden eliminar revisiones pendientes, programadas o canceladas.")
        self._guardar([r for r in registros if r.get("id") != revision_id])

    def pendientes(self) -> list[dict]:
        return [r for r in self.listar() if r["estado"] in {"Pendiente", "Programada", "En proceso"}]

    def vencidas(self) -> list[dict]:
        return [r for r in self.listar() if r["estado"] == "Vencida"]

    def proximas(self, dias=30) -> list[dict]:
        limite = date.today() + timedelta(days=dias)
        salida = []
        for registro in self.listar():
            if registro["estado"] in {"Completada", "Cancelada", "Vencida"}:
                continue
            try:
                fecha_programada = self._parse_fecha(registro["fecha_programada"])
            except ValueError:
                continue
            if date.today() <= fecha_programada <= limite:
                salida.append(registro)
        return salida

    def historial(self) -> list[dict]:
        return [r for r in self.listar() if r["estado"] in {"Completada", "Cancelada"}]
