from collections.abc import Callable
from typing import Any

from structures.nodo import NodoSimple


class Cola:
    """
    Implementa una cola FIFO mediante una lista
    simplemente enlazada.

    Mantiene referencias al frente y al final para que
    las operaciones principales de encolado y desencolado
    sean eficientes.
    """

    def __init__(self) -> None:
        self.frente: NodoSimple | None = None
        self.final: NodoSimple | None = None
        self._tamano: int = 0

    def esta_vacia(self) -> bool:
        """
        Indica si la cola no contiene elementos.
        """
        return self.frente is None

    def encolar(self, dato: Any) -> None:
        """
        Agrega un elemento al final de la cola.
        """
        nuevo_nodo = NodoSimple(dato)

        if self.frente is None:
            self.frente = nuevo_nodo
            self.final = nuevo_nodo

        else:
            # Si existe un frente, una cola válida también
            # debe tener una referencia al nodo final.
            assert self.final is not None

            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

        self._tamano += 1

    def desencolar(self) -> Any:
        """
        Elimina y retorna el elemento ubicado al frente.

        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.frente is None:
            raise IndexError(
                "No se puede desencolar una cola vacía."
            )

        dato = self.frente.dato

        self.frente = self.frente.siguiente

        self._tamano -= 1

        # Si retiramos el último nodo, ambas referencias
        # deben quedar nuevamente en None.
        if self.frente is None:
            self.final = None

        return dato

    def ver_frente(self) -> Any:
        """
        Retorna el primer elemento sin eliminarlo.

        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.frente is None:
            raise IndexError(
                "No se puede consultar una cola vacía."
            )

        return self.frente.dato

    def tamano(self) -> int:
        """
        Retorna la cantidad de elementos almacenados.
        """
        return self._tamano

    def buscar(
        self,
        condicion: Callable[[Any], bool]
    ) -> Any | None:
        """
        Busca el primer elemento que cumpla la condición.

        Args:
            condicion: Función que recibe un elemento y
            retorna True cuando encuentra una coincidencia.

        Returns:
            El elemento encontrado o None si no existe.
        """
        actual = self.frente

        while actual is not None:
            if condicion(actual.dato):
                return actual.dato

            actual = actual.siguiente

        return None

    def eliminar(
        self,
        condicion: Callable[[Any], bool]
    ) -> Any | None:
        """
        Elimina y retorna el primer elemento que cumpla
        la condición indicada.

        Returns:
            El elemento eliminado o None si no existe.
        """
        if self.frente is None:
            return None

        # Caso 1: el elemento buscado está en el frente.
        if condicion(self.frente.dato):
            return self.desencolar()

        anterior = self.frente
        actual = self.frente.siguiente

        while actual is not None:
            if condicion(actual.dato):
                # Saltamos el nodo actual para quitarlo
                # de la lista simplemente enlazada.
                anterior.siguiente = actual.siguiente

                # Caso especial: estamos eliminando
                # el último nodo de la cola.
                if actual is self.final:
                    self.final = anterior

                self._tamano -= 1

                return actual.dato

            anterior = actual
            actual = actual.siguiente

        return None
    
    def obtener_posicion(
        self,
        condicion: Callable[[Any], bool]
    ) -> int | None:
        """
        Retorna la posición del primer elemento que cumpla
        la condición indicada.

        La primera posición de la cola corresponde al índice 0.

        Retorna None cuando no existe una coincidencia.
        """
        actual = self.frente
        posicion = 0

        while actual is not None:
            if condicion(actual.dato):
                return posicion

            actual = actual.siguiente
            posicion += 1

        return None
    
    def insertar_en_posicion(
        self,
        dato: Any,
        posicion: int
    ) -> None:
        """
        Inserta un elemento en una posición específica
        de la cola enlazada.

        Args:
            dato: Elemento que será almacenado.
            posicion: Índice donde será insertado.

        Raises:
            IndexError: Si la posición no es válida.
        """
        if posicion < 0 or posicion > self._tamano:
            raise IndexError(
                "La posición indicada no es válida."
            )

        if posicion == self._tamano:
            self.encolar(dato)
            return

        nuevo_nodo = NodoSimple(dato)

        if posicion == 0:
            nuevo_nodo.siguiente = self.frente
            self.frente = nuevo_nodo

            if self.final is None:
                self.final = nuevo_nodo

            self._tamano += 1
            return

        anterior = self.frente

        for _ in range(posicion - 1):
            assert anterior is not None
            anterior = anterior.siguiente

        assert anterior is not None

        nuevo_nodo.siguiente = anterior.siguiente
        anterior.siguiente = nuevo_nodo

        self._tamano += 1
        
    def obtener_elementos(self) -> list[Any]:
        """
        Retorna los elementos de la cola en orden FIFO
        sin modificar la estructura.

        Returns:
            list[Any]: Copia de los datos almacenados
            desde el frente hasta el final.
        """
        elementos: list[Any] = []

        actual = self.frente

        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos