"""
Paquete de persistencia de señales digitales

Proporciona funcionalidad para guardar y recuperar señales en diferentes formatos.

🎯 OBJETIVO DIDÁCTICO:
Este paquete demuestra la aplicación correcta del principio ISP (Interface Segregation Principle)
mediante interfaces segregadas y herencia múltiple.

✅ ISP CORRECTAMENTE APLICADO (v6.0.0):
- BaseRepositorio: Solo métodos básicos (guardar, obtener)
- BaseAuditor (supervisor): Interfaz segregada para auditoría
- BaseTrazador (supervisor): Interfaz segregada para trazabilidad
- RepositorioSenial: Herencia múltiple (BaseAuditor + BaseTrazador + BaseRepositorio)
- RepositorioUsuario: Solo BaseRepositorio (sin métodos innecesarios)

✅ PRINCIPIOS SOLID APLICADOS:
- SRP: Cada clase tiene una responsabilidad única
- OCP: Extensible sin modificación (nuevos contextos)
- LSP: Contextos intercambiables
- ISP: Interfaces segregadas según necesidades reales
- DIP: Repositorio depende de abstracción BaseContexto (inyección)

Clases principales - Patrón Repository:
- BaseRepositorio: Abstracción de dominio básica (guardar, obtener)
- RepositorioSenial: Repositorio con auditoría/trazabilidad (herencia múltiple)
- RepositorioUsuario: Repositorio simple (solo persistencia)
- BaseContexto: Abstracción de infraestructura (Strategy Pattern)
- ContextoPickle: Persistencia binaria con pickle
- ContextoArchivo: Persistencia en texto plano
- MapeadorArchivo: Serialización/deserialización para archivos de texto

Versión: 6.0.0 - ISP corregido con interfaces segregadas (supervisor package)
Autor: Victor Valotto
"""

__author__ = 'Victor Valotto'
__version__ = '6.0.0'

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