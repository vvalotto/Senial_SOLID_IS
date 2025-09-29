"""
Paquete dominio_senial - Entidades del dominio

Este paquete contiene las entidades fundamentales del dominio de procesamiento
de señales digitales. Es completamente independiente de infraestructura externa.

Aplicación del SRP a nivel de paquete: Este paquete tiene la responsabilidad única
de definir y gestionar las entidades del dominio de señales digitales.

Versión: 1.0.0
Autor: Victor Valotto
"""

from .senial import Senial, SenialPila, SenialCola

__version__ = "1.0.0"
__author__ = "Victor Valotto"
__all__ = ['Senial','SenialPila','SenialCola']