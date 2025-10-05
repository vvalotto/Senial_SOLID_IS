"""
Módulo que define la entidad Senial.
Es considerada una entidad del dominio.

✅ VERSIÓN LSP CORRECTA - Refactorización completa aplicando principios SOLID.

📚 EVOLUCIÓN DIDÁCTICA:
- ANTES: Violaciones múltiples de LSP, OCP y SRP (anti-patrón isinstance)
- AHORA: Abstracción con contrato común, intercambiabilidad polimórfica garantizada

🎯 PRINCIPIOS APLICADOS:
- ✅ LSP: Subclases verdaderamente intercambiables con firmas consistentes
- ✅ OCP: Extensible sin modificación (sin instanceof checks)
- ✅ SRP: Cada clase una responsabilidad específica

🏗️ ARQUITECTURA:
- SenialBase(ABC): Abstracción que define contrato común
- SenialLista: Comportamiento de lista dinámica
- SenialPila: Comportamiento LIFO (Last In, First Out)
- SenialCola: Comportamiento FIFO (First In, First Out) con cola circular

Autor: Victor Valotto
Versión: 4.0.0 - LSP Completo + Arquitectura Limpia
"""
from abc import abstractmethod, ABC
from typing import Any, List, Optional


class SenialBase(ABC):
    """
    ✅ ABSTRACCIÓN BASE - Contrato común para todas las señales.

    📖 LSP APLICADO:
    Define métodos abstractos con firmas consistentes que TODAS las subclases
    deben implementar de forma intercambiable.

    🎯 CONTRATO COMÚN:
    - Constructor con parámetro opcional (compatible con todas las subclases)
    - Métodos abstractos con firmas idénticas
    - Propiedades comunes accesibles polimórficamente

    ✅ GARANTÍAS LSP:
    - Intercambiabilidad: Cualquier SenialBase funciona donde se espera la abstracción
    - Precondiciones consistentes: Mismos parámetros en todos los métodos
    - Postcondiciones garantizadas: Comportamiento predecible
    """

    def __init__(self, tamanio: int = 10):
        """
        Constructor común con parámetro opcional.

        ✅ LSP: Parámetro opcional permite instanciar cualquier subclase
        uniformemente sin conocer su tipo específico.

        :param tamanio: Tamaño máximo de la señal (default: 10)
        """
        self._fecha_adquisicion: Any = None
        self._cantidad: int = 0
        self._tamanio: int = tamanio
        self._comentario: str = ''
        self._id: int = 0

    # ==================== PROPIEDADES ====================

    @property
    def fecha_adquisicion(self) -> Any:
        """Fecha de adquisición de la señal."""
        return self._fecha_adquisicion

    @fecha_adquisicion.setter
    def fecha_adquisicion(self, valor: Any) -> None:
        self._fecha_adquisicion = valor

    @property
    def cantidad(self) -> int:
        """Cantidad actual de elementos en la señal."""
        return self._cantidad

    @property
    def tamanio(self) -> int:
        """Tamaño máximo de la señal."""
        return self._tamanio

    @property
    def comentario(self) -> str:
        """Comentario descriptivo de la señal."""
        return self._comentario

    @comentario.setter
    def comentario(self, valor: str) -> None:
        self._comentario = valor

    @property
    def id(self) -> int:
        """Identificador único de la señal."""
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        self._id = valor

    # ==================== MÉTODOS ABSTRACTOS ====================

    @abstractmethod
    def poner_valor(self, valor: float) -> None:
        """
        Agregar valor según la semántica de la estructura.

        ✅ LSP: Firma consistente en todas las subclases.

        :param valor: Valor a agregar
        """
        pass

    @abstractmethod
    def sacar_valor(self) -> Optional[float]:
        """
        Extraer valor según la semántica de la estructura.

        ✅ LSP: Firma consistente SIN parámetros en todas las subclases.
        - SenialLista: Extrae del final (comportamiento por defecto)
        - SenialPila: Extrae del final (LIFO)
        - SenialCola: Extrae del inicio (FIFO)

        :return: Valor extraído o None si está vacía
        """
        pass

    @abstractmethod
    def limpiar(self) -> None:
        """
        Vaciar la estructura según su implementación interna.

        ✅ LSP: Cada subclase limpia correctamente su estructura específica.
        """
        pass

    @abstractmethod
    def obtener_valor(self, indice: int) -> Optional[float]:
        """
        Obtener valor por índice lógico.

        ⚠️ NOTA LSP: Cada subclase interpreta "índice" según su semántica:
        - SenialLista/Pila: Índice directo en array
        - SenialCola: Índice relativo desde la cabeza (cola circular)

        :param indice: Índice del valor a obtener
        :return: Valor en el índice o None si fuera de rango
        """
        pass

    @abstractmethod
    def obtener_tamanio(self) -> int:
        """
        Cantidad actual de elementos.

        ✅ LSP: Retorna cantidad real de elementos (no capacidad).

        :return: Número de elementos actuales
        """
        pass

    def __str__(self) -> str:
        """Representación en string de la señal."""
        return f"Tipo: {type(self).__name__}\nFecha: {self._fecha_adquisicion}"


class SenialLista(SenialBase):
    """
    ✅ SEÑAL CON COMPORTAMIENTO DE LISTA DINÁMICA.

    📖 SEMÁNTICA:
    - Acceso secuencial y por índice
    - Inserción al final
    - Extracción desde el final (por defecto)

    🎯 LSP CUMPLIDO:
    - Constructor compatible: parámetro opcional heredado
    - Métodos con firmas idénticas a la abstracción
    - Comportamiento predecible y consistente
    """

    def __init__(self, tamanio: int = 10):
        super().__init__(tamanio)
        self._valores: List[float] = []

    def poner_valor(self, valor: float) -> None:
        """
        Agrega un valor al final de la lista.

        :param valor: Dato de la señal obtenida
        """
        if self._cantidad >= self._tamanio:
            print('Error: No se pueden poner más datos')
            return
        self._valores.append(valor)
        self._cantidad += 1

    def sacar_valor(self) -> Optional[float]:
        """
        ✅ LSP CORRECTO: Sin parámetros (extrae del final por defecto).

        Comportamiento: Extrae el último elemento (similar a pila).

        :return: Valor extraído del final o None si está vacía
        """
        if self._cantidad == 0:
            print('Error: No hay valores para sacar')
            return None
        self._cantidad -= 1
        return self._valores.pop()

    def sacar_valor_en(self, indice: int) -> Optional[float]:
        """
        ✅ MÉTODO ADICIONAL ESPECÍFICO: Extraer por índice arbitrario.

        ⚠️ NOTA LSP: Este método NO viola LSP porque:
        - No sobrescribe método abstracto
        - Es funcionalidad ADICIONAL específica de SenialLista
        - Clientes polimórficos no dependen de él

        :param indice: Índice del valor a extraer
        :return: Valor extraído o None si índice inválido
        """
        if self._cantidad == 0:
            print('Error: No hay valores para sacar')
            return None
        try:
            valor = self._valores.pop(indice)
            self._cantidad -= 1
            return valor
        except IndexError:
            print(f'Error: Índice {indice} fuera de rango')
            return None

    def limpiar(self) -> None:
        """Vacía completamente la lista."""
        self._valores.clear()
        self._cantidad = 0

    def obtener_valor(self, indice: int) -> Optional[float]:
        """
        Obtiene valor por índice directo.

        :param indice: Índice del valor
        :return: Valor en el índice o None si fuera de rango
        """
        try:
            return self._valores[indice]
        except IndexError:
            print(f'Error: Índice {indice} fuera de rango')
            return None

    def obtener_tamanio(self) -> int:
        """
        ✅ LSP: Retorna cantidad real de elementos.

        :return: Número de elementos en la lista
        """
        return len(self._valores)


class SenialPila(SenialBase):
    """
    ✅ SEÑAL CON COMPORTAMIENTO LIFO (Last In, First Out).

    📖 SEMÁNTICA:
    - Inserción al final (push)
    - Extracción desde el final (pop)
    - Comportamiento clásico de pila

    🎯 LSP CUMPLIDO:
    - Constructor compatible: parámetro opcional
    - sacar_valor() sin parámetros (consistente)
    - Métodos implementados según contrato común
    """

    def __init__(self, tamanio: int = 10):
        super().__init__(tamanio)
        self._valores: List[float] = []

    def poner_valor(self, valor: float) -> None:
        """
        Agrega un valor al tope de la pila (final de la lista).

        :param valor: Dato de la señal obtenida
        """
        if self._cantidad >= self._tamanio:
            print('Error: No se pueden poner más datos')
            return
        self._valores.append(valor)
        self._cantidad += 1

    def sacar_valor(self) -> Optional[float]:
        """
        ✅ LSP CORRECTO: Extrae del tope de la pila (LIFO).

        :return: Valor extraído del tope o None si está vacía
        """
        if self._cantidad == 0:
            print('Error: No hay valores para sacar')
            return None
        self._cantidad -= 1
        return self._valores.pop()

    def limpiar(self) -> None:
        """Vacía completamente la pila."""
        self._valores.clear()
        self._cantidad = 0

    def obtener_valor(self, indice: int) -> Optional[float]:
        """
        Obtiene valor por índice directo en la pila.

        :param indice: Índice del valor (0 = fondo, n-1 = tope)
        :return: Valor en el índice o None si fuera de rango
        """
        try:
            return self._valores[indice]
        except IndexError:
            print(f'Error: Índice {indice} fuera de rango')
            return None

    def obtener_tamanio(self) -> int:
        """
        ✅ LSP: Retorna cantidad real de elementos en la pila.

        :return: Número de elementos actuales
        """
        return len(self._valores)


class SenialCola(SenialBase):
    """
    ✅ SEÑAL CON COMPORTAMIENTO FIFO (First In, First Out) - Cola circular.

    📖 SEMÁNTICA:
    - Inserción al final (enqueue)
    - Extracción desde el inicio (dequeue)
    - Implementación con array circular para eficiencia

    🎯 LSP CUMPLIDO (CORRECCIONES APLICADAS):
    - ✅ Constructor compatible: parámetro opcional (CORREGIDO)
    - ✅ sacar_valor() sin parámetros (consistente)
    - ✅ limpiar() reinicia correctamente punteros circulares
    - ✅ obtener_valor() con lógica circular apropiada
    - ✅ obtener_tamanio() retorna cantidad real (no capacidad)
    """

    def __init__(self, tamanio: int = 10):
        """
        ✅ CORRECCIÓN LSP: Parámetro opcional (antes era obligatorio).

        :param tamanio: Tamaño máximo de la cola circular (default: 10)
        """
        super().__init__(tamanio)
        self._cabeza: int = 0
        self._cola: int = 0
        self._valores: List[Optional[float]] = [None] * tamanio

    def poner_valor(self, valor: float) -> None:
        """
        Agrega un valor al final de la cola circular.

        :param valor: Dato de la señal obtenida
        """
        if self._cantidad >= self._tamanio:
            print('Error: No se pueden poner más datos')
            return
        self._valores[self._cola] = valor
        self._cola = (self._cola + 1) % self._tamanio
        self._cantidad += 1

    def sacar_valor(self) -> Optional[float]:
        """
        ✅ LSP CORRECTO: Extrae desde el inicio de la cola (FIFO).

        :return: Valor extraído del inicio o None si está vacía
        """
        if self._cantidad == 0:
            print('Error: No hay valores para sacar')
            return None

        valor = self._valores[self._cabeza]
        self._valores[self._cabeza] = None
        self._cabeza = (self._cabeza + 1) % self._tamanio
        self._cantidad -= 1
        return valor

    def limpiar(self) -> None:
        """
        ✅ CORRECCIÓN LSP: Reinicia correctamente array circular y punteros.

        ANTES: Usaba .clear() heredado que rompía la estructura circular.
        AHORA: Reinicializa array y resetea punteros cabeza/cola.
        """
        self._valores = [None] * self._tamanio
        self._cabeza = 0
        self._cola = 0
        self._cantidad = 0

    def obtener_valor(self, indice: int) -> Optional[float]:
        """
        ✅ CORRECCIÓN LSP: Acceso considerando cola circular.

        indice=0 devuelve el elemento en la cabeza (próximo a extraer).
        indice=n devuelve el n-ésimo elemento desde la cabeza.

        ANTES: Acceso directo self._valores[indice] devolvía None en posiciones
               ya extraídas o valores incorrectos por rotación circular.
        AHORA: Calcula índice circular correctamente desde la cabeza.

        :param indice: Índice lógico desde la cabeza (0 = próximo a sacar)
        :return: Valor en el índice circular o None si fuera de rango
        """
        if indice < 0 or indice >= self._cantidad:
            print(f'Error: Índice {indice} fuera de rango')
            return None

        # Calcular índice circular desde la cabeza
        indice_real = (self._cabeza + indice) % self._tamanio
        return self._valores[indice_real]

    def obtener_tamanio(self) -> int:
        """
        ✅ CORRECCIÓN LSP: Retorna cantidad de elementos, no capacidad del array.

        ANTES: len(self._valores) retornaba capacidad fija (incluye None).
        AHORA: Retorna self._cantidad (elementos reales).

        :return: Número de elementos actuales en la cola
        """
        return self._cantidad


# ==================== EXPORTS ====================

__all__ = [
    'SenialBase',
    'SenialLista',
    'SenialPila',
    'SenialCola'
]