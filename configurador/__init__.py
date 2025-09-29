"""
Paquete configurador - Factory Centralizado

Este paquete contiene la clase responsable de crear y configurar
todas las instancias de objetos que participan en la aplicación.

Aplicación de principios SOLID:
- SRP: Responsabilidad única de gestionar creación de objetos
- Preparación para DIP: Centralización que facilitará configuración externa futura

Arquitectura:
- Configurador: Factory centralizado con configuración programática

Versión: 1.0.0 (configuración programática)
Autor: Victor Valotto
"""

from .configurador import Configurador

__version__ = "2.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'Configurador'
]