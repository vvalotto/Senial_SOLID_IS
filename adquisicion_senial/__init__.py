"""
Paquete adquisicion_senial - Aplicación de OCP para adquisición de datos

Este paquete contiene las clases responsables de capturar datos desde diferentes
fuentes para formar señales digitales, implementando el patrón Strategy.

Aplicación de principios SOLID:
- SRP: Responsabilidad única de gestionar adquisición de datos
- OCP: Extensible para nuevos tipos de fuentes sin modificar código existente
- LSP: Todas las implementaciones son intercambiables polimórficamente

Arquitectura basada en patrón Strategy con abstracciones:
- BaseAdquisidor: Clase abstracta que define el contrato común
- AdquisidorConsola: Implementación para entrada desde teclado
- AdquisidorArchivo: Implementación para entrada desde archivos

Versión: 2.1.0 (DIP aplicado - Dependency Inversion Principle)
Autor: Victor Valotto
"""

from .adquisidor import BaseAdquisidor, AdquisidorConsola, AdquisidorArchivo

__version__ = "2.1.0"
__author__ = "Victor Valotto"
__all__ = [
    'BaseAdquisidor',
    'AdquisidorConsola',
    'AdquisidorArchivo'
]