import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from revision_preventiva_service import RevisionPreventivaService


class RevisionesPreventivasIntegrationTest(unittest.TestCase):
    """Punto 23: pruebas de integración de la capa de revisiones preventivas."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = RevisionPreventivaService(Path(self.tmp.name) / "revisiones.json")
        self.base = dict(
            maquina_id="MAQ-01",
            responsable_id="maria.lopez",
            tipo_revision="Inspección visual",
            descripcion="Prueba de integración",
            fecha_programada=(date.today() + timedelta(days=5)).isoformat(),
            observaciones="",
            proxima_revision=None,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_flujo_crear_editar_completar_historial(self):
        revision = self.service.crear(**self.base)
        self.assertEqual(revision["estado"], "Programada")
        self.assertEqual(len(self.service.listar()), 1)

        editada = self.service.actualizar(revision["id"], descripcion="Descripción actualizada")
        self.assertEqual(editada["descripcion"], "Descripción actualizada")

        completada = self.service.completar(
            revision["id"],
            resultado="Aprobada",
            observaciones="Sin anomalías",
            acciones_realizadas="Limpieza y verificación",
        )
        self.assertEqual(completada["estado"], "Completada")
        self.assertEqual(len(self.service.historial()), 1)

    def test_cancelar_aparece_en_historial(self):
        revision = self.service.crear(**self.base)
        cancelada = self.service.cancelar(revision["id"], "Reprogramación")
        self.assertEqual(cancelada["estado"], "Cancelada")
        self.assertEqual(len(self.service.historial()), 1)

    def test_revision_pasada_se_calcula_vencida(self):
        datos = dict(self.base)
        datos["fecha_programada"] = (date.today() - timedelta(days=1)).isoformat()
        revision = self.service.crear(**datos)
        self.assertEqual(self.service.obtener(revision["id"])["estado"], "Vencida")

    def test_rechaza_maquina_inexistente(self):
        datos = dict(self.base)
        datos["maquina_id"] = "MAQ-999"
        with self.assertRaises(ValueError):
            self.service.crear(**datos)

    def test_persistencia_entre_instancias(self):
        revision = self.service.crear(**self.base)
        otro = RevisionPreventivaService(self.service.ruta_datos)
        self.assertEqual(otro.obtener(revision["id"])["id"], revision["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
