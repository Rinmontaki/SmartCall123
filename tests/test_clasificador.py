import unittest
from datetime import datetime

from models.llamada import Llamada, Prioridad
from services.clasificador import ClasificadorLlamadas


class TestClasificadorLlamadas(unittest.TestCase):
    """
    Pruebas unitarias para verificar la clasificación
    automática de llamadas de SmartCall 123.
    """

    def crear_llamada(self, **cambios):
        datos = {
            "id_llamada": "L001",
            "hora_llegada": datetime.now(),
            "tipo": "Reporte general",
            "ubicacion": "Popayán",
            "descripcion": "Situación reportada al 123",
            "personas_afectadas": 1,
            "consciente": True,
            "respira": True,
            "heridos": False,
            "peligro_inmediato": False,
            "riesgo_potencial": False,
        }

        datos.update(cambios)

        return Llamada(**datos)

    def test_clasifica_p1_si_persona_no_respira(self):
        llamada = self.crear_llamada(
            respira=False
        )

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.CRITICA)

    def test_clasifica_p1_si_persona_no_esta_consciente(self):
        llamada = self.crear_llamada(
            consciente=False
        )

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.CRITICA)

    def test_clasifica_p1_si_existe_peligro_inmediato(self):
        llamada = self.crear_llamada(
            peligro_inmediato=True
        )

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.CRITICA)

    def test_p1_tiene_precedencia_sobre_p2(self):
        llamada = self.crear_llamada(
            heridos=True,
            peligro_inmediato=True
        )

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.CRITICA)

    def test_clasifica_p2_si_existen_heridos(self):
        llamada = self.crear_llamada(
            heridos=True
        )

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.ALTA)

    def test_clasifica_p2_si_existe_riesgo_potencial(self):
        llamada = self.crear_llamada(
            riesgo_potencial=True
        )

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.ALTA)

    def test_clasifica_p3_si_no_existen_condiciones_de_mayor_riesgo(self):
        llamada = self.crear_llamada()

        prioridad = ClasificadorLlamadas.clasificar(llamada)

        self.assertEqual(prioridad, Prioridad.NORMAL)


if __name__ == "__main__":
    unittest.main()