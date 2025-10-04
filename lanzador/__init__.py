"""
Paquete lanzador - Orquestador principal del sistema con DIP Completo

Este paquete contiene el lanzador principal que orquesta el flujo completo
de procesamiento de señales aplicando los principios SOLID con configuración
externa JSON.

🎯 RESPONSABILIDAD ÚNICA (SRP):
Coordinar y orquestar el flujo entre componentes sin conocer detalles de
implementación ni tipos concretos.

✅ PRINCIPIOS SOLID APLICADOS (COMPLETOS):
- SRP: Orquestación pura, sin lógica de negocio
- OCP: Extensible editando JSON, sin modificar código
- LSP: Trabaja con abstracciones de señales
- ISP: No depende de interfaces innecesarias
- DIP: **Configuración externa (JSON) determina TODAS las dependencias**

🎯 DIP COMPLETO (v6.0.0):
- Configuración desde config.json
- Lanzador NO conoce tipos concretos
- Solo conoce abstracciones y métodos del Configurador
- Cambiar comportamiento: editar JSON, no código

Versión: 6.0.0 - DIP Completo con Configuración Externa JSON
Autor: Victor Valotto
"""

from .lanzador import Lanzador, ejecutar

__version__ = "6.0.0"
__author__ = "Victor Valotto"
__all__ = ['Lanzador', 'ejecutar']