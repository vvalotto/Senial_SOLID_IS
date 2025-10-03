"""
Paquete lanzador - Orquestador principal del sistema

Este paquete contiene el lanzador principal que orquesta el flujo completo
de procesamiento de señales aplicando los principios SOLID.

🎯 RESPONSABILIDAD ÚNICA (SRP):
Coordinar y orquestar el flujo entre componentes sin conocer detalles de implementación.

✅ PRINCIPIOS SOLID APLICADOS:
- SRP: Orquestación pura, sin lógica de negocio
- OCP: Extensible mediante Configurador
- LSP: Trabaja con abstracciones de señales
- ISP: No depende de interfaces innecesarias
- DIP: Usa componentes inyectados por Configurador

🔄 CORRECCIÓN ISP (v6.0.0):
- Auditoría y trazabilidad internas al repositorio
- Lanzador NO llama auditar() ni trazar() explícitamente
- Cumple SRP: solo orquesta, no supervisa

Versión: 6.0.0
Autor: Victor Valotto
"""

from .lanzador import Lanzador, ejecutar

__version__ = "6.0.0"
__author__ = "Victor Valotto"
__all__ = ['Lanzador', 'ejecutar']