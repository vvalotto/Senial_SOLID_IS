"""
Módulo que define la entidad Senial - VERSIÓN ANTI-PATRÓN.

⚠️ ADVERTENCIA DIDÁCTICA: Este código demuestra VIOLACIONES INTENCIONALES de principios SOLID.
📚 PROPÓSITO EDUCATIVO: Mostrar el contraste entre "funciona" vs "funciona correctamente".

🚨 VIOLACIONES IMPLEMENTADAS:
- ❌ SRP: Una clase con múltiples responsabilidades (lista + cola + validación)
- ❌ OCP: Modificación requerida para agregar nuevos tipos (isinstance anti-pattern)
- ❌ LSP: Comportamientos completamente diferentes en subclases
- ❌ DIP: Dependencia de clases concretas (isinstance checks)

📖 PARA COMPARAR CON: Implementación SOLID correcta en versión futura
🎯 OBJETIVO: Demostrar por qué los principios SOLID son necesarios

Autor: Victor Valotto
Propósito: Demostración didáctica de anti-patrones
"""
from typing import Any, List


class Senial:
    """
    ❌ CLASE BASE CON VIOLACIONES MÚLTIPLES DE SOLID

    🚨 VIOLACIÓN DE SRP:
    Esta clase tiene MÚLTIPLES responsabilidades:
    1. Manejar lista básica de valores
    2. Validar límites de capacidad
    3. Manejar lógica específica de cola (instanceof)
    4. Gestionar diferentes estructuras de datos

    🚨 VIOLACIÓN DE OCP:
    Para agregar un nuevo tipo (ej: SenialDeque), se debe MODIFICAR
    el metodo poner_valor() agregando más checks instanceof.

    🚨 VIOLACIÓN DE LSP:
    Las subclases tienen comportamientos completamente diferentes:
    - Senial usa append()
    - SenialCola usa índice circular
    ¡No son intercambiables!

    🚨 VIOLACIÓN DE DIP:
    Depende directamente de clases concretas (SenialCola)
    mediante isinstance() checks.
    """

    def __init__(self, tamanio: int = 10):
        """
        Constructor: Inicializa la lista de valores vacía.
        :param tamanio: Tamaño inicial de la señal.
        """
        self._valores: List[float] = []
        self._fecha_adquisicion = None
        self._cantidad = 0
        self._tamanio = tamanio

    # Propiedades
    @property
    def fecha_adquisicion(self) -> Any:
        return self._fecha_adquisicion

    @fecha_adquisicion.setter
    def fecha_adquisicion(self, valor) -> None:
        self._fecha_adquisicion = valor

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor) -> None:
        self._cantidad = valor

    @property
    def tamanio(self) -> int:
        return self._tamanio

    @tamanio.setter
    def tamanio(self, valor)-> None:
        self._tamanio = valor

    @property
    def valores(self) -> List[float]:
        return self._valores

    @valores.setter
    def valores(self, datos: List[float]) -> None:
        self._valores = datos

    def poner_valor(self, valor):
        """
        ❌ METODO QUE VIOLA MÚLTIPLES PRINCIPIOS SOLID

        🚨 VIOLACIÓN DE SRP:
        Este metodo tiene MÚLTIPLES responsabilidades:
        - Validar límites de capacidad
        - Manejar lógica de lista básica
        - Manejar lógica específica de cola circular
        - Actualizar contadores

        🚨 VIOLACIÓN DE OCP:
        Para agregar SenialDeque, se debe MODIFICAR este metodo:
        elif isinstance(self, SenialDeque): # ← Nueva modificación requerida

        🚨 VIOLACIÓN DE LSP:
        Mismo metodo, comportamientos COMPLETAMENTE DIFERENTES:
        - Senial: usa append() → lista dinámica
        - SenialCola: usa índice → array circular

        🚨 VIOLACIÓN DE DIP:
        Depende de clase concreta SenialCola mediante isinstance()

        :param valor: dato de la senial obtenida
        """
        if self._cantidad >= self._tamanio:
            print('Error: No se pueden poner más datos')
            return

        # ❌ ANTI-PATRÓN: isinstance() check - viola OCP y DIP
        if isinstance(self, SenialCola):
            # Lógica específica de cola circular hardcodeada
            self._valores[self._cola] = valor
            self._cola = (self._cola + 1) % self._tamanio
        else:
            # Lógica básica de lista
            self._valores.append(valor)

        self._cantidad += 1

    def obtener_valor(self, indice: int) -> Any:
        """
        Recupera el contenido según el indice
        :param indice: Indice del valor a recuperar.
        :return: Valor en el indice especificado.
        """
        try:
            valor = self._valores[indice]
            return valor
        except IndexError:
            print(f'Error: Índice {indice} fuera de rango')
            return None

    def obtener_tamanio(self) -> int:
        """
        ⚠️ METODO PROBLEMÁTICO - Inconsistente entre subclases

        🚨 PROBLEMA LSP:
        - En Senial: len(self._valores) funciona correctamente
        - En SenialCola: len(self._valores) puede incluir elementos None
        - En SenialPila: len(self._valores) no refleja _cantidad real

        :return: Tamaño de la lista de valores (inconsistente por violaciones)
        """
        return len(self._valores)

    def esta_vacia(self) -> bool:
        """
        ⚠️ METODO AGREGADO PARA COMPATIBILIDAD CON VISUALIZADOR

        🚨 PROBLEMA LSP:
        Diferentes implementaciones necesitarían lógicas diferentes:
        - Senial: len(_valores) == 0
        - SenialPila: _cantidad == 0
        - SenialCola: _cantidad == 0

        Esta implementación es INCORRECTA para subclases pero funciona por casualidad.

        :return: True si la señal está vacía (resultado inconsistente)
        """
        return len(self._valores) == 0

    def obtener_valores(self) -> List[float]:
        """
        Retorna la lista de valores.
        :return: Lista de valores.
        """
        return self._valores

    def poner_valores(self, valores: List[float]) -> None:
        """
        Agrega una lista de valores a la lista de la señal
        :param valores: lista de valores a agregar
        """
        self._valores = valores

class SenialPila(Senial):
    """
    ⚠️ SUBCLASE CON VIOLACIONES LSP MENORES

    🚨 VIOLACIONES LSP REALES:
    - Agrega método sacar_valor() que NO existe en clase base (extiende interfaz)
    - Constructor compatible pero comportamiento interno diferente

    ✅ LSP RESPETADO EN:
    - sacar_valor(): Cumple contrato de "extraer elemento" con semántica LIFO apropiada
    - Métodos heredados: Funcionan correctamente para acceso por índice

    🚨 PROBLEMAS TÉCNICOS DETECTADOS:
    - Usa _cantidad para validar, pero acceso directo a _valores[]
    - Mezcla semántica LIFO (sacar_valor) con acceso aleatorio (obtener_valor)
    - NO es problema LSP sino de DISEÑO de interfaz

    ⚠️ NOTA: Funciona correctamente, diseño mejorable
    """
    def sacar_valor(self) -> Any:
        """
        Saca un valor de la pila.
        :return: Valor sacado de la pila.
        """
        if self._cantidad != 0:
            self._cantidad -= 1
            return self._valores[self._cantidad]
        else:
            print('Error: No hay valores para sacar')
            return None

class SenialCola(Senial):
    """
    ❌ SUBCLASE CON VIOLACIONES LSP GRAVES

    🚨 VIOLACIONES CRÍTICAS DE LSP:
    - Constructor INCOMPATIBLE: requiere parámetro obligatorio (rompe sustitución)
    - Estructura interna INCOMPATIBLE: [None] * tamanio vs [] (rompe invariantes)
    - obtener_tamanio() devuelve tamaño fijo vs tamaño real (comportamiento inconsistente)
    - obtener_valor() puede devolver None vs siempre valor válido (postcondición violada)

    ✅ LSP RESPETADO EN:
    - sacar_valor(): Cumple contrato correcto con semántica FIFO apropiada

    🚨 VIOLACIONES ADICIONALES (OCP):
    - Requiere lógica específica hardcodeada en clase base (isinstance)
    - Clase base modificada específicamente para esta subclase

    ❌ ANTI-PATRÓN DEMOSTRADO:
    Esta clase "funciona" solo porque la clase base fue modificada
    específicamente para ella (violación grave de OCP)
    """
    def __init__(self, tamanio: int):
        """
        Construye la instancia de la estructura cola circular, donde se indica el
        tamaño de la cola y se inicializan los punteros de la cabeza y cola.
        :param tamanio: Tamaño de la cola.
        """
        super().__init__(tamanio)
        self._cabeza = 0
        self._cola = 0
        self._valores = [None] * tamanio

    def sacar_valor(self) -> Any:
        """
        ✅ METODO QUE RESPETA LSP CORRECTAMENTE

        📖 ANÁLISIS LSP REFINADO:
        Este método SÍ respeta LSP porque el contrato es claro:
        "extraer un elemento de la estructura según su semántica específica"

        🎯 CONTRATO CUMPLIDO:
        - SenialPila.sacar_valor() → LIFO (comportamiento esperado para pila)
        - SenialCola.sacar_valor() → FIFO (comportamiento esperado para cola)
        - Ambas devuelven: elemento válido o None si está vacía

        ✅ INTERCAMBIABILIDAD POLIMÓRFICA:
        ```python
        def vaciar_estructura(estructura):
            while not estructura.esta_vacia():
                valor = estructura.sacar_valor()  # ← Funciona correctamente
                procesar(valor)
        ```

        🎓 LECCIÓN TÉCNICA:
        En estructuras de datos es NORMAL que implementaciones diferentes
        tengan semánticas específicas (LIFO vs FIFO) manteniendo el contrato común.

        :return: dato extraído (FIFO - primer elemento insertado)
        """
        if self._cantidad == 0:
            print('Error: No hay valores para sacar')
            return None

        valor = self._valores[self._cabeza]
        self._valores[self._cabeza] = None
        self._cabeza = (self._cabeza + 1) % self._tamanio
        self._cantidad -= 1
        return valor