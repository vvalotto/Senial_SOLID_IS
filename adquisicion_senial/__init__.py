"""
Paquete adquisicion_senial - Factory Pattern + Configuración Externa

Este paquete contiene las clases responsables de capturar datos desde diferentes
fuentes para formar señales digitales, implementando el patrón Strategy + Factory.

Aplicación de principios SOLID:
- SRP: Responsabilidad única de gestionar adquisición de datos
- OCP: Extensible para nuevos tipos de fuentes sin modificar código existente
- LSP: Todas las implementaciones son intercambiables polimórficamente
- DIP: Inyección de dependencias (señal) + Configuración externa (JSON)

Arquitectura basada en patrón Strategy + Factory:
- BaseAdquisidor: Clase abstracta que define el contrato común
- AdquisidorConsola: Implementación para entrada desde teclado
- AdquisidorArchivo: Implementación para entrada desde archivos
- AdquisidorSenoidal: Generador de señal sintética
- FactoryAdquisidor: Factory especializado con inyección de dependencias

Versión: 3.0.0 (Factory + Configuración Externa JSON)
Autor: Victor Valotto
"""

from .adquisidor import (
    BaseAdquisidor,
    AdquisidorConsola,
    AdquisidorArchivo,
    AdquisidorSenoidal
)
from .factory_adquisidor import FactoryAdquisidor

__version__ = "3.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'BaseAdquisidor',
    'AdquisidorConsola',
    'AdquisidorArchivo',
    'AdquisidorSenoidal',
    'FactoryAdquisidor'
]