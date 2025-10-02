"""
Patrón repositorio: responsable de manejar de manera abstracta la persitencia
de las entidades
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseRepositorio(ABC):
    """
    Define la interfaz para el acceso a la persistencia de datos
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


class RepositorioSenial(BaseRepositorio):
    """
    Repositorio para gestionar la persistencia de señales
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
            # Firma correcta: recuperar(id_entidad, entidad=None)
            return self._contexto.recuperar(id_senial, entidad)
        except Exception as e:
            print(f"Error al obtener la señal: {e}")
            raise

class RepositorioUsuario(BaseRepositorio):
    """
    Repositorio para gestionar la persistencia de usuarios
    """
    def __init__(self, contexto: Any):
        """
        Inicializa el repositorio con un contexto de persistencia
        :param contexto: Contexto de persistencia
        """
        super().__init__(contexto)

    def guardar(self, usuario: Any) -> None:
        """
        Persiste el usuario
        :param usuario: Usuario a persistir
        """
        try:
            # Convertir ID a string para compatibilidad
            self._contexto.persistir(usuario, str(usuario.id))
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")
            raise

    def obtener(self, id_usuario: str, entidad: Any = None) -> Any:
        """
        Obtiene un usuario por su identificador

        RECONSTRUCCIÓN AUTOMÁTICA: Si el contexto es ContextoArchivo con metadatos,
        no requiere 'entidad'. Si es necesario, se puede proporcionar.

        :param id_usuario: Identificador del usuario
        :param entidad: Instancia template para deserialización (opcional)
        :return: Usuario recuperado
        """
        try:
            # Firma correcta: recuperar(id_entidad, entidad=None)
            return self._contexto.recuperar(id_usuario, entidad)
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            raise