class NodoSimple:
    """
    Nodo para estructuras simplemente enlazadas.

    Cada nodo almacena:
    - Un dato.
    - Una referencia al siguiente nodo.
    """

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class NodoDoble:
    """
    Nodo para estructuras doblemente enlazadas.

    Cada nodo almacena:
    - Un dato.
    - Una referencia al nodo anterior.
    - Una referencia al nodo siguiente.
    """

    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None