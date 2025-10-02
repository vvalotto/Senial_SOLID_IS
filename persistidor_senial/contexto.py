"""
Modulo que contiene la responsabilidad de guardar las seniales, adquiridas y procesadas
en algun tipo de almacen de persistencia (archivo plano, xml, base de dato)
"""
import os
import pickle
import importlib
from abc import ABC, abstractmethod
from persistidor_senial.mapeador import MapeadorArchivo
from typing import Any

class BaseContexto(ABC):
    """
    Clase abstract que define la interfaz de la persistencia de datos
    """
    def __init__(self, recurso):
        """
        Se crea el contexto, donde el nombre es el recurso fisico donde residen los datos
        junto con esto se crea el recurso fisico con el nombre
        :param recurso: Path del repositorio de entidades.
        """
        if not recurso:
            raise ValueError("Nombre de recurso vacío")
        self._recurso = recurso
        if not os.path.isdir(recurso):
            os.makedirs(recurso, exist_ok=True)

    @property
    def recurso(self) -> str:
        return self._recurso

    @abstractmethod
    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """
        Se identifica a la instancia de la entidad con nombre_entidad y en entidad es el tipo a persistir
        """
        pass

    @abstractmethod
    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        """
        Se identifica a la instancia de la entidad con nombre_entidad y en entidad es devuelta por el metodo
        :param id_entidad: Identificador de la entidad a recuperar
        :param entidad: Instancia template para deserialización (opcional, usado por ContextoArchivo)
        """
        pass

class ContextoPickle(BaseContexto):
    """
    Clase de persistidor que persiste un tipo de objeto de manera serializada
    """

    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """
        Se persiste el objeto (entidad) y se indica el tipo de entidad.
        :param entidad: Objeto a persistir.
        :param id_entidad: Nombre del archivo donde se guardará la entidad.
        """
        archivo = f"{id_entidad}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)
        try:
            with open(ubicacion, "wb") as archivo:
                pickle.dump(entidad, archivo)
        except IOError as e:
            print(f"Error al guardar la entidad: {e}")

    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        """
        Se lee la entidad a tratar.
        :param id_entidad: Identificador de la entidad a recuperar.
        :param entidad: NO USADO - Parámetro ignorado (pickle reconstruye automáticamente)
        :return: Entidad recuperada.
        """
        archivo = f"{id_entidad}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)
        try:
            with open(ubicacion, "rb") as archivo:
                return pickle.load(archivo)
        except (IOError, ValueError) as e:
            print(f"Error al recuperar la entidad: {e}")
            return None

class ContextoArchivo(BaseContexto):
    """
    Contexto del recurso de persistencia de tipo archivo
    """


    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """
        Agregar un objeto (entidad) para persistirlo.
        :param entidad: Tipo de entidad.
        :param id_entidad: Identificación de la instancia de la entidad.
        """
        mapeador = MapeadorArchivo()
        archivo = f"{id_entidad}.dat"

        # Guardar metadato de tipo de clase para reconstrucción automática
        tipo_clase = f"__class__:{type(entidad).__module__}.{type(entidad).__name__}\n"
        contenido = tipo_clase + mapeador.ir_a_persistidor(entidad)
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "w") as archivo:
                archivo.write(contenido)
        except IOError as e:
            print(f"Error al guardar la entidad: {e}")

    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        """
        Obtiene la entidad guardada.

        RECONSTRUCCIÓN AUTOMÁTICA: Si no se proporciona 'entidad', lee metadatos
        de tipo desde el archivo y crea instancia dinámicamente.

        :param id_entidad: Identificación de la entidad a recuperar.
        :param entidad: Instancia template para deserialización (opcional)
        :return: Entidad recuperada.
        """
        archivo = f"{id_entidad}.dat"
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "r") as archivo:
                lineas = archivo.readlines()

            # Extraer metadato de clase si existe
            if lineas and lineas[0].startswith("__class__:"):
                tipo_info = lineas[0].strip().split(":", 1)[1]
                modulo_nombre, clase_nombre = tipo_info.rsplit(".", 1)

                # Crear instancia automáticamente si no se proporcionó
                if entidad is None:
                    modulo = importlib.import_module(modulo_nombre)
                    clase = getattr(modulo, clase_nombre)
                    entidad = clase()

                # Deserializar contenido (excluyendo primera línea con metadato)
                contenido = ''.join(lineas[1:])
            else:
                # Formato antiguo sin metadatos - requiere entidad
                if entidad is None:
                    raise ValueError("Archivo sin metadatos requiere parámetro 'entidad'")
                contenido = ''.join(lineas)

            mapeador = MapeadorArchivo()
            return mapeador.venir_desde_persistidor(entidad, contenido)

        except IOError as e:
            print(f"Error al recuperar la entidad: {e}")
            return None
        except (ValueError, ImportError, AttributeError) as e:
            print(f"Error de valor al recuperar la entidad: {e}")
            return None
