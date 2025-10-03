"""
Patrón repositorio: responsable de manejar de manera abstracta la persitencia
de las entidades

⚠️ VIOLACIÓN ISP INTENCIONAL - PROPÓSITO DIDÁCTICO ⚠️

Este módulo contiene una violación deliberada del Interface Segregation Principle
para demostrar las consecuencias de interfaces "gordas" que obligan a los clientes
a implementar métodos innecesarios.

📚 VIOLACIÓN DEMOSTRADA:
BaseRepositorio define 4 métodos abstractos obligatorios:
- guardar() ✅ Todos los repositorios lo necesitan
- obtener() ✅ Todos los repositorios lo necesitan
- auditar() ⚠️ Solo RepositorioSenial lo necesita
- trazar() ⚠️ Solo RepositorioSenial lo necesita

❌ CONSECUENCIAS:
RepositorioUsuario está FORZADO a implementar auditar() y trazar()
aunque NO los necesita, resultando en implementaciones stub que lanzan excepciones.

🎯 LECCIÓN: Segregar interfaces según necesidades reales de los clientes.
"""
from abc import ABC, abstractmethod
from typing import Any
import datetime


class BaseRepositorio(ABC):
    """
    ⚠️ INTERFAZ "GORDA" - Violación ISP Intencional

    Define la interfaz para el acceso a la persistencia de datos
    CON MÉTODOS QUE NO TODOS LOS CLIENTES NECESITAN.

    Problema: Obliga a TODAS las implementaciones a definir:
    - Persistencia (guardar/obtener) ✅ Necesario para todos
    - Auditoría (auditar/trazar) ❌ Solo necesario para algunos

    Solución ISP: Segregar en IRepositorioBasico + IRepositorioAuditable
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

    @abstractmethod
    def auditar(self, entidad, auditoria):
        """
        ⚠️ MÉTODO PROBLEMÁTICO - No todos los repositorios necesitan auditoría

        Realiza el registro de auditoría sobre la entidad indicada
        :param entidad: Entidad a auditar
        :param auditoria: Información de auditoría
        """
        pass

    @abstractmethod
    def trazar(self, entidad, accion, mensaje):
        """
        ⚠️ MÉTODO PROBLEMÁTICO - No todos los repositorios necesitan trazabilidad

        Realiza la traza del evento ocurrido sobre la entidad y con el mensaje de
        traza correspondiente
        :param entidad: Entidad a trazar
        :param accion: Acción realizada
        :param mensaje: Mensaje de traza
        """
        pass


class RepositorioSenial(BaseRepositorio):
    """
    ✅ Repositorio que SÍ NECESITA todos los métodos de BaseRepositorio

    Las señales son datos críticos que requieren:
    - Persistencia (guardar/obtener)
    - Auditoría completa (auditar/trazar)

    Este repositorio NO sufre la violación ISP porque USA todos los métodos.
    """
    def __init__(self, contexto: Any):
        """
        Inicializa el repositorio con un contexto de persistencia
        :param contexto: Contexto de persistencia
        """
        super().__init__(contexto)

    def guardar(self, senial: Any) -> None:
        """
        Persiste la señal
        :param senial: Señal a persistir
        """
        try:
            # Convertir ID a string para compatibilidad
            self._contexto.persistir(senial, str(senial.id))
        except Exception as e:
            print(f"Error al guardar la señal: {e}")
            raise

    def obtener(self, id_senial: str, entidad: Any = None) -> Any:
        """
        Obtiene una señal por su identificador

        RECONSTRUCCIÓN AUTOMÁTICA: Si el contexto es ContextoArchivo con metadatos,
        no requiere 'entidad'. Si es necesario, se puede proporcionar.

        :param id_senial: Identificador de la señal
        :param entidad: Instancia template para deserialización (opcional)
        :return: Señal recuperada
        """
        try:
            return self._contexto.recuperar(id_senial, entidad)
        except Exception as e:
            print(f"Error al obtener la señal: {e}")
            raise

    def auditar(self, senial, auditoria):
        """
        ✅ IMPLEMENTACIÓN REAL - Este método SÍ se usa

        Realiza el registro de auditoría sobre la señal indicada
        :param senial: Señal a auditar
        :param auditoria: Información de auditoría
        """
        nombre = 'auditor.log'
        try:
            with open(nombre, 'a') as auditor:
                auditor.write('------->\n')
                auditor.write(f'Señal ID: {senial.id}\n')
                auditor.write(f'Fecha: {datetime.datetime.now()}\n')
                auditor.write(f'Auditoría: {auditoria}\n')
                auditor.write('\n')
        except IOError as eIO:
            print(f"Error al auditar la señal: {eIO}")
            raise

    def trazar(self, senial, accion, mensaje):
        """
        ✅ IMPLEMENTACIÓN REAL - Este método SÍ se usa

        Realiza la traza del evento ocurrido sobre la señal y con el mensaje de
        traza correspondiente
        :param senial: Señal a trazar
        :param accion: Acción realizada
        :param mensaje: Mensaje de traza
        """
        nombre = 'logger.log'
        try:
            with open(nombre, 'a') as logger:
                logger.write('------->\n')
                logger.write(f'Acción: {accion}\n')
                logger.write(f'Señal ID: {senial.id}\n')
                logger.write(f'Fecha: {datetime.datetime.now()}\n')
                logger.write(f'Mensaje: {mensaje}\n')
                logger.write('\n')
        except IOError as eIO:
            print(f"Error al trazar la señal: {eIO}")
            raise


class RepositorioUsuario(BaseRepositorio):
    """
    ❌ Repositorio que SUFRE la violación ISP

    Los usuarios solo necesitan:
    - Persistencia (guardar/obtener) ✅ Se usan
    - Auditoría (auditar/trazar) ❌ NO se necesitan

    Problema: BaseRepositorio OBLIGA a implementar auditar() y trazar()
    aunque este repositorio NO los necesita.

    Consecuencia: Implementaciones falsas (stub) que lanzan excepciones.
    """
    def __init__(self, contexto: Any):
        """
        Inicializa el repositorio con un contexto de persistencia
        :param contexto: Contexto de persistencia
        """
        super().__init__(contexto)

    def guardar(self, usuario: Any) -> None:
        """
        ✅ IMPLEMENTACIÓN REAL - Este método SÍ se usa

        Persiste el usuario
        :param usuario: Usuario a persistir
        """
        try:
            self._contexto.persistir(usuario, str(usuario.id))
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")
            raise

    def obtener(self, id_usuario: str, entidad: Any = None) -> Any:
        """
        ✅ IMPLEMENTACIÓN REAL - Este método SÍ se usa

        Obtiene un usuario por su identificador

        RECONSTRUCCIÓN AUTOMÁTICA: Si el contexto es ContextoArchivo con metadatos,
        no requiere 'entidad'. Si es necesario, se puede proporcionar.

        :param id_usuario: Identificador del usuario
        :param entidad: Instancia template para deserialización (opcional)
        :return: Usuario recuperado
        """
        try:
            return self._contexto.recuperar(id_usuario, entidad)
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            raise

    def auditar(self, entidad, auditoria):
        """
        ❌ IMPLEMENTACIÓN STUB - Violación ISP

        FORZADO a implementar por BaseRepositorio pero NO se necesita.

        Este método existe SOLO porque la interfaz abstracta lo obliga.
        Si un cliente intenta usarlo, FALLA en runtime.

        🎯 LECCIÓN ISP: "Los clientes no deberían depender de interfaces que no usan"
        """
        raise NotImplementedError("RepositorioUsuario no soporta auditoría - Violación ISP")

    def trazar(self, entidad, accion, mensaje):
        """
        ❌ IMPLEMENTACIÓN STUB - Violación ISP

        FORZADO a implementar por BaseRepositorio pero NO se necesita.

        Este método existe SOLO porque la interfaz abstracta lo obliga.
        Si un cliente intenta usarlo, FALLA en runtime.

        🎯 LECCIÓN ISP: "Los clientes no deberían depender de interfaces que no usan"
        """
        raise NotImplementedError("RepositorioUsuario no soporta trazabilidad - Violación ISP")
