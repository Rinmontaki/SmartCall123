import unittest

from structures.cola import Cola


class TestCola(unittest.TestCase):
    """
    Pruebas unitarias para verificar el comportamiento
    de la estructura Cola.
    """

    def test_cola_inicia_vacia(self):
        cola = Cola()

        self.assertTrue(cola.esta_vacia())
        self.assertEqual(cola.tamano(), 0)

    def test_encolar_primer_elemento(self):
        cola = Cola()

        cola.encolar("L001")

        self.assertFalse(cola.esta_vacia())
        self.assertEqual(cola.ver_frente(), "L001")
        self.assertEqual(cola.tamano(), 1)

    def test_encolar_varios_elementos(self):
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        self.assertEqual(cola.tamano(), 3)
        self.assertEqual(cola.ver_frente(), "L001")

    def test_desencolar_respeta_fifo(self):
        cola = Cola()

        cola.encolar("L001")
        cola.encolar("L002")
        cola.encolar("L003")

        self.assertEqual(cola.desencolar(), "L001")
        self.assertEqual(cola.desencolar(), "L002")
        self.assertEqual(cola.desencolar(), "L003")

    def test_cola_queda_vacia_al_retirar_ultimo_elemento(self):
        cola = Cola()

        cola.encolar("L001")
        cola.desencolar()

        self.assertTrue(cola.esta_vacia())
        self.assertEqual(cola.tamano(), 0)

    def test_desencolar_cola_vacia_genera_error(self):
        cola = Cola()

        with self.assertRaises(IndexError):
            cola.desencolar()

    def test_ver_frente_cola_vacia_genera_error(self):
        cola = Cola()

        with self.assertRaises(IndexError):
            cola.ver_frente()


if __name__ == "__main__":
    unittest.main()