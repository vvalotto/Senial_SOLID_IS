"""
Paquete dominio_senial - Entidades del dominio + Factory Pattern

Este paquete contiene las entidades fundamentales del dominio de procesamiento
de señales digitales. Es completamente independiente de infraestructura externa.

✅ VERSIÓN 5.0 - LSP + Factory Pattern + Configuración Externa

Aplicación del SRP a nivel de paquete: Este paquete tiene la responsabilidad única
de definir y gestionar las entidades del dominio de señales digitales.

🎯 PRINCIPIOS SOLID:
- ✅ LSP: Jerarquía con intercambiabilidad polimórfica garantizada
- ✅ OCP: Extensible sin modificación (sin isinstance checks)
- ✅ SRP: Cada clase una responsabilidad específica
- ✅ DIP: Factory permite configuración externa

🏗️ ARQUITECTURA:
- SenialBase: Abstracción base con contrato común
- SenialLista: Comportamiento de lista dinámica
- SenialPila: Comportamiento LIFO (Last In, First Out)
- SenialCola: Comportamiento FIFO (First In, First Out)
- FactorySenial: Factory especializado para creación según config externa

⚠️ BREAKING CHANGES v4.0.0:
- Eliminado alias "Senial" (usar SenialLista, SenialPila o SenialCola explícitamente)
- Toda la jerarquía refactorizada con LSP aplicado correctamente

✨ NUEVO v5.0.0:
- Factory Pattern para creación configurable
- Preparado para configuración JSON externa

Versión: 5.0.0 - LSP + Factory + Configuración Externa
Autor: Victor Valotto
"""

from .senial import (
    SenialBase,
    SenialLista,
    SenialPila,
    SenialCola
)
from .factory_senial import FactorySenial

__version__ = "5.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'SenialBase',
    'SenialLista',
    'SenialPila',
    'SenialCola',
    'FactorySenial'
]