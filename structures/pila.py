from structures.nodo import NodoSimple


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

        dato = self.tope.dato
        self.tope = self.tope.siguiente

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

        return self.tope.dato

    def tamano(self):
        """
        Retorna la cantidad de elementos almacenados.
        """
        return self._tamano