"""
Paquete configurador - Factory Centralizado con Configuración Externa (DIP Aplicado)

Este paquete contiene las clases responsables de crear y configurar
todas las instancias de objetos desde configuración externa (JSON).

Aplicación de principios SOLID:
- SRP: Responsabilidad única de gestionar creación de objetos
- OCP: Extensible para nuevos tipos sin modificar código cliente
- DIP: Configuración externa (JSON) determina las dependencias del sistema

Arquitectura:
- Configurador: Factory centralizado que usa Factories especializados
- CargadorConfig: Carga y valida configuración desde JSON

🔄 MIGRACIÓN XML → JSON:
Versión 2.0.0: Configuración desde XML (minidom.parse)
Versión 3.0.0: Configuración desde JSON con Factories especializados (ACTUAL)

Versión: 3.0.0 - DIP Completo con Configuración Externa JSON
Autor: Victor Valotto
"""

from .configurador import Configurador
from .cargador_config import CargadorConfig

__version__ = "3.0.0"
__author__ = "Victor Valotto"
__all__ = [
    'Configurador',
    'CargadorConfig'
]