"""
Paquete de persistencia de señales digitales

Proporciona funcionalidad para guardar y recuperar señales en diferentes formatos.

🎯 OBJETIVO DIDÁCTICO:
Este paquete contiene violaciones intencionales del principio ISP (Interface Segregation Principle)
para demostrar problemas de interfaces "gordas" y su posterior corrección.

⚠️ VIOLACIÓN ISP DEMOSTRADA:
- BasePersistidor define interfaz "gorda" con persistir() + recuperar()
- Clientes que solo escriben deben conocer recuperar()
- Clientes que solo leen deben conocer persistir()

✅ PRINCIPIOS CORRECTOS:
- SRP: Cada clase tiene una responsabilidad única
- OCP: Extensible sin modificación (nuevos persistidores)
- DIP: Dependencia en abstracción (BasePersistidor)

Clases principales:
- BasePersistidor: Clase abstracta base (interfaz "gorda" - violación ISP)
- PersistidorPickle: Persistencia binaria con pickle
- PersistidorArchivo: Persistencia en texto plano
- MapeadorArchivo: Serialización/deserialización para archivos de texto

Versión: 1.0.0 - Diseño base con violación ISP intencional
Autor: Victor Valotto
"""

__author__ = 'Victor Valotto'
__version__ = '1.0.0'

from persistidor_senial.persistidor import BasePersistidor, PersistidorPickle, PersistidorArchivo
from persistidor_senial.mapeador import Mapeador, MapeadorArchivo

__all__ = [
    'BasePersistidor',
    'PersistidorPickle',
    'PersistidorArchivo',
    'Mapeador',
    'MapeadorArchivo',
]