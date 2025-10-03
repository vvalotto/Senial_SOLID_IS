"""
Módulo de auditoría - Interface Segregation Principle (ISP)

Proporciona la abstracción BaseAuditor para separar la responsabilidad
de auditoría de otras responsabilidades de supervisión.
"""
from abc import ABCMeta, abstractmethod
from typing import Any


class BaseAuditor(metaclass=ABCMeta):
    """
    Abstracción para auditores.

    Define la interfaz específica para auditoría, aplicando ISP al segregar
    esta responsabilidad de la trazabilidad (BaseTrazador).
    """

    @abstractmethod
    def auditar(self, entidad: Any, auditoria: str) -> None:
        """
        Registra un evento de auditoría sobre una entidad.

        :param entidad: Entidad sobre la cual se registra la auditoría
        :param auditoria: Descripción del evento de auditoría
        """
        pass
