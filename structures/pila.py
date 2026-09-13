from structures.nodo import NodoSimple
from typing import Any

class Pila:
    """
    Implementa una pila LIFO mediante una lista
    simplemente enlazada.

    Todas las inserciones y eliminaciones se realizan
    desde el tope de la estructura.
    """

    def __init__(self):
        self.tope = None
        self._tamano = 0

    def esta_vacia(self):
        """
        Indica si la pila no contiene elementos.
        """
        return self.tope is None

    def apilar(self, dato):
        """
        Agrega un elemento al tope de la pila.
        """
        nuevo_nodo = NodoSimple(dato)

        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo

        self._tamano += 1

    def desapilar(self):
        """
        Elimina y retorna el elemento ubicado en el tope.

        Raises:
            IndexError: Si la pila está vacía.
        """
        if self.esta_vacia():
            raise IndexError(
                "No se puede desapilar una pila vacía."
            )

        nodo_tope = self.tope
        assert nodo_tope is not None

        dato = nodo_tope.dato
        self.tope = nodo_tope.siguiente

        self._tamano -= 1

        return dato

    def ver_tope(self):
        """
        Retorna el elemento del tope sin eliminarlo.

        Raises:
            IndexError: Si la pila está vacía.
        """
        if self.esta_vacia():
            raise IndexError(
                "No se puede consultar una pila vacía."
            )

        assert self.tope is not None
        return self.tope.dato

    def tamano(self):
        """
        Retorna la cantidad de elementos almacenados.
        """
        return self._tamano
    
    def obtener_elementos(self) -> list[Any]:
        """
        Retorna los elementos almacenados en la pila
        desde el tope hasta la base, sin modificarla.

        El primer elemento de la lista corresponde
        a la operación más reciente.
        """
        elementos: list[Any] = []

        actual = self.tope

        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos