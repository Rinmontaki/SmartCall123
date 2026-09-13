from datetime import datetime

from models.llamada import EstadoLlamada, Llamada, Prioridad
from models.operacion import Operacion, TipoOperacion
from services.clasificador import ClasificadorLlamadas
from structures.cola import Cola
from structures.pila import Pila


class GestorLlamadas:
    """
    Coordina el flujo principal de llamadas de SmartCall 123.

    Se encarga de registrar, clasificar, encolar,
    seleccionar, atender y finalizar llamadas.
    """

    def __init__(self) -> None:
        self.cola_p1 = Cola()
        self.cola_p2 = Cola()
        self.cola_p3 = Cola()

        self.pila_operaciones = Pila()

        self.llamada_en_atencion: Llamada | None = None

        self._contador_llamadas: int = 0

        self._registro_llamadas: dict[str, Llamada] = {}

    def registrar_llamada(
        self,
        tipo,
        ubicacion,
        descripcion,
        personas_afectadas,
        consciente,
        respira,
        heridos,
        peligro_inmediato,
        riesgo_potencial,
    ):
        """
        Crea, clasifica y encola una nueva llamada.
        """

        llamada = Llamada(
            id_llamada=self._generar_id(),
            hora_llegada=datetime.now(),
            tipo=tipo,
            ubicacion=ubicacion,
            descripcion=descripcion,
            personas_afectadas=personas_afectadas,
            consciente=consciente,
            respira=respira,
            heridos=heridos,
            peligro_inmediato=peligro_inmediato,
            riesgo_potencial=riesgo_potencial,
        )

        prioridad = ClasificadorLlamadas.clasificar(
            llamada
        )

        llamada.prioridad = prioridad
        llamada.estado = EstadoLlamada.EN_ESPERA

        cola = self._obtener_cola(prioridad)

        cola.encolar(llamada)

        self._registro_llamadas[llamada.id_llamada] = llamada
        
        self._registrar_operacion_registro(llamada)
        
        return llamada

    def obtener_siguiente_llamada(self):
        """
        Retorna la siguiente llamada que debe ser atendida
        sin retirarla de su cola.
        """

        cola = self._obtener_primera_cola_disponible()

        if cola is None:
            return None

        return cola.ver_frente()

    def atender_siguiente_llamada(self):
        """
        Retira de las colas la llamada de mayor prioridad
        y la marca como llamada en atención.
        """

        if self.llamada_en_atencion is not None:
            raise RuntimeError(
                "Ya existe una llamada en atención."
            )

        cola = self._obtener_primera_cola_disponible()

        if cola is None:
            return None

        llamada = cola.desencolar()

        estado_anterior = llamada.estado

        llamada.estado = EstadoLlamada.EN_ATENCION

        self.llamada_en_atencion = llamada

        operacion = Operacion(
            tipo=TipoOperacion.ATENDER,
            id_llamada=llamada.id_llamada,
            estado_anterior=estado_anterior,
            estado_nuevo=EstadoLlamada.EN_ATENCION,
            prioridad_anterior=llamada.prioridad,
            prioridad_nueva=llamada.prioridad,
            posicion_anterior=0,  # La posición anterior no es relevante para esta operación
        )

        self.pila_operaciones.apilar(operacion)

        return llamada

    def finalizar_llamada_actual(self):
        """
        Finaliza la llamada que actualmente está siendo atendida.
        """

        if self.llamada_en_atencion is None:
            raise RuntimeError(
                "No existe ninguna llamada en atención."
            )

        llamada = self.llamada_en_atencion

        estado_anterior = llamada.estado

        llamada.estado = EstadoLlamada.ATENDIDA

        operacion = Operacion(
            tipo=TipoOperacion.FINALIZAR,
            id_llamada=llamada.id_llamada,
            estado_anterior=estado_anterior,
            estado_nuevo=EstadoLlamada.ATENDIDA,
            prioridad_anterior=llamada.prioridad,
            prioridad_nueva=llamada.prioridad,
        )

        self.pila_operaciones.apilar(operacion)

        self.llamada_en_atencion = None

        return llamada
    
    def _obtener_posicion_en_cola(
        self,
        cola: Cola,
        id_llamada: str
    ) -> int | None:
        """
        Retorna la posición de una llamada dentro
        de una cola.
        """

        return cola.obtener_posicion(
            lambda dato:
                isinstance(dato, Llamada)
                and dato.id_llamada == id_llamada
        )
    
    def buscar_llamada(
        self,
        id_llamada: str
    ) -> Llamada | None:
        """
        Busca una llamada que esté esperando
        o actualmente en atención.
        """

        if (
            self.llamada_en_atencion is not None
            and self.llamada_en_atencion.id_llamada
            == id_llamada
        ):
            return self.llamada_en_atencion

        for cola in (
            self.cola_p1,
            self.cola_p2,
            self.cola_p3,
        ):
            llamada = self._buscar_en_cola(
                cola,
                id_llamada
            )

            if llamada is not None:
                return llamada

        return None
    
    def cancelar_llamada(
        self,
        id_llamada: str
    ) -> Llamada:
        """
        Cancela una llamada que se encuentre esperando.

        Guarda su estado, prioridad y posición original
        para permitir posteriormente deshacer la operación.
        """

        llamada = self.buscar_llamada(id_llamada)

        if llamada is None:
            raise ValueError(
                "La llamada indicada no existe."
            )

        if llamada.estado != EstadoLlamada.EN_ESPERA:
            raise RuntimeError(
                "Solo se pueden cancelar llamadas "
                "que estén en espera."
            )

        if llamada.prioridad is None:
            raise RuntimeError(
                "La llamada no tiene una prioridad asignada."
            )

        cola = self._obtener_cola(
            llamada.prioridad
        )

        posicion_anterior = self._obtener_posicion_en_cola(
            cola,
            id_llamada
        )

        if posicion_anterior is None:
            raise RuntimeError(
                "No fue posible determinar la posición "
                "de la llamada."
            )

        eliminada = self._eliminar_de_cola(
            cola,
            id_llamada
        )

        if eliminada is None:
            raise RuntimeError(
                "No fue posible retirar la llamada "
                "de su cola."
            )

        estado_anterior = llamada.estado

        llamada.estado = EstadoLlamada.CANCELADA

        operacion = Operacion(
            tipo=TipoOperacion.CANCELAR,
            id_llamada=llamada.id_llamada,
            estado_anterior=estado_anterior,
            estado_nuevo=EstadoLlamada.CANCELADA,
            prioridad_anterior=llamada.prioridad,
            prioridad_nueva=llamada.prioridad,
            posicion_anterior=posicion_anterior,
        )

        self.pila_operaciones.apilar(
            operacion
        )

        return llamada

    def reclasificar_llamada(
        self,
        id_llamada: str,
        nueva_prioridad: Prioridad
    ) -> Llamada:
        """
        Cambia la prioridad de una llamada en espera.

        La llamada se elimina de su cola actual y se agrega
        al final de la nueva cola, conservando la información
        necesaria para deshacer la operación.
        """

        llamada = self.buscar_llamada(
            id_llamada
        )

        if llamada is None:
            raise ValueError(
                "La llamada indicada no existe."
            )

        if llamada.estado != EstadoLlamada.EN_ESPERA:
            raise RuntimeError(
                "Solo se pueden reclasificar llamadas "
                "que estén en espera."
            )

        prioridad_anterior = llamada.prioridad

        if prioridad_anterior is None:
            raise RuntimeError(
                "La llamada no tiene una prioridad asignada."
            )

        if prioridad_anterior == nueva_prioridad:
            raise ValueError(
                "La llamada ya pertenece "
                "a esa prioridad."
            )

        cola_anterior = self._obtener_cola(
            prioridad_anterior
        )

        posicion_anterior = self._obtener_posicion_en_cola(
            cola_anterior,
            id_llamada
        )

        if posicion_anterior is None:
            raise RuntimeError(
                "No fue posible determinar la posición "
                "original de la llamada."
            )

        eliminada = self._eliminar_de_cola(
            cola_anterior,
            id_llamada
        )

        if eliminada is None:
            raise RuntimeError(
                "No fue posible retirar la llamada "
                "de su cola actual."
            )

        llamada.prioridad = nueva_prioridad

        nueva_cola = self._obtener_cola(
            nueva_prioridad
        )

        nueva_cola.encolar(
            llamada
        )

        operacion = Operacion(
            tipo=TipoOperacion.RECLASIFICAR,
            id_llamada=llamada.id_llamada,
            estado_anterior=llamada.estado,
            estado_nuevo=llamada.estado,
            prioridad_anterior=prioridad_anterior,
            prioridad_nueva=nueva_prioridad,
            posicion_anterior=posicion_anterior,
        )

        self.pila_operaciones.apilar(
            operacion
        )

        return llamada
    
    def deshacer_ultima_operacion(
        self
    ) -> Operacion:
        """
        Revierte la última operación registrada utilizando
        el comportamiento LIFO de la pila.

        Returns:
            Operacion: Operación que fue deshecha.

        Raises:
            RuntimeError: Si no existen operaciones.
        """

        if self.pila_operaciones.esta_vacia():
            raise RuntimeError(
                "No existen operaciones para deshacer."
            )

        operacion = self.pila_operaciones.ver_tope()

        if not isinstance(operacion, Operacion):
            raise RuntimeError(
                "La pila contiene una operación inválida."
            )

        if operacion.tipo == TipoOperacion.REGISTRAR:
            self._deshacer_registro(operacion)

        elif operacion.tipo == TipoOperacion.CANCELAR:
            self._deshacer_cancelacion(operacion)

        elif operacion.tipo == TipoOperacion.RECLASIFICAR:
            self._deshacer_reclasificacion(operacion)

        elif operacion.tipo == TipoOperacion.ATENDER:
            self._deshacer_atencion(operacion)

        elif operacion.tipo == TipoOperacion.FINALIZAR:
            self._deshacer_finalizacion(operacion)

        else:
            raise RuntimeError(
                "El tipo de operación no puede deshacerse."
            )

        self.pila_operaciones.desapilar()

        return operacion
    
    def _deshacer_registro(
        self,
        operacion: Operacion
    ) -> None:
        """
        Elimina del sistema una llamada cuyo registro
        está siendo deshecho.
        """

        llamada = self.obtener_llamada_registrada(
            operacion.id_llamada
        )

        if llamada is None:
            raise RuntimeError(
                "La llamada registrada no existe."
            )

        if llamada.estado != EstadoLlamada.EN_ESPERA:
            raise RuntimeError(
                "El registro no puede deshacerse "
                "en el estado actual."
            )

        if llamada.prioridad is None:
            raise RuntimeError(
                "La llamada no tiene prioridad."
            )

        cola = self._obtener_cola(
            llamada.prioridad
        )

        eliminada = self._eliminar_de_cola(
            cola,
            llamada.id_llamada
        )

        if eliminada is None:
            raise RuntimeError(
                "No fue posible retirar la llamada."
            )

        del self._registro_llamadas[
            llamada.id_llamada
        ]
    
    def _deshacer_cancelacion(
        self,
        operacion: Operacion
    ) -> None:
        """
        Restaura una llamada cancelada en su posición
        y estado originales.
        """

        llamada = self.obtener_llamada_registrada(
            operacion.id_llamada
        )

        if llamada is None:
            raise RuntimeError(
                "La llamada cancelada no existe."
            )

        if operacion.prioridad_anterior is None:
            raise RuntimeError(
                "No existe prioridad anterior registrada."
            )

        if operacion.estado_anterior is None:
            raise RuntimeError(
                "No existe estado anterior registrado."
            )

        if operacion.posicion_anterior is None:
            raise RuntimeError(
                "No existe posición anterior registrada."
            )

        llamada.prioridad = (
            operacion.prioridad_anterior
        )

        llamada.estado = (
            operacion.estado_anterior
        )

        cola = self._obtener_cola(
            operacion.prioridad_anterior
        )

        cola.insertar_en_posicion(
            llamada,
            operacion.posicion_anterior
        )
    
    def _deshacer_reclasificacion(
        self,
        operacion: Operacion
    ) -> None:
        """
        Devuelve una llamada reclasificada a su prioridad
        y posición anteriores.
        """

        llamada = self.obtener_llamada_registrada(
            operacion.id_llamada
        )

        if llamada is None:
            raise RuntimeError(
                "La llamada reclasificada no existe."
            )

        if operacion.prioridad_anterior is None:
            raise RuntimeError(
                "No existe prioridad anterior."
            )

        if operacion.prioridad_nueva is None:
            raise RuntimeError(
                "No existe prioridad nueva."
            )

        if operacion.posicion_anterior is None:
            raise RuntimeError(
                "No existe posición anterior."
            )

        cola_actual = self._obtener_cola(
            operacion.prioridad_nueva
        )

        eliminada = self._eliminar_de_cola(
            cola_actual,
            operacion.id_llamada
        )

        if eliminada is None:
            raise RuntimeError(
                "No fue posible retirar la llamada "
                "de su prioridad actual."
            )

        llamada.prioridad = (
            operacion.prioridad_anterior
        )

        if operacion.estado_anterior is not None:
            llamada.estado = operacion.estado_anterior

        cola_anterior = self._obtener_cola(
            operacion.prioridad_anterior
        )

        cola_anterior.insertar_en_posicion(
            llamada,
            operacion.posicion_anterior
        )
    
    def _deshacer_atencion(
        self,
        operacion: Operacion
    ) -> None:
        """
        Devuelve la llamada en atención a su cola original.
        """

        llamada = self.llamada_en_atencion

        if (
            llamada is None
            or llamada.id_llamada
            != operacion.id_llamada
        ):
            raise RuntimeError(
                "La llamada indicada no está en atención."
            )

        if operacion.prioridad_anterior is None:
            raise RuntimeError(
                "No existe prioridad anterior."
            )

        if operacion.estado_anterior is None:
            raise RuntimeError(
                "No existe estado anterior."
            )

        posicion = (
            operacion.posicion_anterior
            if operacion.posicion_anterior is not None
            else 0
        )

        llamada.estado = (
            operacion.estado_anterior
        )

        llamada.prioridad = (
            operacion.prioridad_anterior
        )

        cola = self._obtener_cola(
            operacion.prioridad_anterior
        )

        cola.insertar_en_posicion(
            llamada,
            posicion
        )

        self.llamada_en_atencion = None
    
    def _deshacer_finalizacion(
        self,
        operacion: Operacion
    ) -> None:
        """
        Devuelve una llamada finalizada al estado
        EN_ATENCION.
        """

        if self.llamada_en_atencion is not None:
            raise RuntimeError(
                "Ya existe una llamada en atención."
            )

        llamada = self.obtener_llamada_registrada(
            operacion.id_llamada
        )

        if llamada is None:
            raise RuntimeError(
                "La llamada finalizada no existe."
            )

        if operacion.estado_anterior is None:
            raise RuntimeError(
                "No existe estado anterior."
            )

        llamada.estado = (
            operacion.estado_anterior
        )

        if operacion.prioridad_anterior is not None:
            llamada.prioridad = (
                operacion.prioridad_anterior
            )

        self.llamada_en_atencion = llamada
    
    
    def _generar_id(self):
        """
        Genera identificadores secuenciales para las llamadas.
        """

        self._contador_llamadas += 1

        return f"L{self._contador_llamadas:03d}"

    def _obtener_cola(self, prioridad):
        """
        Retorna la cola asociada a una prioridad.
        """

        if prioridad == Prioridad.CRITICA:
            return self.cola_p1

        if prioridad == Prioridad.ALTA:
            return self.cola_p2

        if prioridad == Prioridad.NORMAL:
            return self.cola_p3

        raise ValueError(
            "La prioridad indicada no es válida."
        )

    def _obtener_primera_cola_disponible(self):
        """
        Retorna la primera cola no vacía respetando
        el orden de prioridad P1, P2 y P3.
        """

        if not self.cola_p1.esta_vacia():
            return self.cola_p1

        if not self.cola_p2.esta_vacia():
            return self.cola_p2

        if not self.cola_p3.esta_vacia():
            return self.cola_p3

        return None

    def _registrar_operacion_registro(self, llamada):
        """
        Registra en la pila la creación de una llamada.
        """

        operacion = Operacion(
            tipo=TipoOperacion.REGISTRAR,
            id_llamada=llamada.id_llamada,
            estado_anterior=EstadoLlamada.RECIBIDA,
            estado_nuevo=EstadoLlamada.EN_ESPERA,
            prioridad_anterior=None,
            prioridad_nueva=llamada.prioridad,
        )

        self.pila_operaciones.apilar(operacion)
        
    def _buscar_en_cola(
        self,
        cola: Cola,
        id_llamada: str
    ) -> Llamada | None:
        """
        Busca una llamada específica dentro de una cola.
        """

        resultado = cola.buscar(
            lambda dato:
                isinstance(dato, Llamada)
                and dato.id_llamada == id_llamada
        )

        if isinstance(resultado, Llamada):
            return resultado

        return None

    def _eliminar_de_cola(
        self,
        cola: Cola,
        id_llamada: str
    ) -> Llamada | None:
        """
        Elimina una llamada específica de una cola.
        """

        resultado = cola.eliminar(
            lambda dato:
                isinstance(dato, Llamada)
                and dato.id_llamada == id_llamada
        )

        if isinstance(resultado, Llamada):
            return resultado

        return None
    
    def obtener_llamada_registrada(
        self,
        id_llamada: str
    ) -> Llamada | None:
        
        """
        Retorna una llamada que haya sido registrada
        previamente, sin importar su estado actual.
        """
        
        return self._registro_llamadas.get(id_llamada)
    
    def obtener_llamadas_registradas(self) -> list[Llamada]:
        """
        Retorna todas las llamadas registradas durante
        la ejecución actual del sistema.

        Se conserva el orden en el que fueron registradas.
        """
        return list(
            self._registro_llamadas.values()
        )
    def obtener_llamadas_en_espera(
        self
    ) -> list[Llamada]:
        """
        Retorna todas las llamadas que actualmente
        se encuentran esperando en alguna cola.
        """
        return [
            llamada
            for llamada in self._registro_llamadas.values()
            if llamada.estado == EstadoLlamada.EN_ESPERA
        ]
    
    def obtener_operaciones_deshacibles(
        self
    ) -> list[Operacion]:
        """
        Retorna las operaciones almacenadas actualmente
        en la pila LIFO, desde la más reciente hasta
        la más antigua.
        """

        elementos = (
            self.pila_operaciones
            .obtener_elementos()
        )

        return [
            elemento
            for elemento in elementos
            if isinstance(elemento, Operacion)
        ]
    