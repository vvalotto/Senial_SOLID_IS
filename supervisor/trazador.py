"""
Módulo de trazabilidad - Interface Segregation Principle (ISP)

Proporciona la abstracción BaseTrazador para separar la responsabilidad
de trazabilidad de otras responsabilidades de supervisión.
"""
from abc import ABCMeta, abstractmethod
from typing import Any


class BaseTrazador(metaclass=ABCMeta):
    """
    Abstracción para trazadores.

    Define la interfaz específica para trazabilidad, aplicando ISP al segregar
    esta responsabilidad de la auditoría (BaseAuditor).
    """

    @abstractmethod
    def trazar(self, entidad: Any, accion: str, mensaje: str) -> None:
        """
        Registra una traza de acción sobre una entidad.

        :param entidad: Entidad sobre la cual se registra la traza
        :param accion: Tipo de acción realizada (ej: "PROCESAMIENTO", "ADQUISICION")
        :param mensaje: Mensaje descriptivo de la traza
        """
        pass
