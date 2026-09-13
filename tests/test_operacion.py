import unittest
from datetime import datetime

from models.llamada import EstadoLlamada, Prioridad
from models.operacion import Operacion, TipoOperacion


class TestOperacion(unittest.TestCase):
    """
    Pruebas unitarias para verificar el comportamiento
    del modelo Operacion.
    """

    def test_crear_operacion_registro(self):
        operacion = Operacion(
            tipo=TipoOperacion.REGISTRAR,
            id_llamada="L001"
        )

        self.assertEqual(
            operacion.tipo,
            TipoOperacion.REGISTRAR
        )

        self.assertEqual(
            operacion.id_llamada,
            "L001"
        )

    def test_operacion_genera_fecha_automaticamente(self):
        operacion = Operacion(
            tipo=TipoOperacion.REGISTRAR,
            id_llamada="L001"
        )

        self.assertIsInstance(
            operacion.fecha_hora,
            datetime
        )

    def test_operacion_inicia_sin_datos_de_transicion(self):
        operacion = Operacion(
            tipo=TipoOperacion.REGISTRAR,
            id_llamada="L001"
        )

        self.assertIsNone(operacion.estado_anterior)
        self.assertIsNone(operacion.estado_nuevo)
        self.assertIsNone(operacion.prioridad_anterior)
        self.assertIsNone(operacion.prioridad_nueva)

    def test_operacion_guarda_cambio_de_prioridad(self):
        operacion = Operacion(
            tipo=TipoOperacion.RECLASIFICAR,
            id_llamada="L002",
            prioridad_anterior=Prioridad.ALTA,
            prioridad_nueva=Prioridad.CRITICA,
        )

        self.assertEqual(
            operacion.prioridad_anterior,
            Prioridad.ALTA
        )

        self.assertEqual(
            operacion.prioridad_nueva,
            Prioridad.CRITICA
        )

    def test_operacion_guarda_cambio_de_estado(self):
        operacion = Operacion(
            tipo=TipoOperacion.CANCELAR,
            id_llamada="L003",
            estado_anterior=EstadoLlamada.EN_ESPERA,
            estado_nuevo=EstadoLlamada.CANCELADA,
        )

        self.assertEqual(
            operacion.estado_anterior,
            EstadoLlamada.EN_ESPERA
        )

        self.assertEqual(
            operacion.estado_nuevo,
            EstadoLlamada.CANCELADA
        )

    def test_no_permite_id_de_llamada_vacio(self):
        with self.assertRaises(ValueError):
            Operacion(
                tipo=TipoOperacion.REGISTRAR,
                id_llamada=""
            )
    def test_operacion_guarda_posicion_anterior(self) -> None:
        operacion = Operacion(
            tipo=TipoOperacion.CANCELAR,
            id_llamada="L005",
            posicion_anterior=2,
        )

        self.assertEqual(
            operacion.posicion_anterior,
            2
        )


if __name__ == "__main__":
    unittest.main()