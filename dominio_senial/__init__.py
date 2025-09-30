"""
Paquete dominio_senial - Entidades del dominio

Este paquete contiene las entidades fundamentales del dominio de procesamiento
de señales digitales. Es completamente independiente de infraestructura externa.

✅ VERSIÓN 4.0 - LSP COMPLETO + ELIMINACIÓN ALIAS SENIAL

Aplicación del SRP a nivel de paquete: Este paquete tiene la responsabilidad única
de definir y gestionar las entidades del dominio de señales digitales.

🎯 PRINCIPIOS SOLID:
- ✅ LSP: Jerarquía con intercambiabilidad polimórfica garantizada
- ✅ OCP: Extensible sin modificación (sin isinstance checks)
- ✅ SRP: Cada clase una responsabilidad específica

🏗️ ARQUITECTURA:
- SenialBase: Abstracción base con contrato común
- SenialLista: Comportamiento de lista dinámica
- SenialPila: Comportamiento LIFO (Last In, First Out)
- SenialCola: Comportamiento FIFO (First In, First Out)

⚠️ BREAKING CHANGES v4.0.0:
- Eliminado alias "Senial" (usar SenialLista, SenialPila o SenialCola explícitamente)
- Toda la jerarquía refactorizada con LSP aplicado correctamente

Versión: 4.0.0 - LSP Completo + Arquitectura Limpia
Autor: Victor Valotto
"""

from .senial import (
    SenialBase,
    SenialLista,
    SenialPila,
    SenialCola
)

__version__ = "4.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'SenialBase',
    'SenialLista',
    'SenialPila',
    'SenialCola'
]