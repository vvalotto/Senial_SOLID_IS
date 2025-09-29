# VIOLACIONES DE LSP EN TIPOS DE SEÑAL - Análisis Técnico y Demostración

**Proyecto**: Senial SOLID IS
**Autor**: Victor Valotto
**Fecha**: Septiembre 2024
**Objetivo**: Documentar y demostrar violaciones del Liskov Substitution Principle (LSP) en jerarquía de señales

---

## 📋 Resumen Ejecutivo

Este documento identifica y analiza las **violaciones del Liskov Substitution Principle (LSP)** presentes en la implementación de tipos de señal (`Senial`, `SenialPila`, `SenialCola`). Las violaciones demuestran cómo la herencia mal aplicada puede romper la intercambiabilidad polimórfica, sirviendo como base didáctica para comprender LSP y diseñar soluciones correctas.

### 🎯 **Problemática Central**
Las clases `SenialPila` y `SenialCola` heredan de `Senial` pero **NO son verdaderamente intercambiables**, violando el principio fundamental de LSP: "Los objetos de una clase derivada deben ser reemplazables por objetos de la clase base sin alterar el correcto funcionamiento del programa".

---

## 🎯 Fundamentos Teóricos del LSP

### Definición Formal (Barbara Liskov, 1987)

> **"Si φ(x) es una propiedad demostrable de los objetos x de tipo T, entonces φ(y) debe ser verdadera para los objetos y de tipo S, donde S es un subtipo de T"**

#### Interpretación Práctica
- **Intercambiabilidad**: Subclases deben funcionar donde se espera la clase base
- **Contratos respetados**: Precondiciones no fortalecidas, postcondiciones no debilitadas
- **Comportamiento consistente**: Sin sorpresas o efectos colaterales inesperados

### Reglas de Cumplimiento LSP

#### 1. **Regla de Precondiciones**
- Subclases **NO** pueden requerir entrada más restrictiva que la clase base
- `SenialCola(tamanio)` vs `Senial()` ← **VIOLACIÓN**

#### 2. **Regla de Postcondiciones**
- Subclases **NO** pueden garantizar menos de lo que garantiza la clase base
- Diferentes comportamientos de extracción ← **VIOLACIÓN**

#### 3. **Regla de Invariantes**
- Propiedades que deben mantenerse verdaderas en la clase base deben mantenerse en subclases
- Estructura interna diferente (`lista` vs `array circular`) ← **VIOLACIÓN**

#### 4. **Regla de Historia (History Constraint)**
- Subclases no deben permitir cambios de estado no permitidos por la clase base
- Diferentes ordenes de acceso a datos ← **VIOLACIÓN**

---

## 🚨 Análisis de Violaciones Identificadas

### 1. VIOLACIÓN CRÍTICA: Constructor Incompatible

#### Problema Detectado
```python
# ❌ VIOLACIÓN LSP: Constructores incompatibles
def usar_cualquier_senial():
    # Con Senial base
    senial1 = Senial()          # ✅ Funciona: parámetro opcional
    senial2 = Senial(20)        # ✅ Funciona: parámetro explícito

    # Con SenialPila
    pila1 = SenialPila()        # ✅ Funciona: hereda constructor
    pila2 = SenialPila(20)      # ✅ Funciona: hereda constructor

    # Con SenialCola
    cola1 = SenialCola()        # ❌ ERROR: TypeError - parámetro requerido
    cola2 = SenialCola(20)      # ✅ Funciona solo con parámetro obligatorio
```

#### Análisis Técnico
- **Violación de precondición**: `SenialCola` requiere parámetro obligatorio
- **Intercambiabilidad rota**: No se puede usar `SenialCola` donde se espera `Senial`
- **Polimorfismo fallido**: El factory pattern no funciona uniformemente

#### Impacto en el Sistema
```python
# ❌ CÓDIGO QUE FALLA por violación LSP
def factory_polimorfismo_roto(tipo):
    tipos = {
        'lista': Senial,
        'pila': SenialPila,
        'cola': SenialCola  # ← Este rompe el patrón
    }
    return tipos[tipo]()  # ← FALLA con SenialCola
```

### 2. VIOLACIÓN SEMÁNTICA: Comportamiento de Extracción Opuesto

#### Problema Detectado
```python
# ❌ VIOLACIÓN LSP: Mismo método, comportamientos OPUESTOS
def demostrar_violacion_semantica():
    # Configuración idéntica para todas
    señales = [
        Senial(),
        SenialPila(),
        SenialCola(5)  # ← Constructor ya es problemático
    ]

    # Llenar con datos idénticos
    for senial in señales:
        for i in range(3):
            senial.poner_valor(float(i))  # [0.0, 1.0, 2.0]

    # ❌ COMPORTAMIENTOS COMPLETAMENTE DIFERENTES
    # SenialPila.sacar_valor() → 2.0 (LIFO - último)
    # SenialCola.sacar_valor() → 0.0 (FIFO - primero)
    # ¡COMPORTAMIENTO OPUESTO para el mismo método!
```

#### Análisis Detallado
- **Violación de postcondición**: Mismo método produce resultados opuestos
- **Principio de menor sorpresa roto**: Comportamiento impredecible
- **Semántica inconsistente**: LIFO vs FIFO usando mismo interface

#### Demostración Experimental
```python
def probar_intercambiabilidad_rota(senial):
    """
    Esta función DEBERÍA funcionar con cualquier subtipo de Senial
    ❌ PERO NO FUNCIONA debido a violaciones LSP
    """
    senial.poner_valor(10.0)
    senial.poner_valor(20.0)
    senial.poner_valor(30.0)

    if hasattr(senial, 'sacar_valor'):
        valor = senial.sacar_valor()
        # ¿Qué valor esperamos?
        # Con SenialPila: 30.0 ← LIFO
        # Con SenialCola: 10.0 ← FIFO
        # ¡IMPOSIBLE PREDECIR sin conocer el tipo concreto!
        return valor

    return "Sin método sacar_valor"

# ❌ VIOLACIÓN DEMOSTRADA
pila = SenialPila()
cola = SenialCola(5)

resultado_pila = probar_intercambiabilidad_rota(pila)  # → 30.0
resultado_cola = probar_intercambiabilidad_rota(cola)  # → 10.0
# ¡RESULTADOS OPUESTOS! LSP VIOLADO
```

### 3. VIOLACIÓN ESTRUCTURAL: Invariantes Rotas

#### Problema Detectado
```python
# ❌ VIOLACIÓN LSP: Estructura interna incompatible
class Senial:
    def __init__(self):
        self._valores = []  # ← Lista dinámica

class SenialCola(Senial):
    def __init__(self, tamanio):
        super().__init__(tamanio)
        self._valores = [None] * tamanio  # ← Array circular FIJO
        self._cabeza = 0
        self._cola = 0
```

#### Análisis Técnico
- **Invariante de estructura rota**: `_valores` cambia de lista dinámica a array fijo
- **Estado interno inconsistente**: Punteros adicionales no esperados por clase base
- **Herencia mal aplicada**: Sobreescribe comportamiento fundamental

#### Impacto en Métodos Heredados
```python
# ❌ MÉTODO HEREDADO INCOMPATIBLE con nueva estructura
def poner_valor(self, valor):
    """Método heredado de Senial - FUNCIONA MAL en SenialCola"""
    self._valores.append(valor)  # ← ROMPE el array circular
    self._cantidad += 1

# SenialCola debería usar:
# self._valores[self._cola] = valor
# self._cola = (self._cola + 1) % self._tamanio
```

### 4. VIOLACIÓN DE INTERFAZ: Métodos Específicos No Polimórficos

#### Problema Detectado
```python
# ❌ VIOLACIÓN LSP: Métodos que no están en la clase base
def procesar_senial_generica(senial):
    """Debería funcionar con cualquier Senial"""
    senial.poner_valor(5.0)

    # ❌ PROBLEMA: ¿Cómo extraigo el valor de manera polimórfica?
    # senial.obtener_valor(0)?     ← Solo funciona con lista
    # senial.sacar_valor()?        ← Solo existe en Pila/Cola
    # ¿Cuál usar para ser polimórfico?

    # ❌ FORZADO A USAR isinstance (anti-patrón)
    if isinstance(senial, SenialPila):
        return senial.sacar_valor()  # LIFO
    elif isinstance(senial, SenialCola):
        return senial.sacar_valor()  # FIFO (¡diferente!)
    else:
        return senial.obtener_valor(0)  # Por índice
```

#### Análisis del Anti-patrón
- **Uso de `isinstance`**: Indica violación LSP
- **Comportamiento condicional**: Rompe polimorfismo
- **Cliente debe conocer tipos concretos**: Viola encapsulación

---

## 🧪 Pruebas de Violación LSP

### Test Suite para Demostrar Violaciones

```python
import pytest
from dominio_senial import Senial, SenialPila, SenialCola

class TestViolacionesLSP:
    """
    Suite de tests que demuestra violaciones específicas de LSP
    """

    def test_violacion_constructor_incompatible(self):
        """Demuestra que los constructores no son intercambiables"""
        # ✅ Clase base funciona sin parámetros
        senial = Senial()
        assert senial is not None

        # ✅ Pila hereda constructor compatible
        pila = SenialPila()
        assert pila is not None

        # ❌ Cola REQUIERE parámetro - VIOLACIÓN LSP
        with pytest.raises(TypeError):
            cola = SenialCola()  # ← FALLA

    def test_violacion_comportamiento_sacar_valor(self):
        """Demuestra comportamientos opuestos en subclases"""
        # Configuración idéntica
        pila = SenialPila()
        cola = SenialCola(5)

        valores = [1.0, 2.0, 3.0]

        # Llenar con mismos datos
        for valor in valores:
            pila.poner_valor(valor)
            cola.poner_valor(valor)

        # ❌ COMPORTAMIENTOS OPUESTOS - VIOLACIÓN LSP
        valor_pila = pila.sacar_valor()  # → 3.0 (último - LIFO)
        valor_cola = cola.sacar_valor()  # → 1.0 (primero - FIFO)

        # ¡VALORES DIFERENTES! LSP VIOLADO
        assert valor_pila != valor_cola
        assert valor_pila == 3.0
        assert valor_cola == 1.0

    def test_violacion_polimorfismo_roto(self):
        """Demuestra que el polimorfismo no funciona"""
        def procesar_senial_cualquiera(senial):
            """Función que DEBERÍA funcionar con cualquier Senial"""
            senial.poner_valor(100.0)
            # ❌ ¿Cómo accedo al dato polimórficamente?
            # No hay interfaz común para extraer datos

            if hasattr(senial, 'sacar_valor'):
                return senial.sacar_valor()
            else:
                return senial.obtener_valor(0) if senial.obtener_tamanio() > 0 else None

        # Resultados inconsistentes por violación LSP
        lista = Senial()
        pila = SenialPila()
        cola = SenialCola(5)

        resultado_lista = procesar_senial_cualquiera(lista)
        resultado_pila = procesar_senial_cualquiera(pila)
        resultado_cola = procesar_senial_cualquiera(cola)

        # ❌ TODOS DEBERÍAN DAR EL MISMO RESULTADO (LSP)
        # PERO NO LO HACEN por violaciones
        assert resultado_lista == 100.0  # obtener_valor(0)
        assert resultado_pila == 100.0   # sacar_valor() LIFO
        assert resultado_cola == 100.0   # sacar_valor() FIFO
        # ¡Solo por casualidad dan igual en este caso específico!

    def test_violacion_factory_pattern(self):
        """Demuestra que el Factory Pattern falla por LSP violado"""
        def crear_senial_por_tipo(tipo):
            """Factory que DEBERÍA crear cualquier tipo uniformemente"""
            if tipo == 'lista':
                return Senial()
            elif tipo == 'pila':
                return SenialPila()
            elif tipo == 'cola':
                return SenialCola(10)  # ← Parámetro hardcodeado por violación

        # ❌ FACTORY INCONSISTENTE por violaciones LSP
        tipos = ['lista', 'pila', 'cola']
        instancias = []

        for tipo in tipos:
            instancia = crear_senial_por_tipo(tipo)
            instancias.append(instancia)

        # Todas deberían comportarse igual polimórficamente
        for instancia in instancias:
            instancia.poner_valor(42.0)
            # ❌ Pero no podemos acceder uniformemente a los datos
```

### Métricas de Violación

#### Indicadores Cuantitativos
- **Constructores incompatibles**: 1 de 3 clases (33% violación)
- **Métodos con comportamiento opuesto**: 1 método (`sacar_valor`)
- **Uso de `isinstance` requerido**: En 100% de casos polimórficos
- **Factory patterns rotos**: Requiere lógica especial para SenialCola

#### Indicadores Cualitativos
- **Principio de menor sorpresa**: VIOLADO
- **Intercambiabilidad**: NULA
- **Polimorfismo funcional**: ROTO
- **Mantenibilidad**: COMPROMETIDA

---

## 📊 Impacto de las Violaciones en el Sistema

### 1. Código Cliente Comprometido

#### Anti-patrones Forzados
```python
# ❌ CÓDIGO CLIENTE FORZADO a violar principios por LSP roto
def manejar_cualquier_senial(senial):
    """Cliente obligado a usar anti-patrones"""

    # Anti-patrón 1: isinstance checking
    if isinstance(senial, SenialCola):
        # Manejo especial porque constructor es incompatible
        pass

    # Anti-patrón 2: hasattr checking
    if hasattr(senial, 'sacar_valor'):
        valor = senial.sacar_valor()
        # ¿Pero qué valor? ¿LIFO o FIFO?

    # Anti-patrón 3: Try/catch para manejar diferencias
    try:
        senial.obtener_valor(0)
    except:
        # Fallback porque puede no funcionar
        pass
```

#### Testing Comprometido
```python
# ❌ TESTS FORZADOS a ser específicos por tipo
class TestSeñalesComprometido:
    def test_senial_lista(self):
        # Test específico para lista
        pass

    def test_senial_pila(self):
        # Test específico para pila - NO reutilizable
        pass

    def test_senial_cola(self):
        # Test específico para cola - NO reutilizable
        pass

    # ❌ NO HAY test genérico que funcione con todas
```

### 2. Extensibilidad Comprometida

#### Dificultad para Agregar Nuevos Tipos
```python
# ❌ Agregar SenialDeque requiere decisiones sobre:
class SenialDeque(Senial):
    def __init__(self, tamanio=None):  # ¿Opcional u obligatorio?
        # ¿Seguir patrón inconsistente existente?

    def sacar_valor(self):
        # ¿LIFO, FIFO, o ambos extremos?
        # ¡No hay contrato claro!
        pass
```

### 3. Mantenibilidad Reducida

#### Cambios Ripple Effect
- Cambio en `Senial` puede romper subclases incompatibles
- Agregar funcionalidad requiere actualizar todos los `isinstance`
- Testing debe actualizarse para cada tipo específico
- Documentación debe explicar cada comportamiento específico

---

## 🎯 Casos de Uso que Fallan

### 1. Configurador con Intercambio Dinámico

#### Escenario Problemático
```python
# ❌ FALLA: El Configurador no puede intercambiar tipos dinámicamente
def configurador_dinamico(tipo_usuario):
    """Configurador que DEBERÍA poder cambiar tipos transparentemente"""

    # Configuraciones de usuario
    configs = {
        'basico': lambda: Senial(),
        'optimizado': lambda: SenialPila(),
        'tiempo_real': lambda: SenialCola(100)  # ← Parámetro hardcodeado
    }

    senial = configs[tipo_usuario]()

    # ❌ CÓDIGO CLIENTE NO PUEDE ser genérico
    return procesar_senial_genericamente(senial)  # ← FALLA por LSP violado
```

### 2. Pipeline de Procesamiento

#### Escenario Problemático
```python
# ❌ FALLA: Pipeline no puede ser polimórfico
class PipelineProcesamiento:
    def __init__(self, tipo_senial='lista'):
        self.senial = self._crear_senial(tipo_senial)  # ← Factory inconsistente

    def procesar_secuencial(self, datos):
        """DEBERÍA funcionar igual con cualquier tipo"""
        for dato in datos:
            self.senial.poner_valor(dato)

        # ❌ ¿Cómo extraigo datos uniformemente?
        # Cada tipo requiere lógica diferente
        return self._extraer_segun_tipo()  # ← Anti-patrón por LSP violado

    def _extraer_segun_tipo(self):
        """❌ Anti-patrón necesario por violación LSP"""
        if isinstance(self.senial, SenialCola):
            return [self.senial.sacar_valor() for _ in range(self.senial._cantidad)]
        # ... más isinstance checks
```

### 3. Testing Unitario Genérico

#### Escenario Problemático
```python
# ❌ FALLA: No se pueden hacer tests genéricos
@pytest.mark.parametrize("senial_class", [Senial, SenialPila, SenialCola])
def test_comportamiento_consistente(senial_class):
    """Este test DEBERÍA pasar con todas las clases"""

    # ❌ Ya falla en la creación
    if senial_class == SenialCola:
        senial = senial_class(10)  # Constructor especial
    else:
        senial = senial_class()

    # ❌ Comportamiento inconsistente
    senial.poner_valor(1.0)
    senial.poner_valor(2.0)

    # ❌ ¿Cómo testeo uniformemente?
    # No hay operación común que funcione igual

    # El test no puede ser genérico por violación LSP
```

---

## 📚 Lecciones Didácticas

### 1. Herencia NO es solo Reutilización de Código

#### Concepto Erróneo
```python
# ❌ PENSAMIENTO INCORRECTO:
# "SenialCola hereda de Senial para reutilizar código"
class SenialCola(Senial):  # ← Herencia POR IMPLEMENTACIÓN
    # Reutilizo _valores, _cantidad, etc.
```

#### Concepto Correcto
```python
# ✅ PENSAMIENTO CORRECTO:
# "SenialCola ES-UN Senial que puede usarse polimórficamente"
# Si no es intercambiable, NO debe heredar
```

### 2. LSP es Más que Sintaxis

#### Error Común
> "Si compila y no da error, herencia está bien"

#### Realidad
> "LSP se viola en SEMÁNTICA, no sintaxis"

- Constructores diferentes ← Violación semántica
- Comportamientos opuestos ← Violación semántica
- Contratos rotos ← Violación semántica

### 3. Polimorfismo Requiere Contratos Sólidos

#### Sin LSP
```python
def usar_senial(s):
    # ❌ Debo conocer el tipo concreto
    if isinstance(s, SenialPila):
        # Lógica específica
    elif isinstance(s, SenialCola):
        # Lógica específica diferente
```

#### Con LSP
```python
def usar_senial(s):
    # ✅ Trabajo con la abstracción solamente
    s.operacion_comun()  # Funciona igual con todas
```

---

## 🔄 Preparación para Solución LSP

### Análisis de Requisitos para Solución Correcta

#### 1. Contrato Común Requerido
```python
# ✅ INTERFAZ COMÚN que todas las implementaciones deben cumplir
class IAlmacenamientoSenal(ABC):
    @abstractmethod
    def agregar_valor(self, valor: float) -> None:
        """Agregar valor a la estructura"""
        pass

    @abstractmethod
    def obtener_siguiente_valor(self) -> Optional[float]:
        """Obtener próximo valor según la estrategia específica"""
        pass

    @abstractmethod
    def esta_vacia(self) -> bool:
        """Verificar si la estructura está vacía"""
        pass

    @abstractmethod
    def obtener_tamanio(self) -> int:
        """Obtener cantidad de elementos actuales"""
        pass
```

#### 2. Estrategias Específicas
```python
# ✅ IMPLEMENTACIONES que respetan el contrato común
class AlmacenamientoLista(IAlmacenamientoSenal):
    """Estrategia de acceso secuencial"""

class AlmacenamientoPila(IAlmacenamientoSenal):
    """Estrategia LIFO - comportamiento bien definido"""

class AlmacenamientoCola(IAlmacenamientoSenal):
    """Estrategia FIFO - comportamiento bien definido"""
```

#### 3. Composición sobre Herencia
```python
# ✅ COMPOSICIÓN: Senial USA almacenamiento, no ES almacenamiento
class Senial:
    def __init__(self, almacenamiento: IAlmacenamientoSenal):
        self._almacenamiento = almacenamiento

    def poner_valor(self, valor: float):
        self._almacenamiento.agregar_valor(valor)

    def obtener_proximo_valor(self) -> Optional[float]:
        return self._almacenamiento.obtener_siguiente_valor()
```

### Beneficios de la Solución LSP Correcta

#### 1. Intercambiabilidad Verdadera
```python
# ✅ POLIMORFISMO REAL
def procesar_con_cualquier_estrategia(almacenamiento: IAlmacenamientoSenal):
    """Funciona igual con CUALQUIER implementación"""
    almacenamiento.agregar_valor(42.0)
    return almacenamiento.obtener_siguiente_valor()

# Todas funcionan igual polimórficamente
estrategias = [
    AlmacenamientoLista(),
    AlmacenamientoPila(),
    AlmacenamientoCola(100)
]
```

#### 2. Testing Genérico Funcional
```python
# ✅ TEST ÚNICO que funciona con todas las implementaciones
@pytest.mark.parametrize("almacenamiento", [
    AlmacenamientoLista(),
    AlmacenamientoPila(),
    AlmacenamientoCola(10)
])
def test_contrato_respetado(almacenamiento):
    """Test genérico que funciona con TODAS las implementaciones"""
    # Test del contrato común
    almacenamiento.agregar_valor(1.0)
    assert not almacenamiento.esta_vacia()
    assert almacenamiento.obtener_tamanio() == 1

    valor = almacenamiento.obtener_siguiente_valor()
    assert valor == 1.0
    assert almacenamiento.esta_vacia()
```

#### 3. Factory Pattern Consistente
```python
# ✅ FACTORY que funciona uniformemente
def crear_almacenamiento(tipo: str, tamanio: int = 0) -> IAlmacenamientoSenal:
    """Factory consistente - mismo signature para todos"""
    factories = {
        'lista': lambda: AlmacenamientoLista(),
        'pila': lambda: AlmacenamientoPila(),
        'cola': lambda: AlmacenamientoCola(tamanio or 100)
    }
    return factories[tipo]()
```

---

## 🎯 Conclusiones y Próximos Pasos

### Diagnóstico Final

La implementación actual presenta **violaciones graves y múltiples** del Liskov Substitution Principle:

1. **Violación Estructural**: Constructores incompatibles
2. **Violación Semántica**: Comportamientos opuestos
3. **Violación de Contratos**: Postcondiciones inconsistentes
4. **Violación de Interfaz**: Métodos no polimórficos

### Impacto Educativo

Esta implementación es **didácticamente valiosa** porque:
- ✅ Demuestra violaciones LSP **reales y medibles**
- ✅ Muestra el **impacto práctico** de las violaciones
- ✅ Prepara el terreno para **solución correcta**
- ✅ Enseña a **identificar anti-patrones**

### Recomendaciones

#### Inmediato
1. **Documentar experimentos**: Cambiar `Configurador.crear_senial()` para mostrar violaciones
2. **Crear tests de violación**: Demostrar fallos polimórficos
3. **Medir impacto**: Cuantificar problemas en código cliente

#### Próxima Fase
1. **Diseñar solución LSP**: Interfaces apropiadas con Strategy Pattern
2. **Implementar contratos robustos**: Abstracciones verdaderamente intercambiables
3. **Refactorizar hacia composición**: Eliminar herencia problemática
4. **Validar con tests polimórficos**: Garantizar intercambiabilidad real

### Estado del Proyecto

**Fase Actual**: Violaciones LSP identificadas y documentadas ✅
**Próxima Fase**: Diseño e implementación de solución LSP correcta 🔄
**Objetivo**: Demostración completa de LSP violado → LSP aplicado correctamente

---

## 📚 Referencias Técnicas

### Bibliografía Especializada
- **Liskov, Barbara** - "Data Abstraction and Hierarchy" (OOPSLA '87)
- **Martin, Robert C.** - "Clean Architecture" (Capítulo sobre LSP)
- **Meyer, Bertrand** - "Object-Oriented Software Construction" (Principios de herencia)
- **Gamma et al.** - "Design Patterns" (Strategy Pattern como alternativa)

### Casos de Estudio Similares
- **Rectangle/Square Problem** - Ejemplo clásico de violación LSP
- **Bird/Penguin Problem** - Herencia vs. comportamiento
- **Collection Hierarchies** - Java Collections violaciones históricas
- **Streaming APIs** - Contratos de comportamiento en I/O

### Patrones de Solución
- **Strategy Pattern** - Para comportamientos intercambiables
- **Composition over Inheritance** - Evitar herencia problemática
- **Interface Segregation** - Contratos específicos y cohesivos
- **Dependency Inversion** - Abstracciones estables

---

**Documento técnico completado**
**Estado**: Violaciones LSP identificadas y analizadas completamente
**Próximo objetivo**: Implementación de solución LSP correcta con Strategy Pattern