"""
Paquete supervisor - Auditoría y Trazabilidad

Proporciona interfaces segregadas para supervisión de entidades,
demostrando la aplicación correcta del Interface Segregation Principle (ISP).

🎯 OBJETIVO DIDÁCTICO:
Segregar interfaces según necesidades reales de los clientes:
- BaseAuditor: Interfaz específica para auditoría
- BaseTrazador: Interfaz específica para trazabilidad

✅ PRINCIPIOS SOLID:
- ISP: Interfaces segregadas por responsabilidad
- SRP: Cada interfaz tiene una responsabilidad única
- DIP: Clientes dependen de abstracciones

Versión: 1.0.0
Autor: Victor Valotto
"""

__author__ = 'Victor Valotto'
__version__ = '1.0.0'

from supervisor.auditor import BaseAuditor
from supervisor.trazador import BaseTrazador

__all__ = [
    'BaseAuditor',
    'BaseTrazador',
]
