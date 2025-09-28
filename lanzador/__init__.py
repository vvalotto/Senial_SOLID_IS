"""
Paquete lanzador - Orquestador principal del sistema

Este paquete contiene el lanzador principal que orquesta el flujo completo
de procesamiento de señales aplicando los principios SOLID.

Aplicación de principios SOLID: Este paquete tiene la responsabilidad única
de coordinar y orquestar el flujo entre los diferentes componentes del sistema.

Versión: 5.0.0
Autor: Victor Valotto
"""

from .lanzador import Lanzador, ejecutar

__version__ = "5.0.0"
__author__ = "Victor Valotto"
__all__ = ['Lanzador', 'ejecutar']