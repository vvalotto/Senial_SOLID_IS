# Lanzador - Orquestador del Sistema

**Versión**: 6.0.0
**Patrón**: Orquestador/Coordinador
**Responsabilidad**: Orquestar flujo de procesamiento de señales (auditoría automática interna)

## 📋 Descripción

Este paquete implementa la **responsabilidad de orquestación** en la arquitectura de procesamiento de señales, siguiendo los principios SOLID y Clean Architecture. Se encarga de coordinar el flujo completo del sistema integrando todos los componentes.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en el flujo de orquestación del sistema completo.

### ✅ Lo que SÍ hace:
- Orquestar flujo: Adquisición → Procesamiento → Persistencia → Visualización
- Coordinar interacción entre componentes
- Mostrar progreso y resultados del procesamiento

### ❌ Lo que NO hace:
- Decidir QUÉ adquisidor usar (→ Configurador)
- Decidir QUÉ procesador usar (→ Configurador)
- Contener lógica de negocio (→ Componentes específicos)
- Implementar persistencia (→ Repositorio/Contexto)

## 🏗️ Arquitectura - Versión 5.2

```
┌─────────────────────────────────────────────────────────────┐
│                         LANZADOR                            │
│                  (Orquestador - SRP Puro)                   │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │ Adquisidor  │  │ Procesador  │  │  Visualizador    │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────┐       │
│  │           PATRÓN REPOSITORY (v5.2)              │       │
│  │  ┌──────────────────┐  ┌──────────────────┐    │       │
│  │  │ Repositorio      │  │ Repositorio      │    │       │
│  │  │ Adquisición      │  │ Procesamiento    │    │       │
│  │  └──────────────────┘  └──────────────────┘    │       │
│  │          ▼                      ▼               │       │
│  │  ┌──────────────────┐  ┌──────────────────┐    │       │
│  │  │ ContextoArchivo  │  │ ContextoPickle   │    │       │
│  │  │ (texto .dat)     │  │ (binario .pickle)│    │       │
│  │  └──────────────────┘  └──────────────────┘    │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
│              ▲                                              │
│              │  Delegación (Factory Pattern)               │
│              │                                              │
│  ┌───────────┴──────────────────────────────────────┐      │
│  │              CONFIGURADOR                         │      │
│  │  - crear_adquisidor()                             │      │
│  │  - crear_procesador()                             │      │
│  │  - crear_visualizador()                           │      │
│  │  - crear_repositorio_adquisicion()                │      │
│  │  - crear_repositorio_procesamiento()              │      │
│  └───────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Contenido

### Estructura del Paquete

```
lanzador/
├── __init__.py          # Exporta la clase Lanzador y función ejecutar
├── lanzador.py          # Módulo con la clase Lanzador
├── setup.py            # Configuración del paquete
└── README.md           # Este archivo
```

### Clase Principal

**`Lanzador`** (en `lanzador.py`): Orquestador que coordina:
1. Adquisición de señales
2. Procesamiento de señales
3. Persistencia con Patrón Repository (v5.2+)
4. Recuperación desde repositorios
5. Visualización de resultados

## 🚀 Instalación

```bash
pip install lanzador
```

## 💻 Uso

### Como Script de Consola

```bash
# Ejecutar lanzador con configuración por defecto
lanzador
```

### Como Módulo Python

```python
from lanzador import Lanzador

# Ejecutar flujo completo
Lanzador.ejecutar()
```

## 📊 Flujo de Ejecución (v6.0.0)

### Paso 1: Adquisición
```python
# Obtener adquisidor configurado
adquisidor = Configurador.crear_adquisidor()
repo_adquisicion = Configurador.crear_repositorio_adquisicion()

# Adquirir señal
adquisidor.leer_senial()
senial_original = adquisidor.obtener_senial_adquirida()

# Persistir con API de dominio
senial_original.id = 1000
repo_adquisicion.guardar(senial_original)  # Repository Pattern

# ✅ v6.0.0: Auditoría automática INTERNA
# La auditoría ocurre automáticamente dentro de guardar()
# No es necesario llamar repo_adquisicion.auditar() explícitamente
```

### Paso 2: Procesamiento
```python
# Obtener procesador configurado
procesador = Configurador.crear_procesador()
repo_procesamiento = Configurador.crear_repositorio_procesamiento()

# Procesar señal
procesador.procesar(senial_original)
senial_procesada = procesador.obtener_senial_procesada()

# Persistir con API de dominio
senial_procesada.id = 2000
repo_procesamiento.guardar(senial_procesada)  # Repository Pattern

# ✅ v6.0.0: Auditoría automática INTERNA
# La auditoría ocurre automáticamente dentro de guardar()
# No es necesario llamar repo_procesamiento.auditar() explícitamente
```

### Paso 3: Recuperación desde Repositorios (v5.2+)
```python
# Recuperar señales persistidas
senial_original_recuperada = repo_adquisicion.obtener("1000")
senial_procesada_recuperada = repo_procesamiento.obtener("2000")

# Las señales se reconstruyen automáticamente:
# - ContextoArchivo: Lee .dat + .meta y reconstruye objeto
# - ContextoPickle: Deserializa directamente desde .pickle
```

### Paso 4: Visualización
```python
# Obtener visualizador configurado
visualizador = Configurador.crear_visualizador()

# Visualizar señales recuperadas desde archivos
visualizador.mostrar_datos(senial_original_recuperada)
visualizador.mostrar_datos(senial_procesada_recuperada)
```

## ✅ Principios SOLID Demostrados

### SRP (Single Responsibility Principle)
- **Lanzador**: SOLO orquestar el flujo
- **Configurador**: SOLO crear y configurar objetos
- **Repositorio**: SOLO lógica de dominio de persistencia
- **Contexto**: SOLO implementación técnica de persistencia

### OCP (Open/Closed Principle)
- Extensible para nuevos procesadores sin modificar lanzador
- Extensible para nuevos contextos de persistencia sin modificar lanzador

### LSP (Liskov Substitution Principle)
✅ **RESUELTO**: Tipos de señal intercambiables (SenialBase aplicado)
- Cualquier subtipo de `SenialBase` funciona en el sistema
- `SenialLista`, `SenialPila`, `SenialCola` intercambiables

### ISP (Interface Segregation Principle)
✅ **CORRECTAMENTE APLICADO (v6.0.0)**: Interfaces segregadas
- `BaseRepositorio`: Solo métodos básicos (guardar, obtener)
- `BaseAuditor` (paquete supervisor): Auditoría segregada
- `BaseTrazador` (paquete supervisor): Trazabilidad segregada
- `RepositorioSenial`: Herencia múltiple (BaseAuditor + BaseTrazador + BaseRepositorio)
- `RepositorioUsuario`: Solo BaseRepositorio (sin métodos innecesarios)
- **Lanzador**: NO llama auditar() ni trazar() (auditoría automática interna)

### DIP (Dependency Inversion Principle)
✅ **APLICADO**:
- Lanzador depende de abstracciones (obtenidas vía Configurador)
- Repositorio depende de abstracción `BaseContexto`
- Contexto inyectado en repositorio vía constructor

## 🔄 Evolución del Lanzador

### v1.0 - Implementación básica
- Adquisición → Procesamiento → Visualización

### v2.0 - Factory Pattern
- Separación de creación (Configurador) y orquestación (Lanzador)

### v3.0 - OCP con Abstracciones
- Procesadores intercambiables vía polimorfismo

### v4.0 - LSP Resuelto
- `SenialBase` como abstracción común
- Tipos de señal totalmente intercambiables

### v5.0 - Persistencia con DIP
- Persistidores inyectados desde Configurador

### v5.2 - Repository Pattern
- Separación dominio (Repositorio) / infraestructura (Contexto)
- API semántica: `guardar()` / `obtener()` (dominio)
- Implementación técnica: `persistir()` / `recuperar()` (infraestructura)
- Reconstrucción automática de señales desde archivos

### v5.3 - Violación ISP (Didáctica)
- Violación ISP intencional en `BaseRepositorio`
- Llamadas explícitas a `auditar()` y `trazar()` desde Lanzador

### v6.0 - ISP Corregido (Actual)
- Interfaces segregadas: `BaseAuditor` y `BaseTrazador` (paquete supervisor)
- Auditoría automática INTERNA en repositorio
- Lanzador cumple SRP: NO llama auditar/trazar explícitamente
- TODOS los principios SOLID correctamente aplicados

## 🎯 Patrones de Diseño Aplicados

### 1. Coordinador/Orquestador
- Lanzador coordina sin tomar decisiones de configuración

### 2. Factory Pattern
- Configurador centraliza creación de objetos

### 3. Repository Pattern (v5.2+)
- Repositorio abstrae persistencia del dominio
- Contexto implementa estrategia de almacenamiento
- DIP aplicado: Repositorio(contexto)

### 4. Strategy Pattern
- `ContextoPickle` vs `ContextoArchivo`
- Intercambiables sin modificar repositorio

## 🔗 Dependencias

```python
install_requires=[
    "dominio-senial>=4.0.0",         # Entidades base (SenialBase)
    "adquisicion-senial>=2.1.0",     # Captura de datos
    "procesamiento-senial>=2.1.0",   # Transformación de señales
    "presentacion-senial>=2.0.0",    # Visualización
    "configurador>=2.3.0",           # Factory con Repository Pattern
    "persistidor-senial>=6.0.0",     # Repository + Contextos (ISP corregido)
    "supervisor>=1.0.0",             # Interfaces segregadas (BaseAuditor, BaseTrazador)
]
```

## 📚 Documentación Relacionada

- **Patrón Repository**: `docs/PATRON REPOSITORY EN PERSISTENCIA.md`
- **Solución LSP**: `docs/SOLUCION LSP CON ABSTRACCIONES.md`
- **Implementación OCP**: `docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md`
- **SRP en Paquetes**: `docs/IMPLEMETACION DE SRP EN PAQUETES.md`
- **Configurador Factory**: `docs/INCORPORACION DEL CONFIGURADOR CON FACTORY PATTERN.md`

## 📝 Ejemplo Completo

```python
#!/usr/bin/env python3
from lanzador import Lanzador

# Ejecutar sistema completo
# - Adquiere señal desde usuario
# - Procesa con algoritmo configurado
# - Persiste en repositorios (archivo + pickle)
# - Recupera desde repositorios
# - Visualiza señales recuperadas
Lanzador.ejecutar()
```

## 📋 Resumen de Cambios v6.0.0

### Agregado (v6.0.0)
- ✅ **ISP Corregido**: Interfaces segregadas (BaseAuditor, BaseTrazador en paquete supervisor)
- ✅ **Auditoría automática**: Interna al repositorio (no llamadas explícitas)
- ✅ **SRP mejorado**: Lanzador NO llama auditar() ni trazar()
- 📦 Dependencia: `supervisor>=1.0.0`

### Modificado (v6.0.0)
- 🔄 Lanzador simplificado: Eliminadas llamadas explícitas a auditar/trazar
- 🔄 Mensajes: Indica "Auditoría y trazabilidad: Registradas automáticamente"
- 🔄 Resumen SOLID: ISP marcado como ✅ (antes ❌)

### Agregado (v5.3.0)
- 📝 Auditoría y trazabilidad: Llamadas a `auditar()` y `trazar()` para señales (ahora removidas)
- 📄 Generación de archivos `auditor_senial.log` y `logger_senial.log`
- ⚠️ Violación ISP intencional: `BaseRepositorio` con interfaz "gorda" (ahora corregida)

### Agregado (v5.2.0)
- ✅ Patrón Repository para persistencia
- ✅ Recuperación desde repositorios antes de visualizar
- ✅ API semántica de dominio (`guardar()` / `obtener()`)
- ✅ Reconstrucción automática de señales

### Estado Actual
- ✅ **SRP**: Lanzador con responsabilidad única (orquestar)
- ✅ **OCP**: Extensible sin modificación
- ✅ **LSP**: Tipos de señal totalmente intercambiables
- ✅ **ISP**: Interfaces segregadas (v6.0.0)
- ✅ **DIP**: Dependencias inyectadas vía Configurador

---

**📖 Paquete Didáctico - Victor Valotto**
**🎯 Objetivo**: Demostración completa de principios SOLID
**🔄 Estado v6.0.0**: TODOS los principios SOLID correctamente aplicados
