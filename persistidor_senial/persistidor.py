"""
Modulo que contiene la responsabilidad de guardar las seniales, adquiridas y procesadas
en algun tipo de almacen de persistencia (archivo plano, xml, base de dato)
"""
import os
import pickle
import logging
from persistidor_senial.mapeador import *
from typing import Any, Optional

# Configuración del logger para el módulo
logger = logging.getLogger(__name__)


class PersistidorPickle:
    """
    Clase de persistidor que persiste un tipo de objeto de manera serializada
    """

    def __init__(self, recurso: str):
        """
        Se crea el archivo con el path donde se guardarán los archivos
        de las entidades a persistir.
        :param recurso: Path del repositorio de entidades.
        :raises ValueError: Si el recurso es None o está vacío.
        """
        if not recurso or not recurso.strip():
            raise ValueError("El parámetro 'recurso' no puede estar vacío")

        self._recurso = recurso
        if not os.path.isdir(recurso):
            os.makedirs(recurso, exist_ok=True)
            logger.info(f"Directorio creado: {recurso}")

    def persistir(self, entidad: Any, nombre_entidad: str) -> None:
        """
        Se persiste el objeto (entidad) y se indica el tipo de entidad.
        :param entidad: Objeto a persistir.
        :param nombre_entidad: Nombre del archivo donde se guardará la entidad.
        :raises ValueError: Si entidad es None o nombre_entidad está vacío.
        """
        if entidad is None:
            raise ValueError("El parámetro 'entidad' no puede ser None")
        if not nombre_entidad or not nombre_entidad.strip():
            raise ValueError("El parámetro 'nombre_entidad' no puede estar vacío")

        archivo = f"{nombre_entidad}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)
        try:
            with open(ubicacion, "wb") as archivo:
                pickle.dump(entidad, archivo)
            logger.info(f"Entidad persistida exitosamente: {nombre_entidad}")
        except IOError as e:
            logger.error(f"Error al guardar la entidad '{nombre_entidad}': {e}")
            raise

    def recuperar(self, id_entidad: str) -> Optional[Any]:
        """
        Se lee la entidad a tratar.
        :param id_entidad: Identificador de la entidad a recuperar.
        :return: Entidad recuperada o None si no existe.
        :raises ValueError: Si id_entidad está vacío.
        """
        if not id_entidad or not id_entidad.strip():
            raise ValueError("El parámetro 'id_entidad' no puede estar vacío")

        archivo = f"{id_entidad}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)
        try:
            with open(ubicacion, "rb") as archivo:
                entidad = pickle.load(archivo)
            logger.info(f"Entidad recuperada exitosamente: {id_entidad}")
            return entidad
        except FileNotFoundError:
            logger.warning(f"Entidad no encontrada: {id_entidad}")
            return None
        except (IOError, ValueError) as e:
            logger.error(f"Error al recuperar la entidad '{id_entidad}': {e}")
            return None

class PersistidorArchivo:
    """
    Contexto del recurso de persistencia de tipo archivo
    """
    def __init__(self, recurso: str):
        """
        Se crea el archivo con el path donde se guardarán los archivos
        de las entidades a persistir.
        :param recurso: Path del repositorio de entidades.
        :raises ValueError: Si el recurso es None o está vacío.
        :raises IOError: Si no se puede crear el directorio.
        """
        if not recurso or not recurso.strip():
            raise ValueError("El parámetro 'recurso' no puede estar vacío")

        try:
            self._recurso = recurso
            if not os.path.isdir(recurso):
                os.makedirs(recurso, exist_ok=True)
                logger.info(f"Directorio creado: {recurso}")
        except IOError as eIO:
            logger.error(f"Error al crear directorio '{recurso}': {eIO}")
            raise

    def persistir(self, entidad: Any, nombre_entidad: str) -> None:
        """
        Agregar un objeto (entidad) para persistirlo.
        :param entidad: Tipo de entidad.
        :param nombre_entidad: Identificación de la instancia de la entidad.
        :raises ValueError: Si entidad es None o nombre_entidad está vacío.
        """
        if entidad is None:
            raise ValueError("El parámetro 'entidad' no puede ser None")
        if not nombre_entidad or not nombre_entidad.strip():
            raise ValueError("El parámetro 'nombre_entidad' no puede estar vacío")

        mapeador = MapeadorArchivo()
        archivo = f"{nombre_entidad}.dat"
        # Guardar tipo de clase como primera línea
        tipo_clase = f"__class__:{type(entidad).__module__}.{type(entidad).__name__}\n"
        contenido = tipo_clase + mapeador.ir_a_persistidor(entidad)
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "w") as archivo:
                archivo.write(contenido)
            logger.info(f"Entidad persistida exitosamente: {nombre_entidad}")
        except IOError as e:
            logger.error(f"Error al guardar la entidad '{nombre_entidad}': {e}")
            raise

    def recuperar(self, id_entidad: str) -> Optional[Any]:
        """
        Obtiene la entidad guardada.
        :param id_entidad: Identificación de la entidad a recuperar.
        :return: Entidad recuperada o None si no existe.
        :raises ValueError: Si id_entidad está vacío.
        """
        if not id_entidad or not id_entidad.strip():
            raise ValueError("El parámetro 'id_entidad' no puede estar vacío")

        archivo = f"{id_entidad}.dat"
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "r") as archivo:
                lineas = archivo.readlines()

            # Extraer tipo de clase de la primera línea
            if not lineas or not lineas[0].startswith("__class__:"):
                raise ValueError("Archivo no contiene información de tipo de clase")

            tipo_info = lineas[0].strip().split(":", 1)[1]
            modulo_nombre, clase_nombre = tipo_info.rsplit(".", 1)

            # Importar módulo y crear instancia
            import importlib
            modulo = importlib.import_module(modulo_nombre)
            clase = getattr(modulo, clase_nombre)
            entidad = clase()

            # Desmapear contenido (excluyendo primera línea)
            contenido = ''.join(lineas[1:])
            mapeador = MapeadorArchivo()
            resultado = mapeador.venir_desde_persistidor(entidad, contenido)
            logger.info(f"Entidad recuperada exitosamente: {id_entidad}")
            return resultado
        except FileNotFoundError:
            logger.warning(f"Entidad no encontrada: {id_entidad}")
            return None
        except IOError as e:
            logger.error(f"Error al recuperar la entidad '{id_entidad}': {e}")
            return None
        except ValueError as e:
            logger.error(f"Error de valor al recuperar la entidad '{id_entidad}': {e}")
            return None
