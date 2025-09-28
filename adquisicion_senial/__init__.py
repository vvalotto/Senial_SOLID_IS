"""
Paquete adquisicion_senial - Captura de datos de entrada

Este paquete contiene todas las clases responsables de capturar y obtener datos
desde diferentes fuentes para formar señales digitales.

Aplicación del SRP a nivel de paquete: Este paquete tiene la responsabilidad única
de gestionar la captura y adquisición de datos de entrada al sistema.

Versión: 1.0.0
Autor:Victor Valotto
"""

from .adquisidor import Adquisidor

__version__ = "1.0.0"
__author__ = "Victor Valotto"
__all__ = ['Adquisidor']