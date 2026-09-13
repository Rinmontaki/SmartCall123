from models.llamada import Llamada, Prioridad


class ClasificadorLlamadas:
    """
    Determina el nivel de prioridad de una llamada
    según sus condiciones de riesgo.
    """

    @staticmethod
    def clasificar(llamada: Llamada) -> Prioridad:
        """
        Retorna la prioridad correspondiente a la llamada.

        La evaluación respeta el siguiente orden:

        1. Prioridad crítica (P1).
        2. Prioridad alta (P2).
        3. Prioridad normal (P3).
        """

        if ClasificadorLlamadas._es_critica(llamada):
            return Prioridad.CRITICA

        if ClasificadorLlamadas._es_alta(llamada):
            return Prioridad.ALTA

        return Prioridad.NORMAL

    @staticmethod
    def _es_critica(llamada: Llamada) -> bool:
        """
        Determina si una llamada presenta alguna
        condición considerada crítica.
        """
        return (
            not llamada.respira
            or not llamada.consciente
            or llamada.peligro_inmediato
        )

    @staticmethod
    def _es_alta(llamada: Llamada) -> bool:
        """
        Determina si una llamada presenta alguna
        condición considerada de prioridad alta.
        """
        return (
            llamada.heridos
            or llamada.riesgo_potencial
        )