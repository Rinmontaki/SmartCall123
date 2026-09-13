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


if __name__ == "__main__":
    unittest.main()