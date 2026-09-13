from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Prioridad(Enum):
    """
    Niveles de prioridad disponibles para una llamada.
    """

    CRITICA = "P1"
    ALTA = "P2"
    NORMAL = "P3"


class EstadoLlamada(Enum):
    """
    Estados posibles durante el ciclo de vida de una llamada.
    """

    RECIBIDA = "RECIBIDA"
    EN_ESPERA = "EN_ESPERA"
    EN_ATENCION = "EN_ATENCION"
    ATENDIDA = "ATENDIDA"
    CANCELADA = "CANCELADA"


@dataclass
class Llamada:
    """
    Representa una llamada recibida por SmartCall 123.

    Contiene la información necesaria para clasificar,
    gestionar y atender la llamada.
    """

    id_llamada: str
    hora_llegada: datetime
    tipo: str
    ubicacion: str
    descripcion: str
    personas_afectadas: int

    consciente: bool
    respira: bool
    heridos: bool
    peligro_inmediato: bool
    riesgo_potencial: bool

    prioridad: Optional[Prioridad] = None
    estado: EstadoLlamada = EstadoLlamada.RECIBIDA

    def __post_init__(self):
        self._validar_id()
        self._validar_personas_afectadas()

    def _validar_id(self):
        """
        Verifica que la llamada tenga un identificador.
        """
        if not self.id_llamada.strip():
            raise ValueError(
                "El identificador de la llamada no puede estar vacío."
            )

    def _validar_personas_afectadas(self):
        """
        Verifica que la cantidad de personas afectadas
        no sea negativa.
        """
        if self.personas_afectadas < 0:
            raise ValueError(
                "La cantidad de personas afectadas no puede ser negativa."
            )