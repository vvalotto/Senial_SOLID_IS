"""
Paquete procesamiento_senial - Factory Pattern + Configuración Externa

Este paquete contiene todas las clases responsables de aplicar algoritmos
y transformaciones sobre señales digitales, implementando el patrón Strategy + Factory.

Aplicación de principios SOLID:
- SRP: Responsabilidad única de gestionar procesamiento de señales
- OCP: Extensible para nuevos tipos de procesamiento sin modificar código existente
- LSP: Todas las implementaciones son intercambiables polimórficamente
- DIP: Inyección de dependencias (señal) + Configuración externa (JSON)

Arquitectura basada en patrón Strategy + Factory:
- BaseProcesador: Clase abstracta que define el contrato común
- ProcesadorAmplificador: Implementación para amplificación de señales
- ProcesadorConUmbral: Implementación para filtrado por umbral
- FactoryProcesador: Factory especializado con inyección de dependencias

Versión: 3.0.0 (Factory + Configuración Externa JSON)
Autor: Victor Valotto
"""

from .procesador import (
    BaseProcesador,
    ProcesadorAmplificador,
    ProcesadorConUmbral
)
from .factory_procesador import FactoryProcesador

__version__ = "3.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'BaseProcesador',
    'ProcesadorAmplificador',
    'ProcesadorConUmbral',
    'FactoryProcesador'
]