import unittest
from datetime import datetime

from models.llamada import EstadoLlamada, Llamada


class TestLlamada(unittest.TestCase):
    """
    Pruebas unitarias del modelo Llamada.
    """

    def crear_llamada_valida(self):
        return Llamada(
            id_llamada="L001",
            hora_llegada=datetime.now(),
            tipo="Accidente de tránsito",
            ubicacion="Calle 5 con Carrera 10",
            descripcion="Choque entre dos vehículos",
            personas_afectadas=2,
            consciente=True,
            respira=True,
            heridos=True,
            peligro_inmediato=False,
            riesgo_potencial=True,
        )

    def test_crear_llamada(self):
        llamada = self.crear_llamada_valida()

        self.assertEqual(llamada.id_llamada, "L001")
        self.assertEqual(llamada.tipo, "Accidente de tránsito")
        self.assertEqual(llamada.personas_afectadas, 2)

    def test_llamada_inicia_sin_prioridad(self):
        llamada = self.crear_llamada_valida()

        self.assertIsNone(llamada.prioridad)

    def test_llamada_inicia_como_recibida(self):
        llamada = self.crear_llamada_valida()

        self.assertEqual(
            llamada.estado,
            EstadoLlamada.RECIBIDA
        )

    def test_no_permite_personas_afectadas_negativas(self):
        with self.assertRaises(ValueError):
            Llamada(
                id_llamada="L002",
                hora_llegada=datetime.now(),
                tipo="Incendio",
                ubicacion="Barrio Centro",
                descripcion="Incendio residencial",
                personas_afectadas=-1,
                consciente=True,
                respira=True,
                heridos=False,
                peligro_inmediato=True,
                riesgo_potencial=True,
            )

    def test_no_permite_id_vacio(self):
        with self.assertRaises(ValueError):
            Llamada(
                id_llamada="",
                hora_llegada=datetime.now(),
                tipo="Accidente",
                ubicacion="Carrera 5",
                descripcion="Accidente menor",
                personas_afectadas=1,
                consciente=True,
                respira=True,
                heridos=False,
                peligro_inmediato=False,
                riesgo_potencial=False,
            )


if __name__ == "__main__":
    unittest.main()