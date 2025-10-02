"""
Módulo de persistencia de señales digitales

Responsabilidad: Guardar y recuperar señales en diferentes formatos de almacenamiento.

⚠️ VIOLACIÓN ISP INTENCIONAL (Interface Segregation Principle):
Este módulo contiene una interfaz "gorda" (fat interface) donde todos los
persistidores implementan TANTO persistir() COMO recuperar(), forzando a los
clientes a depender de métodos que pueden no necesitar.

PROBLEMA DEMOSTRADO:
- Un Adquisidor que solo ESCRIBE debe conocer el método recuperar()
- Un Visualizador que solo LEE debe conocer el método persistir()
- Violación del principio: "Los clientes no deben depender de interfaces que no usan"

🎯 OBJETIVO DIDÁCTICO:
Demostrar el problema ISP antes de aplicar la solución con interfaces segregadas.

✅ PRINCIPIOS APLICADOS CORRECTAMENTE:
- SRP: Cada persistidor tiene una responsabilidad única (estrategia de persistencia)
- OCP: Extensible mediante nuevos persistidores sin modificar código existente
- DIP: Dependencia en abstracción (BasePersistidor) no en implementaciones concretas

Versión: 1.0.0 - Diseño base con violación ISP intencional
Autor: Victor Valotto
"""
import os
import pickle
import logging
import importlib
from abc import ABC, abstractmethod
from typing import Any, Optional
from persistidor_senial.mapeador import MapeadorArchivo

# Configuración del logger para el módulo
logger = logging.getLogger(__name__)


class BasePersistidor(ABC):
    """
    🏛️ CLASE ABSTRACTA BASE - Interfaz común para todos los persistidores.

    ⚠️ VIOLACIÓN ISP DOCUMENTADA:
    Esta clase abstracta define una interfaz "gorda" que obliga a todas las
    implementaciones a proveer TANTO persistir() COMO recuperar(), incluso
    cuando los clientes solo necesitan una de estas operaciones.

    📖 RESPONSABILIDADES:
    1. Gestión del recurso físico (directorio de almacenamiento)
    2. Validaciones comunes de parámetros
    3. Definición de contrato para operaciones de persistencia

    ✅ OCP APLICADO:
    Permite extensión mediante nuevas implementaciones (PersistidorJSON,
    PersistidorSQL) sin modificar código existente.

    🎓 DISEÑO:
    - Template para lógica común (inicialización, validaciones)
    - Strategy para algoritmos específicos (pickle vs archivo vs otros)
    """

    def __init__(self, recurso: str):
        """
        Inicializa el contexto de persistencia con el recurso físico.

        Crea el directorio de almacenamiento si no existe, aplicando el
        principio de "fail-fast" con validaciones tempranas.

        :param recurso: Path del directorio donde se almacenarán los archivos
        :raises ValueError: Si el recurso es None, vacío o contiene solo espacios
        :raises IOError: Si no se puede crear el directorio
        """
        if not recurso or not recurso.strip():
            raise ValueError("El parámetro 'recurso' no puede estar vacío")

        self._recurso = recurso.strip()

        try:
            if not os.path.isdir(self._recurso):
                os.makedirs(self._recurso, exist_ok=True)
                logger.info(f"Directorio de persistencia creado: {self._recurso}")
        except OSError as e:
            logger.error(f"Error al crear directorio '{self._recurso}': {e}")
            raise IOError(f"No se pudo crear el directorio de persistencia: {e}") from e

    @property
    def recurso(self) -> str:
        """
        Path del recurso físico donde se almacenan las entidades.

        :return: Path absoluto o relativo del directorio de almacenamiento
        """
        return self._recurso

    @abstractmethod
    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """
        ⚠️ MÉTODO ABSTRACTO - Persiste una entidad en el almacenamiento.

        VIOLACIÓN ISP: Este método está en la misma interfaz que recuperar(),
        forzando a clientes que solo leen a conocer esta operación.

        :param entidad: Objeto a persistir (debe ser serializable)
        :param id_entidad: Identificador único para el archivo
        :raises ValueError: Si los parámetros son inválidos
        :raises IOError: Si falla la operación de escritura
        """
        pass

    @abstractmethod
    def recuperar(self, id_entidad: str, entidad: Optional[Any] = None) -> Optional[Any]:
        """
        ⚠️ MÉTODO ABSTRACTO - Recupera una entidad desde el almacenamiento.

        VIOLACIÓN ISP: Este método está en la misma interfaz que persistir(),
        forzando a clientes que solo escriben a conocer esta operación.

        INCONSISTENCIA DE FIRMA: El parámetro 'entidad' es necesario para
        PersistidorArchivo (deserialización manual) pero NO para PersistidorPickle
        (reconstrucción automática). Esto es parte de la demostración del problema.

        :param id_entidad: Identificador único del archivo a recuperar
        :param entidad: Instancia vacía para deserialización (solo PersistidorArchivo)
        :return: Entidad recuperada o None si no existe o hay error
        :raises ValueError: Si los parámetros son inválidos
        """
        pass

    def _validar_entidad(self, entidad: Any, nombre_param: str = "entidad") -> None:
        """
        Validación defensiva: Verifica que la entidad no sea None.

        :param entidad: Objeto a validar
        :param nombre_param: Nombre del parámetro para mensajes de error
        :raises ValueError: Si la entidad es None
        """
        if entidad is None:
            raise ValueError(f"El parámetro '{nombre_param}' no puede ser None")

    def _validar_id_entidad(self, id_entidad: str) -> None:
        """
        Validación defensiva: Verifica que el ID no esté vacío.

        :param id_entidad: Identificador a validar
        :raises ValueError: Si el ID es None, vacío o solo espacios
        """
        if not id_entidad or not id_entidad.strip():
            raise ValueError("El parámetro 'id_entidad' no puede estar vacío")


class PersistidorPickle(BasePersistidor):
    """
    📦 PERSISTIDOR BINARIO - Serialización usando pickle de Python.

    🎯 ESTRATEGIA:
    Usa el módulo pickle para serialización/deserialización automática,
    preservando completamente la estructura del objeto Python.

    ✅ VENTAJAS:
    - Rápido y eficiente
    - Preserva tipos complejos (listas, objetos anidados)
    - No requiere mapeo manual

    ⚠️ DESVENTAJAS:
    - Formato binario (no human-readable)
    - Solo funciona entre aplicaciones Python
    - Potencial riesgo de seguridad con datos no confiables

    ⚠️ VIOLACIÓN ISP HEREDADA:
    Implementa persistir() y recuperar() aunque algunos clientes
    solo necesiten una de estas operaciones.
    """

    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """
        Serializa y guarda una entidad en formato pickle.

        :param entidad: Objeto a persistir (debe ser pickleable)
        :param id_entidad: Identificador único (sin extensión)
        :raises ValueError: Si entidad es None o id_entidad está vacío
        :raises IOError: Si falla la escritura del archivo
        """
        self._validar_entidad(entidad)
        self._validar_id_entidad(id_entidad)

        archivo = f"{id_entidad.strip()}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "wb") as f:
                pickle.dump(entidad, f, protocol=pickle.HIGHEST_PROTOCOL)
            logger.info(f"Entidad persistida exitosamente: {id_entidad} → {ubicacion}")
        except (IOError, pickle.PicklingError) as e:
            logger.error(f"Error al persistir entidad '{id_entidad}': {e}")
            raise IOError(f"Fallo al guardar entidad con pickle: {e}") from e

    def recuperar(self, id_entidad: str, entidad: Optional[Any] = None) -> Optional[Any]:
        """
        Deserializa y recupera una entidad desde archivo pickle.

        NOTA: El parámetro 'entidad' es ignorado (pickle reconstruye automáticamente),
        pero está presente por coherencia con la interfaz base.

        :param id_entidad: Identificador único (sin extensión)
        :param entidad: NO USADO - Presente por interfaz común
        :return: Entidad reconstruida o None si no existe/falla
        :raises ValueError: Si id_entidad está vacío
        """
        self._validar_id_entidad(id_entidad)

        archivo = f"{id_entidad.strip()}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "rb") as f:
                resultado = pickle.load(f)
            logger.info(f"Entidad recuperada exitosamente: {id_entidad} ← {ubicacion}")
            return resultado
        except FileNotFoundError:
            logger.warning(f"Archivo no encontrado: {ubicacion}")
            return None
        except (IOError, pickle.UnpicklingError) as e:
            logger.error(f"Error al recuperar entidad '{id_entidad}': {e}")
            return None


class PersistidorArchivo(BasePersistidor):
    """
    📄 PERSISTIDOR TEXTO PLANO - Serialización human-readable con mapeo custom.

    🎯 ESTRATEGIA:
    Usa MapeadorArchivo para convertir objetos a formato de texto plano
    con sintaxis clave:valor, incluyendo metadatos de tipo de clase.

    ✅ VENTAJAS:
    - Formato human-readable (debugging fácil)
    - Portable entre diferentes lenguajes
    - Inspección directa de archivos .dat

    ⚠️ DESVENTAJAS:
    - Más lento que pickle
    - Requiere mapeo manual (MapeadorArchivo)
    - Limitado a tipos soportados por el mapeador

    ⚠️ VIOLACIÓN ISP HEREDADA:
    Implementa persistir() y recuperar() aunque algunos clientes
    solo necesiten una de estas operaciones.

    📋 FORMATO DE ARCHIVO:
    ```
    __class__:dominio_senial.senial.SenialLista
    _tamanio:100,_cantidad:5,
    _valores>0:10.5
    _valores>1:20.3
    ```
    """

    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """
        Mapea y guarda una entidad en formato texto plano.

        FORMATO: Primera línea contiene metadato de tipo, seguido por
        datos mapeados usando MapeadorArchivo.

        :param entidad: Objeto a persistir (debe soportar mapeo)
        :param id_entidad: Identificador único (sin extensión)
        :raises ValueError: Si entidad es None o id_entidad está vacío
        :raises IOError: Si falla la escritura del archivo
        """
        self._validar_entidad(entidad)
        self._validar_id_entidad(id_entidad)

        archivo = f"{id_entidad.strip()}.dat"
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            # Metadato de tipo para reconstrucción automática
            tipo_clase = f"__class__:{type(entidad).__module__}.{type(entidad).__name__}\n"

            # Serialización con mapeador
            mapeador = MapeadorArchivo()
            contenido = tipo_clase + mapeador.ir_a_persistidor(entidad)

            with open(ubicacion, "w", encoding="utf-8") as f:
                f.write(contenido)
            logger.info(f"Entidad persistida exitosamente: {id_entidad} → {ubicacion}")
        except IOError as e:
            logger.error(f"Error al persistir entidad '{id_entidad}': {e}")
            raise IOError(f"Fallo al guardar entidad en archivo: {e}") from e

    def recuperar(self, id_entidad: str, entidad: Optional[Any] = None) -> Optional[Any]:
        """
        Desmapea y recupera una entidad desde archivo texto plano.

        RECONSTRUCCIÓN AUTOMÁTICA: Lee metadato de tipo desde la primera línea
        y crea instancia dinámicamente usando importlib.

        :param id_entidad: Identificador único (sin extensión)
        :param entidad: OPCIONAL - Si se proporciona, se usa en lugar de crear instancia nueva
        :return: Entidad reconstruida o None si no existe/falla
        :raises ValueError: Si id_entidad está vacío o formato inválido
        """
        self._validar_id_entidad(id_entidad)

        archivo = f"{id_entidad.strip()}.dat"
        ubicacion = os.path.join(self._recurso, archivo)

        try:
            with open(ubicacion, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            # Validar formato: debe tener metadato de clase
            if not lineas or not lineas[0].startswith("__class__:"):
                raise ValueError(f"Archivo '{archivo}' no contiene metadato de tipo válido")

            # Extraer información de tipo
            tipo_info = lineas[0].strip().split(":", 1)[1]
            modulo_nombre, clase_nombre = tipo_info.rsplit(".", 1)

            # Crear instancia (si no se proporcionó una)
            if entidad is None:
                modulo = importlib.import_module(modulo_nombre)
                clase = getattr(modulo, clase_nombre)
                entidad = clase()

            # Deserialización con mapeador
            contenido = ''.join(lineas[1:])
            mapeador = MapeadorArchivo()
            resultado = mapeador.venir_desde_persistidor(entidad, contenido)

            logger.info(f"Entidad recuperada exitosamente: {id_entidad} ← {ubicacion}")
            return resultado

        except FileNotFoundError:
            logger.warning(f"Archivo no encontrado: {ubicacion}")
            return None
        except (IOError, ValueError, ImportError, AttributeError) as e:
            logger.error(f"Error al recuperar entidad '{id_entidad}': {e}")
            return None
