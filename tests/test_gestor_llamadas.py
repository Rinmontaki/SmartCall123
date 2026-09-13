import unittest
from typing import Any

from models.llamada import EstadoLlamada, Llamada, Prioridad
from models.operacion import TipoOperacion
from services.gestor_llamadas import GestorLlamadas


class TestGestorLlamadas(unittest.TestCase):
    """
    Pruebas unitarias del servicio principal
    de gestión de llamadas de SmartCall 123.
    """

    def setUp(self) -> None:
        """
        Crea un gestor nuevo antes de ejecutar cada test.

        Esto garantiza que cada prueba sea independiente
        y no comparta datos con las demás.
        """
        self.gestor = GestorLlamadas()

    def registrar_llamada(
        self,
        **cambios: Any
    ) -> Llamada:
        """
        Registra una llamada válida utilizando valores
        predeterminados.

        Los valores pueden modificarse mediante **cambios
        para probar diferentes escenarios.
        """

        datos = {
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

        return self.gestor.registrar_llamada(**datos)

    def test_gestor_inicia_con_colas_vacias(self) -> None:
        self.assertTrue(
            self.gestor.cola_p1.esta_vacia()
        )

        self.assertTrue(
            self.gestor.cola_p2.esta_vacia()
        )

        self.assertTrue(
            self.gestor.cola_p3.esta_vacia()
        )

    def test_registro_genera_identificadores_secuenciales(
        self
    ) -> None:
        primera = self.registrar_llamada()
        segunda = self.registrar_llamada()

        self.assertEqual(
            primera.id_llamada,
            "L001"
        )

        self.assertEqual(
            segunda.id_llamada,
            "L002"
        )

    def test_registro_coloca_llamada_critica_en_p1(
        self
    ) -> None:
        llamada = self.registrar_llamada(
            peligro_inmediato=True
        )

        self.assertEqual(
            llamada.prioridad,
            Prioridad.CRITICA
        )

        self.assertEqual(
            self.gestor.cola_p1.tamano(),
            1
        )

    def test_registro_coloca_llamada_alta_en_p2(
        self
    ) -> None:
        llamada = self.registrar_llamada(
            heridos=True
        )

        self.assertEqual(
            llamada.prioridad,
            Prioridad.ALTA
        )

        self.assertEqual(
            self.gestor.cola_p2.tamano(),
            1
        )

    def test_registro_coloca_llamada_normal_en_p3(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.assertEqual(
            llamada.prioridad,
            Prioridad.NORMAL
        )

        self.assertEqual(
            self.gestor.cola_p3.tamano(),
            1
        )

    def test_llamada_registrada_queda_en_espera(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.assertEqual(
            llamada.estado,
            EstadoLlamada.EN_ESPERA
        )

    def test_registro_se_guarda_en_pila_de_operaciones(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        operacion = (
            self.gestor
            .pila_operaciones
            .ver_tope()
        )

        self.assertEqual(
            operacion.tipo,
            TipoOperacion.REGISTRAR
        )

        self.assertEqual(
            operacion.id_llamada,
            llamada.id_llamada
        )

    def test_siguiente_llamada_respeta_prioridad(
        self
    ) -> None:
        # P3
        self.registrar_llamada()

        # P2
        self.registrar_llamada(
            heridos=True
        )

        # P1
        llamada_p1 = self.registrar_llamada(
            peligro_inmediato=True
        )

        siguiente = (
            self.gestor
            .obtener_siguiente_llamada()
        )

        if siguiente is None:
            self.fail(
                "Se esperaba una siguiente llamada."
            )

        self.assertEqual(
            siguiente.id_llamada,
            llamada_p1.id_llamada
        )

    def test_atender_cambia_estado_de_la_llamada(
        self
    ) -> None:
        llamada = self.registrar_llamada(
            peligro_inmediato=True
        )

        atendida = (
            self.gestor
            .atender_siguiente_llamada()
        )

        if atendida is None:
            self.fail(
                "Se esperaba una llamada atendida."
            )

        self.assertEqual(
            atendida.id_llamada,
            llamada.id_llamada
        )

        self.assertEqual(
            atendida.estado,
            EstadoLlamada.EN_ATENCION
        )

    def test_atender_respeta_fifo_dentro_de_misma_prioridad(
        self
    ) -> None:
        primera = self.registrar_llamada(
            peligro_inmediato=True
        )

        segunda = self.registrar_llamada(
            peligro_inmediato=True
        )

        atendida = (
            self.gestor
            .atender_siguiente_llamada()
        )

        if atendida is None:
            self.fail(
                "Se esperaba una llamada atendida."
            )

        self.assertEqual(
            atendida.id_llamada,
            primera.id_llamada
        )

        siguiente = (
            self.gestor
            .cola_p1
            .ver_frente()
        )

        self.assertEqual(
            siguiente.id_llamada,
            segunda.id_llamada
        )

    def test_no_permite_atender_dos_llamadas_simultaneamente(
        self
    ) -> None:
        self.registrar_llamada()
        self.registrar_llamada()

        self.gestor.atender_siguiente_llamada()

        with self.assertRaises(RuntimeError):
            self.gestor.atender_siguiente_llamada()

    def test_finalizar_llamada_cambia_estado_a_atendida(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.atender_siguiente_llamada()

        finalizada = (
            self.gestor
            .finalizar_llamada_actual()
        )

        self.assertEqual(
            finalizada.id_llamada,
            llamada.id_llamada
        )

        self.assertEqual(
            finalizada.estado,
            EstadoLlamada.ATENDIDA
        )

        self.assertIsNone(
            self.gestor.llamada_en_atencion
        )
        
    def test_buscar_llamada_registrada(self) -> None:
        llamada = self.registrar_llamada()

        encontrada = self.gestor.buscar_llamada(
            llamada.id_llamada
        )

        self.assertIsNotNone(encontrada)

        if encontrada is None:
            self.fail("Se esperaba encontrar la llamada.")

        self.assertEqual(
            encontrada.id_llamada,
            llamada.id_llamada
        )

    def test_buscar_llamada_inexistente_retorna_none(
        self
    ) -> None:
        encontrada = self.gestor.buscar_llamada(
            "L999"
        )

        self.assertIsNone(encontrada)

    def test_cancelar_llamada_en_espera(self) -> None:
        llamada = self.registrar_llamada()

        cancelada = self.gestor.cancelar_llamada(
            llamada.id_llamada
        )

        self.assertEqual(
            cancelada.estado,
            EstadoLlamada.CANCELADA
        )

        self.assertTrue(
            self.gestor.cola_p3.esta_vacia()
        )

    def test_cancelar_registra_operacion_en_pila(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.cancelar_llamada(
            llamada.id_llamada
        )

        operacion = (
            self.gestor
            .pila_operaciones
            .ver_tope()
        )

        self.assertEqual(
            operacion.tipo,
            TipoOperacion.CANCELAR
        )

        self.assertEqual(
            operacion.id_llamada,
            llamada.id_llamada
        )

    def test_no_permite_cancelar_llamada_en_atencion(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.atender_siguiente_llamada()

        with self.assertRaises(RuntimeError):
            self.gestor.cancelar_llamada(
                llamada.id_llamada
            )

    def test_reclasificar_llamada_cambia_prioridad(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        reclasificada = (
            self.gestor.reclasificar_llamada(
                llamada.id_llamada,
                Prioridad.CRITICA
            )
        )

        self.assertEqual(
            reclasificada.prioridad,
            Prioridad.CRITICA
        )

        self.assertTrue(
            self.gestor.cola_p3.esta_vacia()
        )

        self.assertEqual(
            self.gestor.cola_p1.tamano(),
            1
        )

    def test_reclasificacion_respeta_fifo_en_nueva_cola(
        self
    ) -> None:
        primera_p1 = self.registrar_llamada(
            peligro_inmediato=True
        )

        llamada_p3 = self.registrar_llamada()

        self.gestor.reclasificar_llamada(
            llamada_p3.id_llamada,
            Prioridad.CRITICA
        )

        siguiente = (
            self.gestor
            .obtener_siguiente_llamada()
        )

        if siguiente is None:
            self.fail(
                "Se esperaba una siguiente llamada."
            )

        self.assertEqual(
            siguiente.id_llamada,
            primera_p1.id_llamada
        )

    def test_reclasificacion_se_registra_en_pila(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.reclasificar_llamada(
            llamada.id_llamada,
            Prioridad.ALTA
        )

        operacion = (
            self.gestor
            .pila_operaciones
            .ver_tope()
        )

        self.assertEqual(
            operacion.tipo,
            TipoOperacion.RECLASIFICAR
        )

        self.assertEqual(
            operacion.prioridad_anterior,
            Prioridad.NORMAL
        )

        self.assertEqual(
            operacion.prioridad_nueva,
            Prioridad.ALTA
        )

    def test_no_permite_reclasificar_a_misma_prioridad(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        with self.assertRaises(ValueError):
            self.gestor.reclasificar_llamada(
                llamada.id_llamada,
                Prioridad.NORMAL
            )
    
    def test_registro_temporal_guarda_llamada(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        registrada = (
            self.gestor
            .obtener_llamada_registrada(
                llamada.id_llamada
            )
        )

        self.assertIsNotNone(registrada)

        if registrada is None:
            self.fail(
                "Se esperaba encontrar la llamada registrada."
            )

        self.assertEqual(
            registrada.id_llamada,
            llamada.id_llamada
        )


    def test_registro_temporal_conserva_llamada_cancelada(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.cancelar_llamada(
            llamada.id_llamada
        )

        registrada = (
            self.gestor
            .obtener_llamada_registrada(
                llamada.id_llamada
            )
        )

        self.assertIsNotNone(registrada)

        if registrada is None:
            self.fail(
                "La llamada cancelada debe permanecer "
                "en el registro temporal."
            )

        self.assertEqual(
            registrada.estado,
            EstadoLlamada.CANCELADA
        )


    def test_registro_temporal_conserva_llamada_atendida(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.atender_siguiente_llamada()
        self.gestor.finalizar_llamada_actual()

        registrada = (
            self.gestor
            .obtener_llamada_registrada(
                llamada.id_llamada
            )
        )

        self.assertIsNotNone(registrada)

        if registrada is None:
            self.fail(
                "La llamada atendida debe permanecer "
                "en el registro temporal."
            )

        self.assertEqual(
            registrada.estado,
            EstadoLlamada.ATENDIDA
        )


    def test_obtener_llamada_registrada_inexistente(
        self
    ) -> None:
        registrada = (
            self.gestor
            .obtener_llamada_registrada(
                "L999"
            )
        )

        self.assertIsNone(registrada)
        
    def test_deshacer_sin_operaciones_genera_error(
        self
    ) -> None:
        with self.assertRaises(RuntimeError):
            self.gestor.deshacer_ultima_operacion()


    def test_deshacer_registro_elimina_llamada(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.deshacer_ultima_operacion()

        self.assertIsNone(
            self.gestor.obtener_llamada_registrada(
                llamada.id_llamada
            )
        )

        self.assertTrue(
            self.gestor.cola_p3.esta_vacia()
        )


    def test_deshacer_cancelacion_restaura_posicion(
        self
    ) -> None:
        primera = self.registrar_llamada()
        segunda = self.registrar_llamada()
        tercera = self.registrar_llamada()

        self.gestor.cancelar_llamada(
            segunda.id_llamada
        )

        self.gestor.deshacer_ultima_operacion()

        self.assertEqual(
            self.gestor.cola_p3.desencolar().id_llamada,
            primera.id_llamada
        )

        self.assertEqual(
            self.gestor.cola_p3.desencolar().id_llamada,
            segunda.id_llamada
        )

        self.assertEqual(
            self.gestor.cola_p3.desencolar().id_llamada,
            tercera.id_llamada
        )


    def test_deshacer_reclasificacion_restaura_cola(
        self
    ) -> None:
        primera = self.registrar_llamada()
        segunda = self.registrar_llamada()
        tercera = self.registrar_llamada()

        self.gestor.reclasificar_llamada(
            segunda.id_llamada,
            Prioridad.CRITICA
        )

        self.gestor.deshacer_ultima_operacion()

        self.assertTrue(
            self.gestor.cola_p1.esta_vacia()
        )

        self.assertEqual(
            self.gestor.cola_p3.desencolar().id_llamada,
            primera.id_llamada
        )

        self.assertEqual(
            self.gestor.cola_p3.desencolar().id_llamada,
            segunda.id_llamada
        )

        self.assertEqual(
            self.gestor.cola_p3.desencolar().id_llamada,
            tercera.id_llamada
        )


    def test_deshacer_atencion_restaura_llamada_al_frente(
        self
    ) -> None:
        primera = self.registrar_llamada()
        segunda = self.registrar_llamada()

        self.gestor.atender_siguiente_llamada()

        self.gestor.deshacer_ultima_operacion()

        self.assertIsNone(
            self.gestor.llamada_en_atencion
        )

        self.assertEqual(
            self.gestor.cola_p3.ver_frente().id_llamada,
            primera.id_llamada
        )

        self.assertEqual(
            self.gestor.cola_p3.tamano(),
            2
        )


    def test_deshacer_finalizacion_restaura_atencion(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.atender_siguiente_llamada()
        self.gestor.finalizar_llamada_actual()

        self.gestor.deshacer_ultima_operacion()

        actual = self.gestor.llamada_en_atencion

        if actual is None:
            self.fail(
                "Se esperaba una llamada en atención."
            )

        self.assertEqual(
            actual.id_llamada,
            llamada.id_llamada
        )

        self.assertEqual(
            actual.estado,
            EstadoLlamada.EN_ATENCION
        )


    def test_deshacer_respeta_orden_lifo(
        self
    ) -> None:
        llamada = self.registrar_llamada()

        self.gestor.reclasificar_llamada(
            llamada.id_llamada,
            Prioridad.CRITICA
        )

        self.gestor.cancelar_llamada(
            llamada.id_llamada
        )

        # Primero debe deshacer CANCELAR.
        operacion = (
            self.gestor
            .deshacer_ultima_operacion()
        )

        self.assertEqual(
            operacion.tipo,
            TipoOperacion.CANCELAR
        )

        self.assertEqual(
            llamada.prioridad,
            Prioridad.CRITICA
        )

        # Después debe deshacer RECLASIFICAR.
        operacion = (
            self.gestor
            .deshacer_ultima_operacion()
        )

        self.assertEqual(
            operacion.tipo,
            TipoOperacion.RECLASIFICAR
        )

        self.assertEqual(
            llamada.prioridad,
            Prioridad.NORMAL
        )


if __name__ == "__main__":
    unittest.main()