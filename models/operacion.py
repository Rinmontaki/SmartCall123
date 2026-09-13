from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from models.llamada import EstadoLlamada, Prioridad


class TipoOperacion(Enum):
    """
    Tipos de operaciones que pueden registrarse
    durante la gestión de una llamada.
    """

    REGISTRAR = "REGISTRAR"
    RECLASIFICAR = "RECLASIFICAR"
    CANCELAR = "CANCELAR"
    ATENDER = "ATENDER"
    FINALIZAR = "FINALIZAR"


@dataclass
class Operacion:
    """
    Representa una acción realizada sobre una llamada.

    Las operaciones serán almacenadas en una pila LIFO
    para permitir posteriormente deshacer acciones.
    """

    tipo: TipoOperacion
    id_llamada: str

    fecha_hora: datetime = field(
        default_factory=datetime.now
    )

    estado_anterior: Optional[EstadoLlamada] = None
    estado_nuevo: Optional[EstadoLlamada] = None

    prioridad_anterior: Optional[Prioridad] = None
    prioridad_nueva: Optional[Prioridad] = None

    def __post_init__(self):
        self._validar_id_llamada()

    def _validar_id_llamada(self):
        """
        Verifica que la operación esté asociada
        a una llamada identificable.
        """
        if not self.id_llamada.strip():
            raise ValueError(
                "El identificador de la llamada no puede estar vacío."
            )