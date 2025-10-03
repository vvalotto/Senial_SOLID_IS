"""
Paquete de persistencia de señales digitales

Proporciona funcionalidad para guardar y recuperar señales en diferentes formatos.

🎯 OBJETIVO DIDÁCTICO:
Este paquete contiene violaciones intencionales del principio ISP (Interface Segregation Principle)
para demostrar problemas de interfaces "gordas" y su posterior corrección.

⚠️ VIOLACIÓN ISP DEMOSTRADA (v5.3.0):
- BaseRepositorio define interfaz "gorda" con 4 métodos abstractos:
  * guardar() + obtener() → Necesarios para TODOS los repositorios ✅
  * auditar() + trazar() → Solo necesarios para RepositorioSenial ❌
- RepositorioUsuario FORZADO a implementar auditar() y trazar()
- Implementaciones stub que lanzan NotImplementedError
- Código frágil que falla en runtime

✅ PRINCIPIOS CORRECTOS:
- SRP: Cada clase tiene una responsabilidad única
- OCP: Extensible sin modificación (nuevos contextos)
- LSP: Contextos intercambiables
- DIP: Repositorio depende de abstracción BaseContexto (inyección)

Clases principales - Patrón Repository:
- BaseRepositorio: Abstracción de dominio (interfaz "gorda" - violación ISP)
- RepositorioSenial: Repositorio con auditoría/trazabilidad
- RepositorioUsuario: Repositorio simple (sufre violación ISP)
- BaseContexto: Abstracción de infraestructura (Strategy Pattern)
- ContextoPickle: Persistencia binaria con pickle
- ContextoArchivo: Persistencia en texto plano
- MapeadorArchivo: Serialización/deserialización para archivos de texto

Versión: 5.3.0 - Violación ISP intencional en BaseRepositorio (auditar/trazar)
Autor: Victor Valotto
"""

__author__ = 'Victor Valotto'
__version__ = '5.3.0'

from persistidor_senial.contexto import BaseContexto, ContextoPickle, ContextoArchivo
from persistidor_senial.repositorio import BaseRepositorio, RepositorioSenial, RepositorioUsuario
from persistidor_senial.mapeador import Mapeador, MapeadorArchivo

# Alias de compatibilidad con código legacy (deprecados)
BasePersistidor = BaseContexto
PersistidorPickle = ContextoPickle
PersistidorArchivo = ContextoArchivo

__all__ = [
    # Nuevas clases - Patrón Repository
    'BaseContexto',
    'ContextoPickle',
    'ContextoArchivo',
    'BaseRepositorio',
    'RepositorioSenial',
    'RepositorioUsuario',
    # Mapeadores
    'Mapeador',
    'MapeadorArchivo',
    # Alias de compatibilidad (deprecados)
    'BasePersistidor',
    'PersistidorPickle',
    'PersistidorArchivo',
]