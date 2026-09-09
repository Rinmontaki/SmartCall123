import unittest

from structures.nodo import NodoDoble, NodoSimple


class TestNodoSimple(unittest.TestCase):

    def test_crear_nodo_simple(self):
        nodo = NodoSimple("L001")

        self.assertEqual(nodo.dato, "L001")
        self.assertIsNone(nodo.siguiente)

    def test_enlazar_dos_nodos_simples(self):
        primero = NodoSimple("L001")
        segundo = NodoSimple("L002")

        primero.siguiente = segundo

        self.assertIs(primero.siguiente, segundo)


class TestNodoDoble(unittest.TestCase):

    def test_crear_nodo_doble(self):
        nodo = NodoDoble("L001")

        self.assertEqual(nodo.dato, "L001")
        self.assertIsNone(nodo.anterior)
        self.assertIsNone(nodo.siguiente)

    def test_enlazar_dos_nodos_dobles(self):
        primero = NodoDoble("L001")
        segundo = NodoDoble("L002")

        primero.siguiente = segundo
        segundo.anterior = primero

        self.assertIs(primero.siguiente, segundo)
        self.assertIs(segundo.anterior, primero)


if __name__ == "__main__":
    unittest.main()