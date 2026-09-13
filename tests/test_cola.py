import unittest

from structures.cola import Cola


class TestCola(unittest.TestCase):
    """
    Pruebas unitarias para verificar el comportamiento
    de la estructura Cola.
    """

    def test_cola_inicia_vacia(self) -> None:
        cola = Cola()

        self.assertTrue(
            cola.esta_vacia()
        )

        self.assertEqual(
            cola.tamano(),
            0
        )

    def test_encolar_primer_elemento(self) -> None:
        cola = Cola()

        cola.encolar("L001")

        self.assertFalse(
            cola.esta_vacia()
        )

        self.assertEqual(
            cola.ver_frente(),
            "L001"
        )

        self.assertEqual(
            cola.tamano(),
            1
        )

    def test_encolar_varios_elementos(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        self.assertEqual(
            cola.tamano(),
            3
        )

        self.assertEqual(
            cola.ver_frente(),
            "L001"
        )

    def test_desencolar_respeta_fifo(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        self.assertEqual(
            cola.desencolar(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L002"
        )

        self.assertEqual(
            cola.desencolar(),
            "L003"
        )

    def test_cola_queda_vacia_al_retirar_ultimo_elemento(
        self
    ) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.desencolar()

        self.assertTrue(
            cola.esta_vacia()
        )

        self.assertEqual(
            cola.tamano(),
            0
        )

    def test_desencolar_cola_vacia_genera_error(
        self
    ) -> None:
        cola = Cola()

        with self.assertRaises(IndexError):
            cola.desencolar()

    def test_ver_frente_cola_vacia_genera_error(
        self
    ) -> None:
        cola = Cola()

        with self.assertRaises(IndexError):
            cola.ver_frente()

    def test_buscar_elemento_existente(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        resultado = cola.buscar(
            lambda elemento:
                elemento == "L002"
        )

        self.assertEqual(
            resultado,
            "L002"
        )

    def test_buscar_elemento_inexistente(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")

        resultado = cola.buscar(
            lambda elemento:
                elemento == "L999"
        )

        self.assertIsNone(
            resultado
        )

    def test_eliminar_elemento_intermedio(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        eliminado = cola.eliminar(
            lambda elemento:
                elemento == "L002"
        )

        self.assertEqual(
            eliminado,
            "L002"
        )

        self.assertEqual(
            cola.tamano(),
            2
        )

        self.assertEqual(
            cola.ver_frente(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L003"
        )

    def test_eliminar_elemento_del_frente(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")

        eliminado = cola.eliminar(
            lambda elemento:
                elemento == "L001"
        )

        self.assertEqual(
            eliminado,
            "L001"
        )

        self.assertEqual(
            cola.ver_frente(),
            "L002"
        )

        self.assertEqual(
            cola.tamano(),
            1
        )

    def test_eliminar_elemento_final(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")

        eliminado = cola.eliminar(
            lambda elemento:
                elemento == "L002"
        )

        self.assertEqual(
            eliminado,
            "L002"
        )

        self.assertEqual(
            cola.tamano(),
            1
        )

        # Esta inserción comprueba indirectamente que
        # la referencia "final" quedó actualizada correctamente.
        cola.encolar("L003")

        self.assertEqual(
            cola.desencolar(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L003"
        )

    def test_eliminar_unico_elemento_deja_cola_vacia(
        self
    ) -> None:
        cola = Cola()

        cola.encolar("L001")

        eliminado = cola.eliminar(
            lambda elemento:
                elemento == "L001"
        )

        self.assertEqual(
            eliminado,
            "L001"
        )

        self.assertTrue(
            cola.esta_vacia()
        )

        self.assertEqual(
            cola.tamano(),
            0
        )

    def test_eliminar_elemento_inexistente(self) -> None:
        cola = Cola()

        cola.encolar("L001")

        eliminado = cola.eliminar(
            lambda elemento:
                elemento == "L999"
        )

        self.assertIsNone(
            eliminado
        )

        self.assertEqual(
            cola.tamano(),
            1
        )

        self.assertEqual(
            cola.ver_frente(),
            "L001"
        )
        
    def test_obtener_posicion_elemento_existente(self) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        posicion = cola.obtener_posicion(
            lambda elemento:
                elemento == "L002"
        )

        self.assertEqual(
            posicion,
            1
        )


    def test_obtener_posicion_elemento_inexistente(self) -> None:
        cola = Cola()

        cola.encolar("L001")

        posicion = cola.obtener_posicion(
            lambda elemento:
                elemento == "L999"
        )

        self.assertIsNone(
            posicion
        )


    def test_insertar_elemento_en_posicion_intermedia(
        self
    ) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L003")

        cola.insertar_en_posicion(
            "L002",
            1
        )

        self.assertEqual(
            cola.desencolar(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L002"
        )

        self.assertEqual(
            cola.desencolar(),
            "L003"
        )


    def test_insertar_elemento_en_frente(self) -> None:
        cola = Cola()

        cola.encolar("L002")

        cola.insertar_en_posicion(
            "L001",
            0
        )

        self.assertEqual(
            cola.desencolar(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L002"
        )


    def test_insertar_elemento_al_final(self) -> None:
        cola = Cola()

        cola.encolar("L001")

        cola.insertar_en_posicion(
            "L002",
            1
        )

        self.assertEqual(
            cola.desencolar(),
            "L001"
        )

        self.assertEqual(
            cola.desencolar(),
            "L002"
        )


    def test_insertar_en_posicion_invalida_genera_error(
        self
    ) -> None:
        cola = Cola()

        with self.assertRaises(IndexError):
            cola.insertar_en_posicion(
                "L001",
                1
            )
    def test_obtener_elementos_respeta_orden_fifo(
        self
    ) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        elementos = cola.obtener_elementos()

        self.assertEqual(
            elementos,
            ["L001", "L002", "L003"]
        )


    def test_obtener_elementos_no_modifica_cola(
        self
    ) -> None:
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")

        elementos = cola.obtener_elementos()

        self.assertEqual(
            elementos,
            ["L001", "L002"]
        )

        self.assertEqual(
            cola.tamano(),
            2
        )

        self.assertEqual(
            cola.ver_frente(),
            "L001"
        )


    def test_obtener_elementos_cola_vacia(
        self
    ) -> None:
        cola = Cola()

        elementos = cola.obtener_elementos()

        self.assertEqual(
            elementos,
            []
        )

if __name__ == "__main__":
    unittest.main()