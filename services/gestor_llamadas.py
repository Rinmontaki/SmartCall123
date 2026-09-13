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

    def __init__(self):
        self.cola_p1 = Cola()
        self.cola_p2 = Cola()
        self.cola_p3 = Cola()

        self.pila_operaciones = Pila()

        self.llamada_en_atencion = None

        self._contador_llamadas = 0

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