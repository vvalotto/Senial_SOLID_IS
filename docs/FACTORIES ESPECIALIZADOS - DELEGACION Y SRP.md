# FACTORIES ESPECIALIZADOS - Delegación y SRP Aplicado

**Proyecto**: Senial SOLID IS
**Autor**: Victor Valotto
**Fecha**: Octubre 2024
**Versión**: 3.0.0
**Objetivo**: Documentar la implementación de Factories especializados como patrón de delegación para lograr SRP estricto en el Configurador

---

## 📋 Resumen Ejecutivo

Este documento presenta la **arquitectura de Factories especializados** implementada en la versión 3.0.0 del sistema de procesamiento de señales. Los Factories son componentes clave que permiten **delegar la responsabilidad de creación** desde el Configurador hacia módulos especializados, logrando **SRP (Single Responsibility Principle)** estricto y eliminando redundancia.

### 🎯 **Problema Resuelto**

Transformar un Configurador con **21+ métodos redundantes** en un **orquestador simple de 8 métodos** que delega la lógica de creación a **4 Factories especializados**, cada uno con responsabilidad única.

### ✅ **Resultado**

```
Antes: Configurador con 21+ métodos específicos
Después: Configurador con 8 métodos + 4 Factories especializados

Reducción: 62% menos métodos
SRP: Perfectamente aplicado
OCP: Extensibilidad mejorada
DIP: Delegación completa
```

---

## 🎯 El Problema: Configurador Sobrecargado

### Configurador v2.2 - Antipatrón

```python
# ❌ PROBLEMA: Configurador con responsabilidades mezcladas
class Configurador:
    # ❌ Métodos redundantes para señales
    @staticmethod
    def crear_senial_lista(tamanio):
        return SenialLista(tamanio)

    @staticmethod
    def crear_senial_pila(tamanio):
        return SenialPila(tamanio)

    @staticmethod
    def crear_senial_cola(tamanio):
        return SenialCola(tamanio)

    # ❌ Métodos redundantes para adquisidores
    @staticmethod
    def crear_adquisidor_consola(num_muestras, senial):
        return AdquisidorConsola(num_muestras, senial)

    @staticmethod
    def crear_adquisidor_archivo(ruta, senial):
        return AdquisidorArchivo(ruta, senial)

    @staticmethod
    def crear_adquisidor_senoidal(num_muestras, senial):
        return AdquisidorSenoidal(num_muestras, senial)

    # ❌ Métodos redundantes para procesadores
    @staticmethod
    def crear_procesador_amplificador(factor, senial):
        return ProcesadorAmplificador(factor, senial)

    @staticmethod
    def crear_procesador_umbral(umbral, senial):
        return ProcesadorUmbral(umbral, senial)

    # ❌ Métodos redundantes para contextos
    @staticmethod
    def crear_contexto_pickle(recurso):
        return ContextoPickle(recurso)

    @staticmethod
    def crear_contexto_archivo(recurso):
        return ContextoArchivo(recurso)

    # ... y muchos más métodos
```

### Problemas Identificados

#### ❌ **Violación de SRP**

**Razones para cambiar el Configurador:**
1. Agregar nuevo tipo de señal → Modificar Configurador
2. Agregar nuevo tipo de adquisidor → Modificar Configurador
3. Agregar nuevo tipo de procesador → Modificar Configurador
4. Agregar nuevo tipo de contexto → Modificar Configurador
5. Cambiar lógica de configuración JSON → Modificar Configurador

**Resultado:** Configurador tiene **5+ razones para cambiar** (violación grave de SRP)

#### ❌ **Redundancia Masiva**

```python
# Patrón repetitivo en TODOS los métodos:
@staticmethod
def crear_TIPO_VARIANTE(parametros):
    return ClaseConcreta(parametros)  # ← Siempre la misma estructura
```

**Problema:** 21+ métodos con la misma estructura básica

#### ❌ **Violación de Pylint**

```
too-many-public-methods: Configurador tiene 21 métodos públicos (límite 20)
```

#### ❌ **Baja Escalabilidad**

```
Agregar 1 nuevo tipo de señal:
- ❌ Agregar método específico en Configurador
- ❌ Incrementar conteo de métodos públicos
- ❌ Duplicar estructura repetitiva
- ❌ Aumentar complejidad ciclomática
```

---

## ✅ La Solución: Factories Especializados

### Principio de Delegación

```
┌─────────────────────────────────────┐
│         CONFIGURADOR                │
│  (Orquestador - 8 métodos)          │
│  - Lee JSON                         │
│  - Delega creación a Factories      │
└──────────┬──────────────────────────┘
           │ delega a
     ┌─────┴─────┬──────────┬─────────┬──────────┐
     ▼           ▼          ▼         ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Factory │ │ Factory │ │ Factory │ │ Factory │
│ Señal   │ │Adquisidor│ │Procesador│ │Contexto │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
     │           │          │         │
     └───────────┴──────────┴─────────┘
                  │ crean
           ┌──────▼──────┐
           │   Objetos   │
           │  Concretos  │
           └─────────────┘
```

### Configurador v3.0 - Patrón Factory

```python
# ✅ SOLUCIÓN: Configurador delega a Factories
class Configurador:
    _cargador = None  # Singleton CargadorConfig

    @staticmethod
    def inicializar_configuracion(ruta_config: str = None):
        """Inicializa configuración desde JSON"""
        Configurador._cargador = CargadorConfig(ruta_config)
        Configurador._cargador.cargar()

    @staticmethod
    def crear_senial_adquisidor():
        """🏭 Crea señal para adquisición (delega a FactorySenial)"""
        config = Configurador._cargador.obtener_config_senial_adquisidor()
        tipo = config.get('tipo', 'lista')
        return FactorySenial.crear(tipo, config)  # ← DELEGACIÓN

    @staticmethod
    def crear_adquisidor():
        """🏭 Crea adquisidor (delega a FactoryAdquisidor)"""
        config = Configurador._cargador.obtener_config_adquisidor()
        tipo = config.get('tipo', 'archivo')
        senial = Configurador.crear_senial_adquisidor()
        return FactoryAdquisidor.crear(tipo, config, senial)  # ← DELEGACIÓN

    @staticmethod
    def crear_procesador():
        """🏭 Crea procesador (delega a FactoryProcesador)"""
        config = Configurador._cargador.obtener_config_procesador()
        tipo = config.get('tipo', 'amplificador')
        senial = Configurador.crear_senial_procesador()
        return FactoryProcesador.crear(tipo, config, senial)  # ← DELEGACIÓN

    @staticmethod
    def crear_repositorio_adquisicion():
        """🏭 Crea repositorio (delega a FactoryContexto)"""
        config = Configurador._cargador.obtener_config_contexto_adquisicion()
        tipo = config.get('tipo', 'pickle')
        ctx = FactoryContexto.crear(tipo, config)  # ← DELEGACIÓN
        return RepositorioSenial(ctx)

    # ... Total: 8 métodos (vs 21+ antes)
```

---

## 🏭 Los 4 Factories Especializados

### 1. FactorySenial

**Ubicación:** `dominio_senial/factory_senial.py`

**Responsabilidad Única:** Crear señales según tipo y configuración

```python
"""
Factory especializado para crear señales.

SRP: SOLO crear señales según tipo
OCP: Extensible para nuevos tipos de señal
"""
from typing import Dict, Any
from dominio_senial.senial_base import SenialBase
from dominio_senial.senial_lista import SenialLista
from dominio_senial.senial_pila import SenialPila
from dominio_senial.senial_cola import SenialCola


class FactorySenial:
    """
    Factory para creación de señales polimórficas.

    ✅ SRP: Responsabilidad única - crear señales
    ✅ OCP: Extensible agregando nuevos tipos aquí
    ✅ LSP: Todas las señales cumplen protocolo SenialBase
    """

    @staticmethod
    def crear(tipo: str, config: Dict[str, Any]) -> SenialBase:
        """
        Crea una señal según el tipo especificado.

        :param tipo: Tipo de señal ('lista', 'pila', 'cola')
        :param config: Diccionario con configuración (tamanio, etc.)
        :return: Instancia de señal concreta
        :raises ValueError: Si el tipo es desconocido
        """
        tamanio = config.get('tamanio', 10)

        if tipo == 'lista':
            return SenialLista(tamanio)
        elif tipo == 'pila':
            return SenialPila(tamanio)
        elif tipo == 'cola':
            return SenialCola(tamanio)
        else:
            raise ValueError(
                f"Tipo de señal desconocido: '{tipo}'. "
                f"Valores válidos: 'lista', 'pila', 'cola'"
            )
```

**Características:**
- ✅ SRP: Solo crear señales
- ✅ OCP: Agregar tipo → Modificar solo este archivo
- ✅ Validación: ValueError para tipos desconocidos
- ✅ Fallback: `tamanio` default = 10

**Extensión (OCP):**

```python
# Agregar nuevo tipo: SenialDeque
elif tipo == 'deque':
    from dominio_senial.senial_deque import SenialDeque
    return SenialDeque(tamanio)
# ← Configurador NO se modifica, solo este Factory
```

---

### 2. FactoryAdquisidor

**Ubicación:** `adquisicion_senial/factory_adquisidor.py`

**Responsabilidad Única:** Crear adquisidores con señal inyectada

```python
"""
Factory especializado para crear adquisidores.

SRP: SOLO crear adquisidores según tipo
DIP: Recibe señal inyectada (abstracción)
"""
from typing import Dict, Any
from adquisicion_senial.adquisidor_consola import AdquisidorConsola
from adquisicion_senial.adquisidor_archivo import AdquisidorArchivo
from adquisicion_senial.adquisidor_senoidal import AdquisidorSenoidal


class FactoryAdquisidor:
    """
    Factory para creación de adquisidores polimórficos.

    ✅ SRP: Responsabilidad única - crear adquisidores
    ✅ OCP: Extensible agregando nuevos tipos aquí
    ✅ DIP: Recibe señal como abstracción (SenialBase)
    """

    @staticmethod
    def crear(tipo: str, config: Dict[str, Any], senial):
        """
        Crea un adquisidor según el tipo especificado.

        :param tipo: Tipo de adquisidor ('consola', 'archivo', 'senoidal')
        :param config: Diccionario con configuración
        :param senial: Señal inyectada (SenialBase)
        :return: Instancia de adquisidor concreto
        :raises ValueError: Si el tipo es desconocido
        """
        if tipo == 'consola':
            num_muestras = config.get('num_muestras', 5)
            return AdquisidorConsola(num_muestras, senial)

        elif tipo == 'archivo':
            ruta = config.get('ruta_archivo', 'senial.txt')
            return AdquisidorArchivo(ruta, senial)

        elif tipo == 'senoidal':
            num_muestras = config.get('num_muestras', 10)
            return AdquisidorSenoidal(num_muestras, senial)

        else:
            raise ValueError(
                f"Tipo de adquisidor desconocido: '{tipo}'. "
                f"Valores válidos: 'consola', 'archivo', 'senoidal'"
            )
```

**Características:**
- ✅ SRP: Solo crear adquisidores
- ✅ DIP: Señal inyectada (abstracción)
- ✅ Validación: ValueError para tipos desconocidos
- ✅ Fallbacks: Valores default para cada tipo

**Extensión (OCP):**

```python
# Agregar nuevo tipo: AdquisidorRandom
elif tipo == 'random':
    from adquisicion_senial.adquisidor_random import AdquisidorRandom
    min_val = config.get('min', 0)
    max_val = config.get('max', 100)
    num_muestras = config.get('num_muestras', 10)
    return AdquisidorRandom(min_val, max_val, num_muestras, senial)
```

---

### 3. FactoryProcesador

**Ubicación:** `procesamiento_senial/factory_procesador.py`

**Responsabilidad Única:** Crear procesadores con señal inyectada

```python
"""
Factory especializado para crear procesadores.

SRP: SOLO crear procesadores según tipo
DIP: Recibe señal inyectada (abstracción)
"""
from typing import Dict, Any
from procesamiento_senial.procesador_amplificador import ProcesadorAmplificador
from procesamiento_senial.procesador_umbral import ProcesadorUmbral


class FactoryProcesador:
    """
    Factory para creación de procesadores polimórficos.

    ✅ SRP: Responsabilidad única - crear procesadores
    ✅ OCP: Extensible agregando nuevos tipos aquí
    ✅ DIP: Recibe señal como abstracción (SenialBase)
    """

    @staticmethod
    def crear(tipo: str, config: Dict[str, Any], senial):
        """
        Crea un procesador según el tipo especificado.

        :param tipo: Tipo de procesador ('amplificador', 'umbral')
        :param config: Diccionario con configuración
        :param senial: Señal procesada inyectada (SenialBase)
        :return: Instancia de procesador concreto
        :raises ValueError: Si el tipo es desconocido
        """
        if tipo == 'amplificador':
            factor = config.get('factor', 4.0)
            return ProcesadorAmplificador(factor, senial)

        elif tipo == 'umbral':
            umbral = config.get('umbral', 100)
            return ProcesadorUmbral(umbral, senial)

        else:
            raise ValueError(
                f"Tipo de procesador desconocido: '{tipo}'. "
                f"Valores válidos: 'amplificador', 'umbral'"
            )
```

**Características:**
- ✅ SRP: Solo crear procesadores
- ✅ DIP: Señal inyectada (abstracción)
- ✅ Validación: ValueError para tipos desconocidos
- ✅ Fallbacks: `factor=4.0`, `umbral=100`

**Extensión (OCP):**

```python
# Agregar nuevo tipo: ProcesadorFiltro
elif tipo == 'filtro':
    from procesamiento_senial.procesador_filtro import ProcesadorFiltro
    frecuencia_corte = config.get('frecuencia_corte', 50)
    return ProcesadorFiltro(frecuencia_corte, senial)
```

---

### 4. FactoryContexto

**Ubicación:** `persistidor_senial/factory_contexto.py`

**Responsabilidad Única:** Crear contextos de persistencia

```python
"""
Factory especializado para crear contextos de persistencia.

SRP: SOLO crear contextos según tipo
Strategy Pattern: Diferentes estrategias de persistencia
"""
from typing import Dict, Any
from persistidor_senial.contexto_pickle import ContextoPickle
from persistidor_senial.contexto_archivo import ContextoArchivo


class FactoryContexto:
    """
    Factory para creación de contextos de persistencia.

    ✅ SRP: Responsabilidad única - crear contextos
    ✅ OCP: Extensible agregando nuevas estrategias
    ✅ Strategy Pattern: ContextoPickle vs ContextoArchivo
    """

    @staticmethod
    def crear(tipo: str, config: Dict[str, Any]):
        """
        Crea un contexto de persistencia según el tipo.

        :param tipo: Tipo de contexto ('pickle', 'archivo')
        :param config: Diccionario con configuración (recurso, etc.)
        :return: Instancia de contexto concreto
        :raises ValueError: Si el tipo es desconocido
        """
        recurso = config.get('recurso', './datos_persistidos')

        if tipo == 'pickle':
            return ContextoPickle(recurso)

        elif tipo == 'archivo':
            return ContextoArchivo(recurso)

        else:
            raise ValueError(
                f"Tipo de contexto desconocido: '{tipo}'. "
                f"Valores válidos: 'pickle', 'archivo'"
            )
```

**Características:**
- ✅ SRP: Solo crear contextos
- ✅ Strategy Pattern: Estrategias intercambiables
- ✅ Validación: ValueError para tipos desconocidos
- ✅ Fallback: `recurso='./datos_persistidos'`

**Extensión (OCP):**

```python
# Agregar nuevo tipo: ContextoJSON
elif tipo == 'json':
    from persistidor_senial.contexto_json import ContextoJSON
    return ContextoJSON(recurso)

# Agregar nuevo tipo: ContextoSQLite
elif tipo == 'sqlite':
    from persistidor_senial.contexto_sqlite import ContextoSQLite
    db_path = config.get('db_path', 'senial.db')
    return ContextoSQLite(db_path)
```

---

## 📊 Comparativa de Arquitecturas

### Tabla Comparativa

| Aspecto | v2.2 (Sin Factories) | v3.0 (Con Factories) |
|---------|---------------------|---------------------|
| **Métodos Configurador** | 21+ métodos | 8 métodos |
| **Lógica de creación** | En Configurador | En Factories |
| **SRP Configurador** | ❌ Violado | ✅ Cumplido |
| **SRP Factories** | N/A | ✅ Cumplido |
| **Redundancia** | Alta | Eliminada |
| **Extensibilidad** | Modificar Configurador | Modificar Factory |
| **Testing** | Complejo | Simple |
| **Mantenibilidad** | Baja | Alta |
| **Escalabilidad** | Limitada | Alta |

### Métricas de Código

```
CONFIGURADOR v2.2:
- Métodos públicos: 21+
- Líneas de código: ~600
- Complejidad ciclomática: Alta
- Dependencias: Todas las clases concretas
- Razones para cambiar: 5+

CONFIGURADOR v3.0:
- Métodos públicos: 8
- Líneas de código: ~200
- Complejidad ciclomática: Baja
- Dependencias: 4 Factories + CargadorConfig
- Razones para cambiar: 1 (cambios en orquestación JSON)

FACTORIES (4 archivos):
- Métodos públicos por Factory: 1 (crear)
- Líneas de código total: ~300
- Complejidad ciclomática: Baja
- Dependencias: Clases concretas de su dominio
- Razones para cambiar: 1 por Factory (nuevos tipos)
```

---

## 🎯 Principios SOLID en Factories

### SRP (Single Responsibility Principle)

✅ **Cada Factory tiene UNA responsabilidad:**

| Factory | Responsabilidad |
|---------|----------------|
| `FactorySenial` | Crear señales |
| `FactoryAdquisidor` | Crear adquisidores |
| `FactoryProcesador` | Crear procesadores |
| `FactoryContexto` | Crear contextos |

### OCP (Open/Closed Principle)

✅ **Extensible sin modificar Configurador:**

```python
# Agregar nuevo tipo de señal:
# 1. Modificar SOLO FactorySenial (agregar elif)
# 2. Configurador NO se toca
# 3. Lanzador NO se toca
# 4. Otros Factories NO se tocan

# FactorySenial.crear()
elif tipo == 'deque':
    return SenialDeque(tamanio)  # ← Una línea en Factory
```

### LSP (Liskov Substitution Principle)

✅ **Objetos creados son intercambiables:**

```python
# Todos los adquisidores cumplen el mismo protocolo
adq1 = FactoryAdquisidor.crear('consola', config, senial)
adq2 = FactoryAdquisidor.crear('archivo', config, senial)
adq3 = FactoryAdquisidor.crear('senoidal', config, senial)

# Todos funcionan polimórficamente
adq1.leer_senial()
adq2.leer_senial()  # ← Mismo método
adq3.leer_senial()
```

### ISP (Interface Segregation Principle)

✅ **Factories NO dependen de interfaces innecesarias:**

```python
# FactorySenial solo conoce:
# - SenialBase (protocolo)
# - Clases concretas de señales
# NO conoce: Adquisidores, Procesadores, Contextos

# FactoryAdquisidor solo conoce:
# - Clases concretas de adquisidores
# NO conoce: Señales (recibe inyectadas), Procesadores, Contextos
```

### DIP (Dependency Inversion Principle)

✅ **Factories reciben abstracciones:**

```python
# FactoryAdquisidor.crear(tipo, config, senial)
#                                      ↑
#                              SenialBase (abstracción)

# NO conoce si es SenialLista, SenialPila, o SenialCola
# Solo conoce que cumple el protocolo SenialBase
```

---

## 🧪 Testing de Factories

### Ventajas de Testear Factories

1. **Aislamiento**: Testear creación sin testear orquestación
2. **Rapidez**: Tests unitarios sin dependencias complejas
3. **Cobertura**: Cada Factory testeado independientemente
4. **Validación**: Verificar tipos desconocidos lanzan ValueError

### Ejemplo: Test de FactorySenial

```python
import pytest
from dominio_senial import FactorySenial
from dominio_senial.senial_lista import SenialLista
from dominio_senial.senial_pila import SenialPila
from dominio_senial.senial_cola import SenialCola


def test_factory_senial_crea_lista():
    config = {'tamanio': 20}
    senial = FactorySenial.crear('lista', config)

    assert isinstance(senial, SenialLista)
    assert senial.obtener_tamanio() == 20


def test_factory_senial_crea_pila():
    config = {'tamanio': 15}
    senial = FactorySenial.crear('pila', config)

    assert isinstance(senial, SenialPila)
    assert senial.obtener_tamanio() == 15


def test_factory_senial_crea_cola():
    config = {'tamanio': 25}
    senial = FactorySenial.crear('cola', config)

    assert isinstance(senial, SenialCola)
    assert senial.obtener_tamanio() == 25


def test_factory_senial_fallback_tamanio():
    config = {}  # Sin tamanio especificado
    senial = FactorySenial.crear('lista', config)

    assert senial.obtener_tamanio() == 10  # Default


def test_factory_senial_tipo_desconocido():
    config = {'tamanio': 20}

    with pytest.raises(ValueError) as excinfo:
        FactorySenial.crear('arbol', config)

    assert "Tipo de señal desconocido: 'arbol'" in str(excinfo.value)
```

### Ejemplo: Test de FactoryContexto

```python
import pytest
from persistidor_senial import FactoryContexto
from persistidor_senial.contexto_pickle import ContextoPickle
from persistidor_senial.contexto_archivo import ContextoArchivo


def test_factory_contexto_crea_pickle():
    config = {'recurso': './tmp/test'}
    contexto = FactoryContexto.crear('pickle', config)

    assert isinstance(contexto, ContextoPickle)


def test_factory_contexto_crea_archivo():
    config = {'recurso': './tmp/test'}
    contexto = FactoryContexto.crear('archivo', config)

    assert isinstance(contexto, ContextoArchivo)


def test_factory_contexto_tipo_desconocido():
    config = {'recurso': './tmp/test'}

    with pytest.raises(ValueError) as excinfo:
        FactoryContexto.crear('mongodb', config)

    assert "Tipo de contexto desconocido: 'mongodb'" in str(excinfo.value)
```

---

## 📚 Lecciones Aprendidas

### ✅ **Hacer (Best Practices)**

1. **Factory por Dominio**: Un Factory por cada dominio lógico (señales, adquisidores, etc.)
2. **Método Único**: Un solo método público `crear()` por Factory
3. **Validación**: Lanzar `ValueError` para tipos desconocidos
4. **Fallbacks**: Valores default para parámetros opcionales
5. **Documentación**: Docstrings claros con tipos válidos
6. **Testing**: Tests unitarios para cada Factory
7. **OCP**: Agregar tipo → Modificar solo el Factory correspondiente
8. **SRP**: Factory NO debe orquestar, solo crear

### ❌ **Evitar (Anti-Patterns)**

1. **Factory Gigante**: No crear un solo Factory para todos los dominios
2. **Múltiples Métodos**: No crear métodos específicos (crear_lista, crear_pila, etc.)
3. **Lógica Compleja**: Factory NO debe contener lógica de negocio
4. **Acoplamiento**: Factory NO debe conocer otros Factories
5. **Orquestación**: Factory NO debe coordinar flujos
6. **Hardcoding**: No hardcodear valores, usar config
7. **Sin Validación**: Siempre validar tipos y lanzar excepciones claras

---

## 🔮 Evolución Futura

### Registry Pattern

```python
# Registro dinámico de tipos
class FactorySenial:
    _registry = {
        'lista': SenialLista,
        'pila': SenialPila,
        'cola': SenialCola,
    }

    @classmethod
    def registrar(cls, tipo: str, clase):
        """Permite registrar nuevos tipos dinámicamente"""
        cls._registry[tipo] = clase

    @classmethod
    def crear(cls, tipo: str, config: Dict[str, Any]):
        if tipo not in cls._registry:
            raise ValueError(f"Tipo desconocido: {tipo}")

        clase = cls._registry[tipo]
        tamanio = config.get('tamanio', 10)
        return clase(tamanio)

# Uso externo (plugin)
from mi_extension import SenialDeque
FactorySenial.registrar('deque', SenialDeque)
```

### Abstract Factory

```python
# Factory de Factories
class AbstractFactory:
    @staticmethod
    def get_factory(dominio: str):
        if dominio == 'senial':
            return FactorySenial
        elif dominio == 'adquisidor':
            return FactoryAdquisidor
        # ...

# Uso
factory = AbstractFactory.get_factory('senial')
senial = factory.crear('lista', {'tamanio': 20})
```

---

## 📖 Conclusión

La implementación de **Factories especializados** es un componente fundamental de la arquitectura DIP del sistema. Estos Factories permiten:

1. ✅ **SRP Estricto**: Cada Factory tiene responsabilidad única
2. ✅ **Eliminación de Redundancia**: De 21+ métodos a 4 Factories
3. ✅ **OCP Mejorado**: Extensibilidad sin modificar Configurador
4. ✅ **Testabilidad**: Cada Factory testeado independientemente
5. ✅ **Mantenibilidad**: Código organizado por dominio
6. ✅ **Delegación Completa**: Configurador delega, no implementa

**Los Factories no son solo un patrón de creación - son la clave para lograr SRP estricto y OCP efectivo en sistemas complejos con múltiples tipos y variantes.**

---

**📖 Documento Técnico - Factories Especializados**
**Victor Valotto - Octubre 2024**
**v3.0.0 - Delegación y SRP Aplicado**
