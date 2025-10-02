"""
Paquete de persistencia de señales digitales

Proporciona funcionalidad para guardar y recuperar señales en diferentes formatos.

🎯 OBJETIVO DIDÁCTICO:
Este paquete contiene violaciones intencionales del principio ISP (Interface Segregation Principle)
para demostrar problemas de interfaces "gordas" y su posterior corrección.

Clases principales:
- PersistidorPickle: Persistencia binaria con pickle
- PersistidorArchivo: Persistencia en texto plano
- MapeadorArchivo: Serialización/deserialización para archivos de texto
"""

__author__ = 'Victor Valotto'
__version__ = '1.0.0'

from persistidor_senial.persistidor import PersistidorPickle, PersistidorArchivo
from persistidor_senial.mapeador import Mapeador, MapeadorArchivo

__all__ = [
    'PersistidorPickle',
    'PersistidorArchivo',
    'Mapeador',
    'MapeadorArchivo',
]