# PATRÓN REPOSITORY EN PERSISTENCIA - Arquitectura en Capas

**Proyecto**: Senial SOLID IS
**Autor**: Victor Valotto
**Fecha**: Octubre 2024
**Versión**: 5.2.0
**Objetivo**: Documentar la implementación del patrón Repository para abstracción de persistencia, separando responsabilidades de dominio e infraestructura

---

## 📋 Resumen Ejecutivo

Este documento presenta la **arquitectura en capas** del paquete `persistidor_senial`, que implementa el **patrón Repository** combinado con el **patrón Strategy** para separar completamente las responsabilidades de **QUÉ se persiste** (dominio) y **CÓMO se persiste** (infraestructura).

### 🎯 **Solución Central**

Aplicación de **Repository Pattern + Dependency Injection** mediante una arquitectura de dos capas:
- **Capa de Dominio**: `BaseRepositorio` y sus implementaciones (RepositorioSenial, RepositorioUsuario)
- **Capa de Infraestructura**: `BaseContexto` y sus estrategias (ContextoPickle, ContextoArchivo)

### ⚠️ **Violación ISP Intencional**

El diseño actual contiene una **violación deliberada del Interface Segregation Principle** en `BaseContexto`, que expone tanto `persistir()` como `recuperar()` en la misma interfaz. Esta violación es **didáctica** y será corregida en iteraciones futuras.

---

## 🏗️ Arquitectura del Sistema

### Separación en Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                       │
│  (Lanzador, Configurador - Orquestación de dominio)        │
└────────────────────────┬────────────────────────────────────┘
                         │ usa
┌────────────────────────▼────────────────────────────────────┐
│                    CAPA DE DOMINIO                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ BaseRepositorio (ABC)                                 │  │
│  │  + guardar(entidad) → None                           │  │
│  │  + obtener(id, entidad?) → Any                       │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │ implementan                                 │
│       ┌───────┴────────┐                                    │
│       ▼                ▼                                    │
│  RepositorioSenial  RepositorioUsuario                      │
│  (gestión señales)  (gestión usuarios)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ depende de (DIP)
┌────────────────────────▼────────────────────────────────────┐
│              CAPA DE INFRAESTRUCTURA                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ BaseContexto (ABC) ⚠️ VIOLACIÓN ISP                   │  │
│  │  + persistir(entidad, id) → None                     │  │
│  │  + recuperar(id, entidad?) → Any                     │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │ implementan (Strategy Pattern)              │
│       ┌───────┴────────┐                                    │
│       ▼                ▼                                    │
│  ContextoPickle    ContextoArchivo                          │
│  (binario .pickle) (texto .dat)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Patrón Repository

### Definición

> **Repository**: Abstrae la lógica de acceso a datos, proporcionando una interfaz orientada a colecciones para acceder a objetos del dominio.

### Responsabilidades

#### **BaseRepositorio** (Abstracción)
```python
class BaseRepositorio(ABC):
    """
    Define la interfaz para el acceso a la persistencia de datos
    """
    def __init__(self, contexto: Any):
        self._contexto = contexto  # ← Inyección de dependencias (DIP)

    @abstractmethod
    def guardar(self, entidad: Any) -> None:
        """Persiste la entidad"""
        pass

    @abstractmethod
    def obtener(self, id_entidad: str, entidad: Any = None) -> Any:
        """Obtiene una entidad por su identificador"""
        pass
```

#### **RepositorioSenial** (Implementación)
```python
class RepositorioSenial(BaseRepositorio):
    """
    Repositorio para gestionar la persistencia de señales
    """
    def guardar(self, senial: Any) -> None:
        # Delega en el contexto (infraestructura)
        self._contexto.persistir(senial, str(senial.id))

    def obtener(self, id_senial: str, entidad: Any = None) -> Any:
        # Delega en el contexto (infraestructura)
        return self._contexto.recuperar(id_senial, entidad)
```

### Ventajas del Patrón Repository

| Ventaja | Descripción |
|---------|-------------|
| **Abstracción** | Oculta detalles de persistencia del dominio |
| **API Semántica** | `guardar()` / `obtener()` en lugar de `persistir()` / `recuperar()` |
| **Testabilidad** | Fácil crear mocks/stubs del repositorio |
| **Centralización** | Lógica de acceso a datos en un solo lugar |
| **Cambio de Estrategia** | Cambiar contexto sin modificar dominio |

---

## 🔧 Patrón Strategy (Contextos)

### Definición

> **Strategy**: Permite definir una familia de algoritmos (estrategias de persistencia), encapsularlos y hacerlos intercambiables.

### Responsabilidades

#### **BaseContexto** (Abstracción de Estrategia)
```python
class BaseContexto(ABC):
    """
    ⚠️ VIOLACIÓN ISP INTENCIONAL
    Interfaz "gorda" que fuerza implementar persistir() + recuperar()
    """
    def __init__(self, recurso: str):
        self._recurso = recurso
        if not os.path.isdir(recurso):
            os.makedirs(recurso, exist_ok=True)

    @abstractmethod
    def persistir(self, entidad: Any, id_entidad: str) -> None:
        pass

    @abstractmethod
    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        pass
```

#### **ContextoPickle** (Estrategia Binaria)
```python
class ContextoPickle(BaseContexto):
    """
    Estrategia de persistencia usando pickle (serialización binaria)
    """
    def persistir(self, entidad: Any, id_entidad: str) -> None:
        archivo = f"{id_entidad}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)
        with open(ubicacion, "wb") as f:
            pickle.dump(entidad, f, protocol=pickle.HIGHEST_PROTOCOL)

    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        archivo = f"{id_entidad}.pickle"
        ubicacion = os.path.join(self._recurso, archivo)
        with open(ubicacion, "rb") as f:
            return pickle.load(f)  # Reconstrucción automática
```

#### **ContextoArchivo** (Estrategia Texto Plano)
```python
class ContextoArchivo(BaseContexto):
    """
    Estrategia de persistencia usando archivos de texto plano
    con metadatos de tipo para reconstrucción automática
    """
    def persistir(self, entidad: Any, id_entidad: str) -> None:
        archivo = f"{id_entidad}.dat"
        ubicacion = os.path.join(self._recurso, archivo)

        # Metadato de clase para reconstrucción automática
        tipo_clase = f"__class__:{type(entidad).__module__}.{type(entidad).__name__}\n"

        mapeador = MapeadorArchivo()
        contenido = tipo_clase + mapeador.ir_a_persistidor(entidad)

        with open(ubicacion, "w", encoding="utf-8") as f:
            f.write(contenido)

    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        archivo = f"{id_entidad}.dat"
        ubicacion = os.path.join(self._recurso, archivo)

        with open(ubicacion, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        # Leer metadato de tipo
        tipo_info = lineas[0].strip().split(":", 1)[1]
        modulo_nombre, clase_nombre = tipo_info.rsplit(".", 1)

        # Reconstrucción automática usando importlib
        if entidad is None:
            modulo = importlib.import_module(modulo_nombre)
            clase = getattr(modulo, clase_nombre)
            entidad = clase()

        # Deserializar contenido
        contenido = ''.join(lineas[1:])
        mapeador = MapeadorArchivo()
        return mapeador.venir_desde_persistidor(entidad, contenido)
```

### Comparación de Estrategias

| Característica | ContextoPickle | ContextoArchivo |
|----------------|----------------|-----------------|
| **Formato** | Binario (.pickle) | Texto plano (.dat) |
| **Velocidad** | ⚡ Muy rápida | 🐢 Más lenta |
| **Legibilidad** | ❌ No human-readable | ✅ Human-readable |
| **Portabilidad** | 🐍 Solo Python | 📄 Multiplataforma |
| **Reconstrucción** | Automática (pickle) | Automática (metadatos) |
| **Uso típico** | Producción, cache | Debugging, análisis |

---

## 🔄 Dependency Inversion Principle (DIP)

### Aplicación de DIP

El patrón Repository implementa DIP mediante **inyección de dependencias**:

```python
# INCORRECTO (dependencia directa de implementación)
class RepositorioSenial:
    def __init__(self):
        self._contexto = ContextoPickle('./datos')  # ← Acoplamiento fuerte

# CORRECTO (dependencia de abstracción)
class RepositorioSenial:
    def __init__(self, contexto: BaseContexto):  # ← Inyección de abstracción
        self._contexto = contexto
```

### Diagrama de Dependencias

```
┌──────────────────┐
│ RepositorioSenial│ (Módulo de alto nivel - Dominio)
└────────┬─────────┘
         │ depende de
         ▼
┌─────────────────┐
│  BaseContexto   │ (Abstracción)
│      (ABC)      │
└────────┬────────┘
         │ implementan
    ┌────┴────┐
    ▼         ▼
ContextoPickle  ContextoArchivo  (Módulos de bajo nivel - Infra)
```

**Regla DIP cumplida**: "Los módulos de alto nivel NO deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones."

---

## ⚠️ Violación ISP (Interface Segregation Principle)

### Problema Identificado

`BaseContexto` es una **interfaz "gorda"** que viola ISP:

```python
class BaseContexto(ABC):
    @abstractmethod
    def persistir(self, entidad, id_entidad):  # ← Operación de ESCRITURA
        pass

    @abstractmethod
    def recuperar(self, id_entidad, entidad):  # ← Operación de LECTURA
        pass
```

### Consecuencias de la Violación

| Cliente | Necesita | Depende de | Problema |
|---------|----------|------------|----------|
| **Adquisidor** | Solo `persistir()` | `persistir()` + `recuperar()` | Conoce método innecesario |
| **Visualizador** | Solo `recuperar()` | `persistir()` + `recuperar()` | Conoce método innecesario |
| **Procesador** | `persistir()` (solo escribe) | `persistir()` + `recuperar()` | Conoce método innecesario |

### Solución Futura (Segregación de Interfaces)

```python
# Interfaces segregadas
class IEscritor(ABC):
    @abstractmethod
    def persistir(self, entidad, id_entidad):
        pass

class ILector(ABC):
    @abstractmethod
    def recuperar(self, id_entidad, entidad):
        pass

# Implementaciones combinan según necesidad
class ContextoPickle(IEscritor, ILector):
    # Implementa ambas interfaces
    pass

# Clientes dependen solo de lo que necesitan
class RepositorioSoloEscritura:
    def __init__(self, escritor: IEscritor):  # ← Solo escritura
        self._escritor = escritor
```

---

## 🧪 Casos de Uso

### Caso 1: Uso Básico del Repositorio

```python
from configurador import Configurador
from dominio_senial import SenialLista

# Crear repositorio (patrón Repository)
repo = Configurador.crear_repositorio_adquisicion()

# Crear y guardar señal
señal = SenialLista(10)
señal.poner_valor(1.5)
señal.poner_valor(2.8)
señal.id = 100

repo.guardar(señal)  # ← API semántica de dominio

# Recuperar señal
señal_recuperada = repo.obtener('100')  # ← Sin template (reconstrucción automática)
```

### Caso 2: Composición Manual (DIP Explícito)

```python
from configurador import Configurador

# Definir contexto (infraestructura)
ctx_adq = Configurador.definir_contexto('./datos/adquisicion', 'archivo')
ctx_proc = Configurador.definir_contexto('./datos/procesamiento', 'pickle')

# Crear repositorios con inyección de contexto (DIP)
repo_adq = Configurador.definir_repositorio(ctx_adq, 'senial')
repo_proc = Configurador.definir_repositorio(ctx_proc, 'senial')

# Usar repositorios
señal.id = 200
repo_adq.guardar(señal)    # → Guardado en archivo de texto
repo_proc.guardar(señal)   # → Guardado en pickle binario
```

### Caso 3: Cambio de Estrategia sin Modificar Dominio

```python
# Configuración inicial: Pickle
ctx = Configurador.definir_contexto('./datos', 'pickle')
repo = Configurador.definir_repositorio(ctx, 'senial')
repo.guardar(señal)  # → .pickle

# Cambio a archivo de texto (solo cambiar contexto)
ctx_nuevo = Configurador.definir_contexto('./datos', 'archivo')
repo = Configurador.definir_repositorio(ctx_nuevo, 'senial')
repo.guardar(señal)  # → .dat

# El código del dominio NO cambió (OCP aplicado)
```

---

## 📊 Flujo de Datos

### Guardar Entidad

```
┌──────────┐                 ┌──────────────────┐                ┌──────────────┐
│ Lanzador │ ──guardar()──>  │ RepositorioSenial│ ──persistir()─>│ContextoPickle│
└──────────┘                 └──────────────────┘                └──────┬───────┘
                                                                         │
                                                                         ▼
                                                                  ┌──────────────┐
                                                                  │archivo.pickle│
                                                                  └──────────────┘
```

1. **Lanzador** llama a `repo.guardar(señal)` (API de dominio)
2. **RepositorioSenial** convierte a `contexto.persistir(señal, id)` (traducción)
3. **ContextoPickle** serializa con pickle y escribe archivo
4. Archivo `.pickle` guardado en disco

### Obtener Entidad

```
┌──────────┐                 ┌──────────────────┐                ┌──────────────┐
│ Lanzador │ <──return───────│ RepositorioSenial│<──return───────│ContextoPickle│
└──────────┘                 └──────────────────┘                └──────┬───────┘
     ▲                                                                   │
     │                                                                   │
     └──obtener(id)───────────────────recuperar(id)──────────────────────┘
                                                                         │
                                                                         ▼
                                                                  ┌──────────────┐
                                                                  │archivo.pickle│
                                                                  └──────────────┘
```

1. **Lanzador** llama a `repo.obtener('100')` (API de dominio)
2. **RepositorioSenial** convierte a `contexto.recuperar(id)` (traducción)
3. **ContextoPickle** lee archivo y deserializa con pickle
4. Objeto reconstruido automáticamente retornado al lanzador

---

## 📚 Formato de Archivos

### Archivo Pickle (.pickle)

**Formato**: Binario serializado con pickle

```
(No human-readable - contenido binario)
```

**Ventajas**:
- Serialización/deserialización automática
- Alta velocidad
- Preserva estructura completa de objetos Python

### Archivo de Texto (.dat)

**Formato**: Texto plano con metadatos

```
__class__:dominio_senial.senial.SenialLista
_fecha_adquisicion:2025-10-02,_cantidad:5,_tamanio:10,_comentario:Test,_id:100,
_valores>0:10.5,
_valores>1:20.3,
_valores>2:15.7,
```

**Estructura**:
1. **Línea 1**: Metadato de tipo (`__class__:modulo.Clase`)
2. **Línea 2**: Atributos simples (formato `clave:valor,`)
3. **Líneas 3+**: Colecciones (formato `clave>índice:valor,`)

**Ventajas**:
- Human-readable (inspección directa)
- Reconstrucción automática con metadatos
- Debugging simplificado

---

## 🎯 Principios SOLID Aplicados

### ✅ SRP (Single Responsibility Principle)

| Clase | Responsabilidad Única |
|-------|----------------------|
| `BaseRepositorio` | Definir contrato de persistencia de dominio |
| `RepositorioSenial` | Gestionar persistencia de señales |
| `BaseContexto` | Definir contrato de estrategia de almacenamiento |
| `ContextoPickle` | Implementar persistencia binaria con pickle |
| `ContextoArchivo` | Implementar persistencia en texto plano |
| `MapeadorArchivo` | Serializar/deserializar objetos a texto |

### ✅ OCP (Open/Closed Principle)

**Extensible sin modificación**:
- Agregar `ContextoJSON` → Sin modificar repositorios existentes
- Agregar `RepositorioProcesamiento` → Sin modificar contextos existentes

```python
# Nueva estrategia (extensión)
class ContextoJSON(BaseContexto):
    def persistir(self, entidad, id_entidad):
        # Implementación JSON
        pass

# Usar nueva estrategia SIN modificar código existente
ctx = ContextoJSON('./datos')
repo = RepositorioSenial(ctx)  # ← Funciona sin cambios
```

### ✅ LSP (Liskov Substitution Principle)

**Todos los contextos son intercambiables**:

```python
def procesar_con_repositorio(repo: BaseRepositorio):
    señal = SenialLista()
    repo.guardar(señal)  # ← Funciona con ANY repositorio

# LSP cumplido: cualquier repositorio funciona
procesar_con_repositorio(RepositorioSenial(ContextoPickle('./datos')))
procesar_con_repositorio(RepositorioSenial(ContextoArchivo('./datos')))
```

### ⚠️ ISP (Interface Segregation Principle)

**VIOLACIÓN INTENCIONAL**: `BaseContexto` es interfaz "gorda"

**Problema**: Clientes que solo escriben deben conocer `recuperar()`

**Solución futura**: Segregar en `IEscritor` + `ILector`

### ✅ DIP (Dependency Inversion Principle)

**Inyección de dependencias aplicada**:

```python
class RepositorioSenial:
    def __init__(self, contexto: BaseContexto):  # ← Depende de abstracción
        self._contexto = contexto

# Inyección en tiempo de creación
ctx = ContextoPickle('./datos')
repo = RepositorioSenial(ctx)  # ← DIP cumplido
```

---

## 🔄 Evolución Planificada

### Versión Actual (5.2.0)

- ✅ Patrón Repository implementado
- ✅ Patrón Strategy para contextos
- ✅ DIP con inyección de dependencias
- ⚠️ Violación ISP intencional (didáctica)

### Versión Futura (6.0.0)

- 🔄 Segregar `IEscritor` + `ILector` (corrección ISP)
- 🔄 Implementar `RepositorioSoloEscritura` / `RepositorioSoloLectura`
- 🔄 Agregar `ContextoSQL` para base de datos
- 🔄 Implementar patrón Unit of Work

---

## 📖 Referencias

### Documentación Relacionada

- `docs/SOLUCION LSP CON ABSTRACCIONES.md` - LSP en jerarquía de señales
- `docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md` - OCP con procesadores
- `docs/INCORPORACION DEL CONFIGURADOR CON FACTORY PATTERN.md` - Factory Centralizado
- `docs/IMPLEMETACION DE SRP EN PAQUETES.md` - SRP a nivel de arquitectura

### Código Fuente

- `persistidor_senial/contexto.py` - Implementación de contextos
- `persistidor_senial/repositorio.py` - Implementación de repositorios
- `persistidor_senial/mapeador.py` - Serialización para archivos de texto
- `configurador/configurador.py` - Factory methods para repositorios

### Patrones de Diseño

- **Repository Pattern**: Martin Fowler - Patterns of Enterprise Application Architecture
- **Strategy Pattern**: Gang of Four - Design Patterns
- **Dependency Injection**: Mark Seemann - Dependency Injection in .NET

---

## 🎓 Lecciones Aprendidas

### ✅ Buenas Prácticas Aplicadas

1. **Separación de Responsabilidades**: Dominio (repositorio) vs Infraestructura (contexto)
2. **Inyección de Dependencias**: Contexto inyectado en repositorio
3. **API Semántica**: `guardar()` / `obtener()` en lugar de `persistir()` / `recuperar()`
4. **Reconstrucción Automática**: Metadatos de tipo en archivos de texto
5. **Extensibilidad**: Fácil agregar nuevas estrategias o entidades

### ⚠️ Deuda Técnica Identificada

1. **Violación ISP**: Interfaz "gorda" en `BaseContexto`
2. **Firma Inconsistente**: Parámetro `entidad` opcional en `recuperar()` (necesario para algunos contextos, no para otros)
3. **Acoplamiento Temporal**: Entidad debe tener atributo `id` (no hay ID generado automáticamente)

### 🔄 Mejoras Futuras

1. Segregar interfaces para escritura/lectura (corrección ISP)
2. Implementar generador automático de IDs
3. Agregar validaciones de integridad referencial
4. Implementar transacciones (Unit of Work)
5. Agregar caché de segundo nivel

---

**Fin del Documento**
