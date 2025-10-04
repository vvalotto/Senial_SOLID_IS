"""
Paquete de persistencia de señales digitales + Factory Pattern

Proporciona funcionalidad para guardar y recuperar señales en diferentes formatos.

🎯 OBJETIVO DIDÁCTICO:
Este paquete demuestra la aplicación correcta del principio ISP (Interface Segregation Principle)
mediante interfaces segregadas y herencia múltiple + Factory Pattern para creación configurable.

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
- DIP: Repositorio depende de abstracción BaseContexto (inyección) + Configuración externa

Clases principales - Patrón Repository + Factory:
- BaseRepositorio: Abstracción de dominio básica (guardar, obtener)
- RepositorioSenial: Repositorio con auditoría/trazabilidad (herencia múltiple)
- RepositorioUsuario: Repositorio simple (solo persistencia)
- BaseContexto: Abstracción de infraestructura (Strategy Pattern)
- ContextoPickle: Persistencia binaria con pickle
- ContextoArchivo: Persistencia en texto plano
- FactoryContexto: Factory especializado para creación según config externa
- MapeadorArchivo: Serialización/deserialización para archivos de texto

✨ NUEVO v7.0.0:
- Factory Pattern para creación de contextos
- Preparado para configuración JSON externa

Versión: 7.0.0 - ISP + Factory Pattern + Configuración Externa
Autor: Victor Valotto
"""

__author__ = 'Victor Valotto'
__version__ = '7.0.0'

from persistidor_senial.contexto import BaseContexto, ContextoPickle, ContextoArchivo
from persistidor_senial.repositorio import BaseRepositorio, RepositorioSenial, RepositorioUsuario
from persistidor_senial.mapeador import Mapeador, MapeadorArchivo
from persistidor_senial.factory_contexto import FactoryContexto

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
    # Factory
    'FactoryContexto',
    # Mapeadores
    'Mapeador',
    'MapeadorArchivo',
    # Alias de compatibilidad (deprecados)
    'BasePersistidor',
    'PersistidorPickle',
    'PersistidorArchivo',
]