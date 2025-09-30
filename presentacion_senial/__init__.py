"""
Paquete presentacion_senial - Visualización de datos

Este paquete contiene todas las clases responsables de presentar y visualizar
señales digitales en diferentes formatos de salida.

Aplicación del SRP a nivel de paquete: Este paquete tiene la responsabilidad única
de gestionar la presentación y visualización de datos de señales.

Versión: 2.0.0 (Compatible con SenialBase - LSP aplicado)

⚠️ BREAKING CHANGES v2.0.0:
- Visualizador ahora trabaja con SenialBase en lugar de clase Senial concreta
- Compatible polimórficamente con SenialLista, SenialPila, SenialCola
Autor: Victor Valotto
"""

from .visualizador import Visualizador

__version__ = "2.0.0"
__author__ = "Victor Valotto"
__all__ = ['Visualizador']