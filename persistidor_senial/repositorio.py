"""
Patrón repositorio: responsable de manejar de manera abstracta la persitencia
de las entidades

⚠️ VERSIÓN CORREGIDA - ISP APLICADO ⚠️

Este módulo contiene la CORRECCIÓN de la violación ISP mediante interfaces segregadas.

📚 SOLUCIÓN ISP APLICADA:
BaseRepositorio ahora solo define métodos básicos:
- guardar() ✅ Todos los repositorios lo necesitan
- obtener() ✅ Todos los repositorios lo necesitan

Auditoría y trazabilidad segregadas en:
- BaseAuditor (supervisor.auditor) ✅ Solo para repositorios que lo necesitan
- BaseTrazador (supervisor.trazador) ✅ Solo para repositorios que lo necesitan

✅ RESULTADO:
- RepositorioSenial: Implementa BaseRepositorio + BaseAuditor + BaseTrazador
- RepositorioUsuario: Solo implementa BaseRepositorio (sin métodos innecesarios)

🎯 LECCIÓN: Interfaces segregadas según necesidades reales de los clientes.
"""
from abc import ABC, abstractmethod
from supervisor import BaseAuditor, BaseTrazador
from typing import Any
import datetime


class BaseRepositorio(ABC):
    """
    ✅ Interfaz básica - Solo persistencia

    Define la interfaz para el acceso a la persistencia de datos
    SIN métodos de auditoría ni trazabilidad (ISP aplicado).
    """

    def __init__(self, contexto: Any):
        """
        Inicializa el repositorio con un contexto de persistencia
        :param contexto: Contexto de persistencia
        """
        self._contexto = contexto

    @abstractmethod
    def guardar(self, entidad: Any) -> None:
        """
        Persiste la entidad
        :param entidad: Entidad a persistir
        """
        pass

    @abstractmethod
    def obtener(self, id_entidad: str, entidad: Any = None) -> Any:
        """
        Obtiene una entidad por su identificador
        :param id_entidad: Identificador de la entidad
        :param entidad: Instancia template para deserialización (opcional)
        :return: Entidad recuperada
        """
        pass


class RepositorioSenial(BaseAuditor, BaseTrazador, BaseRepositorio):
    """
    ✅ Repositorio que NECESITA auditoría y trazabilidad

    Implementa las 3 interfaces porque las señales son datos críticos
    que requieren supervisión completa:
    - BaseRepositorio: Persistencia básica
    - BaseAuditor: Auditoría de operaciones
    - BaseTrazador: Trazabilidad de eventos

    Este repositorio NO sufre violación ISP porque USA todos los métodos.
    """

    def __init__(self, contexto: Any):
        """
        Inicializa el repositorio de señales
        :param contexto: Contexto de persistencia
        """
        super().__init__(contexto)

    def guardar(self, senial: Any) -> None:
        """
        Persiste la señal con auditoría y trazabilidad
        :param senial: Señal a persistir
        """
        try:
            self.auditar(senial, "Antes de hacer la persistencia")
            self._contexto.persistir(senial, str(senial.id))
            self.auditar(senial, "Se realizó la persistencia")
        except Exception as ex:
            self.auditar(senial, "Problema al persistir")
            self.trazar(senial, "guardar", str(ex))
            raise

    def obtener(self, id_senial: str, entidad: Any = None) -> Any:
        """
        Obtiene una señal por su identificador con auditoría

        :param id_senial: Identificador de la señal
        :param entidad: Instancia template para deserialización (opcional)
        :return: Señal recuperada
        """
        try:
            # Auditar antes de recuperar (usamos dict vacío si no hay entidad)
            self.auditar(entidad if entidad else {'id': id_senial}, "Antes de recuperar la señal")

            senial_recuperada = self._contexto.recuperar(id_senial, entidad)

            self.auditar(senial_recuperada, "Se realizó la recuperación")
            return senial_recuperada
        except Exception as ex:
            msj = f'Error al leer señal persistida - ID: {id_senial}'
            self.trazar(entidad if entidad else {'id': id_senial}, "obtener", msj)
            raise

    def auditar(self, senial: Any, auditoria: str) -> None:
        """
        ✅ IMPLEMENTACIÓN REAL - Auditoría de señales

        Registra eventos de auditoría en archivo de log
        :param senial: Señal a auditar
        :param auditoria: Descripción del evento
        """
        nombre = 'auditor_senial.log'
        try:
            with open(nombre, 'a', encoding='utf-8') as auditor:
                auditor.write('------->\n')
                auditor.write(f'{senial}\n')
                auditor.write(f'{datetime.datetime.now()}\n')
                auditor.write(f'{auditoria}\n')
                auditor.write('\n')
        except IOError as eIO:
            print(f"Error al auditar: {eIO}")
            raise

    def trazar(self, senial: Any, accion: str, mensaje: str) -> None:
        """
        ✅ IMPLEMENTACIÓN REAL - Trazabilidad de señales

        Registra trazas de acciones en archivo de log
        :param senial: Señal a trazar
        :param accion: Acción realizada (ej: "guardar", "obtener")
        :param mensaje: Mensaje descriptivo
        """
        nombre = 'logger_senial.log'
        try:
            with open(nombre, 'a', encoding='utf-8') as logger:
                logger.write('------->\n')
                logger.write(f'Acción: {accion}\n')
                logger.write(f'{senial}\n')
                logger.write(f'{datetime.datetime.now()}\n')
                logger.write(f'{mensaje}\n')
                logger.write('\n')
        except IOError as eIO:
            print(f"Error al trazar: {eIO}")
            raise


class RepositorioUsuario(BaseRepositorio):
    """
    ✅ Repositorio simple - SIN auditoría ni trazabilidad

    Solo implementa BaseRepositorio porque los usuarios son entidades
    simples que NO requieren supervisión especial.

    Este repositorio DEMUESTRA la corrección ISP:
    - Solo implementa métodos que REALMENTE necesita
    - NO hay stubs con NotImplementedError
    - NO depende de interfaces innecesarias
    """

    def __init__(self, contexto: Any):
        """
        Inicializa el repositorio de usuarios
        :param contexto: Contexto de persistencia
        """
        super().__init__(contexto)

    def guardar(self, usuario: Any) -> None:
        """
        ✅ IMPLEMENTACIÓN REAL - Persistencia de usuario

        Persiste el usuario sin auditoría
        :param usuario: Usuario a persistir
        """
        try:
            self._contexto.persistir(usuario, str(usuario.id))
        except Exception as ex:
            print(f"Error al guardar usuario: {ex}")
            raise

    def obtener(self, id_usuario: str, entidad: Any = None) -> Any:
        """
        ✅ IMPLEMENTACIÓN REAL - Recuperación de usuario

        Obtiene un usuario sin auditoría
        :param id_usuario: Identificador del usuario
        :param entidad: Instancia template para deserialización (opcional)
        :return: Usuario recuperado
        """
        try:
            return self._contexto.recuperar(id_usuario, entidad)
        except Exception as ex:
            print(f"Error al obtener usuario: {ex}")
            raise
