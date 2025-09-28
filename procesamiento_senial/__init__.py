"""
Paquete procesamiento_senial - Algoritmos de procesamiento

Este paquete contiene todas las clases responsables de aplicar algoritmos
y transformaciones sobre señales digitales.

Aplicación de principios SOLID:
- SRP: Responsabilidad única de gestionar procesamiento de señales
- OCP: Extensible para nuevos tipos de procesamiento sin modificar código existente

Arquitectura basada en patrón Strategy con abstracciones:
- BaseProcesador: Clase abstracta que define el contrato común
- ProcesadorAmplificador: Implementación para amplificación de señales
- ProcesadorConUmbral: Implementación para filtrado por umbral

Versión: 2.0.0 (actualizada para OCP)
Autor: Victor Valotto
"""

from .procesador import BaseProcesador, ProcesadorAmplificador, ProcesadorConUmbral

__version__ = "2.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'BaseProcesador',
    'ProcesadorAmplificador',
    'ProcesadorConUmbral'
]