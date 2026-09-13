from structures.nodo import NodoSimple


class Cola:
    """
    Implementa una cola FIFO mediante una lista
    simplemente enlazada.

    La estructura mantiene referencias al frente y al final
    para realizar inserciones y eliminaciones eficientemente.
    """

    def __init__(self):
        self.frente = None
        self.final = None
        self._tamano = 0

    def esta_vacia(self):
        """
        Indica si la cola no contiene elementos.
        """
        return self.frente is None

    def encolar(self, dato):
        """
        Agrega un elemento al final de la cola.
        """
        nuevo_nodo = NodoSimple(dato)

        if self.esta_vacia():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

        self._tamano += 1

    def desencolar(self):
        """
        Elimina y retorna el elemento ubicado al frente.

        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.esta_vacia():
            raise IndexError(
                "No se puede desencolar una cola vacía."
            )

        dato = self.frente.dato
        self.frente = self.frente.siguiente
        self._tamano -= 1

        if self.frente is None:
            self.final = None

        return dato

    def ver_frente(self):
        """
        Retorna el primer elemento sin retirarlo.

        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.esta_vacia():
            raise IndexError(
                "No se puede consultar una cola vacía."
            )

        return self.frente.dato

    def tamano(self):
        """
        Retorna la cantidad de elementos almacenados.
        """
        return self._tamano