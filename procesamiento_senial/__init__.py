"""
Paquete procesamiento_senial - Algoritmos de procesamiento

Este paquete contiene todas las clases responsables de aplicar algoritmos
y transformaciones sobre señales digitales.

Aplicación del SRP a nivel de paquete: Este paquete tiene la responsabilidad única
de gestionar el procesamiento y transformación de señales digitales.

Versión: 1.0.0
Autor: Victor Valotto
"""

from .procesador import Procesador, ProcesadorUmbral

__version__ = "1.0.0"
__author__ = "Victor Valotto"
__all__ = ['Procesador', 'ProcesadorUmbral']