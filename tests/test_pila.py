import unittest

from structures.pila import Pila


class TestPila(unittest.TestCase):
    """
    Pruebas unitarias para verificar el comportamiento
    de la estructura Pila.
    """

    def test_pila_inicia_vacia(self):
        pila = Pila()

        self.assertTrue(pila.esta_vacia())
        self.assertEqual(pila.tamano(), 0)

    def test_apilar_primer_elemento(self):
        pila = Pila()

        pila.apilar("OP001")

        self.assertFalse(pila.esta_vacia())
        self.assertEqual(pila.ver_tope(), "OP001")
        self.assertEqual(pila.tamano(), 1)

    def test_apilar_varios_elementos(self):
        pila = Pila()

        pila.apilar("OP001")
        pila.apilar("OP002")
        pila.apilar("OP003")

        self.assertEqual(pila.tamano(), 3)
        self.assertEqual(pila.ver_tope(), "OP003")

    def test_desapilar_respeta_lifo(self):
        pila = Pila()

        pila.apilar("OP001")
        pila.apilar("OP002")
        pila.apilar("OP003")

        self.assertEqual(pila.desapilar(), "OP003")
        self.assertEqual(pila.desapilar(), "OP002")
        self.assertEqual(pila.desapilar(), "OP001")

    def test_pila_queda_vacia_al_retirar_ultimo_elemento(self):
        pila = Pila()

        pila.apilar("OP001")
        pila.desapilar()

        self.assertTrue(pila.esta_vacia())
        self.assertEqual(pila.tamano(), 0)

    def test_desapilar_pila_vacia_genera_error(self):
        pila = Pila()

        with self.assertRaises(IndexError):
            pila.desapilar()

    def test_ver_tope_pila_vacia_genera_error(self):
        pila = Pila()

        with self.assertRaises(IndexError):
            pila.ver_tope()


if __name__ == "__main__":
    unittest.main()