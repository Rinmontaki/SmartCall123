from typing import Any


class NodoSimple:
    """
    Representa un nodo de una estructura simplemente enlazada.

    Cada nodo almacena un dato y una referencia
    al siguiente nodo.
    """

    def __init__(self, dato: Any) -> None:
        self.dato: Any = dato
        self.siguiente: NodoSimple | None = None


class NodoDoble:
    """
    Representa un nodo de una estructura doblemente enlazada.

    Cada nodo almacena un dato y referencias
    al nodo anterior y al nodo siguiente.
    """

    def __init__(self, dato: Any) -> None:
        self.dato: Any = dato

        self.anterior: NodoDoble | None = None
        self.siguiente: NodoDoble | None = None