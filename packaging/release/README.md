# Principios SOLID - Caso de Estudio Avanzado

**Versión**: 6.0.0 - SOLID Completo con DIP Aplicado (Configuración Externa JSON)
**Autor**: Victor Valotto
**Objetivo**: Demostración práctica y didáctica de principios SOLID aplicados a arquitectura de software

Este proyecto es un caso de estudio didáctico que demuestra la **evolución progresiva** de un sistema de procesamiento de señales digitales aplicando principios SOLID, desde violaciones iniciales hasta arquitectura limpia con **configuración externa JSON** y **Factories especializados**.

✅ **VERSIÓN ACTUAL: v6.0.0** - Todos los principios SOLID correctamente aplicados con DIP completo.

## 🎯 Estado Actual del Proyecto

### ✅ Principios SOLID Implementados

- **✅ S** - **Single Responsibility Principle**: Aplicado a nivel de clases, paquetes, y Factories especializados
- **✅ O** - **Open/Closed Principle**: Extensibilidad sin modificación mediante Factories y configuración JSON
- **✅ L** - **Liskov Substitution Principle**: Intercambiabilidad polimórfica garantizada con SenialBase
- **✅ I** - **Interface Segregation Principle**: Interfaces segregadas (BaseAuditor, BaseTrazador en paquete supervisor)
- **✅ D** - **Dependency Inversion Principle**: **Configuración externa JSON determina TODAS las dependencias del sistema**

### 🏗️ Arquitectura Actual (v6.0.0 - DIP Completo)

```
📦 Senial_SOLID_IS/
├── 🏠 dominio_senial/          # Entidades del dominio (SenialBase + LSP + FactorySenial)
├── 📡 adquisicion_senial/      # Adquisición (OCP + FactoryAdquisidor)
├── ⚙️  procesamiento_senial/    # Procesamiento (OCP + FactoryProcesador)
├── 📊 presentacion_senial/     # Visualización
├── 💾 persistidor_senial/      # Repository Pattern (DIP + ISP + FactoryContexto)
├── 👁️  supervisor/              # Interfaces segregadas (ISP - BaseAuditor, BaseTrazador)
├── 🏭 configurador/            # Factory centralizado (SRP + DIP + JSON)
│   ├── config.json            # ⭐ Configuración externa (DIP)
│   ├── cargador_config.py     # ⭐ Lector de JSON (SRP)
│   └── configurador.py        # Orquestador de Factories (8 métodos)
└── 🚀 lanzador/               # Orquestador (SRP puro)
```
---

## 📚 Evolución del Caso de Estudio

### 🎯 Requerimiento 1: Sistema Base de Procesamiento

**Objetivo**: Implementar procesador de señales digitales básico
- **Adquisición**: Captura de valores numéricos (consola/archivo)
- **Procesamiento**: Amplificación con factor configurable
- **Visualización**: Mostrar señal original y procesada

### 🔄 Requerimiento 2: Extensión con Nuevos Tipos (OCP)

**Contexto**: Agregar filtrado por umbral sin romper funcionalidad existente
- **Desafío OCP**: Extensión sin modificación de código existente
- **Solución**: Abstracciones + polimorfismo + Factory Pattern

### 🏭 Requerimiento 3: Factory Centralizado (SRP)

**Contexto**: Separar responsabilidades de creación y orquestación
- **Desafío SRP**: Lanzador con múltiples responsabilidades
- **Solución v2.0**: Configurador centralizado con decisiones "de fábrica"
- **Solución v3.0**: Configurador simplificado (8 métodos) + Factories especializados (4)

### 📚 Requerimiento 4: Manejo de Colecciones de Datos (LSP)

**Contexto**: Agregar manejo de colecciones (lista, pila, cola) para valores de señal
- **Desafío LSP**: Intercambiabilidad real entre diferentes implementaciones
- **Solución v4.0.0**: Abstracción `SenialBase` con contrato común
- **Resultado**: ✅ LSP aplicado completamente - 100% intercambiabilidad polimórfica

### 💾 Requerimiento 5: Persistencia y Trazabilidad (ISP)

**Contexto**: Persistencia de datos con auditoría y trazabilidad
- **Desafío ISP**: Interfaces segregadas por responsabilidad específica
- **Implementación v5.3.0**: ⚠️ Violación ISP intencional (didáctica)
- **Problema Demostrado**: `BaseRepositorio` con interfaz "gorda"
- **Solución v6.0.0**: ✅ Interfaces segregadas (BaseAuditor, BaseTrazador)

### 🔌 Requerimiento 6: Configuración Externa (DIP)

**Contexto**: Extensibilidad total sin impacto en código fuente
- **Desafío DIP**: Invertir dependencias para lograr configurabilidad completa
- **Solución v3.0.0**: **Configuración externa JSON** con **Factories especializados**
- **Resultado**: ✅ Cambiar comportamiento → Editar JSON, NO código

**🎯 Componentes DIP v3.0.0:**
- `config.json`: Configuración externa que determina tipos y parámetros
- `CargadorConfig`: Lector de JSON con ruta dinámica (`__file__`)
- `Configurador`: Simplificado de 21+ métodos a 8 métodos esenciales
- `FactorySenial`: Crea señales según tipo JSON
- `FactoryAdquisidor`: Crea adquisidores según tipo JSON
- `FactoryProcesador`: Crea procesadores según tipo JSON
- `FactoryContexto`: Crea contextos según tipo JSON

---

## 🚀 Funcionalidades Implementadas

### 📡 Adquisición de Señales (OCP + Factory)
- **`AdquisidorConsola`**: Entrada interactiva desde teclado
- **`AdquisidorArchivo`**: Lectura desde archivos de datos
- **`AdquisidorSenoidal`**: Generación de señal senoidal sintética
- **Factory**: `FactoryAdquisidor.crear(tipo, config, senial)`
- **Extensible**: Agregar tipo → Modificar solo FactoryAdquisidor

### ⚙️ Procesamiento de Señales (OCP + Factory)
- **`ProcesadorAmplificador`**: Amplificación con factor configurable
- **`ProcesadorUmbral`**: Filtrado por umbral
- **Factory**: `FactoryProcesador.crear(tipo, config, senial)`
- **Extensible**: Agregar tipo → Modificar solo FactoryProcesador

### 🏠 Tipos de Señales (LSP + Factory)
- **`SenialLista`**: Basada en lista Python
- **`SenialPila`**: LIFO (Last In, First Out)
- **`SenialCola`**: FIFO (First In, First Out)
- **Factory**: `FactorySenial.crear(tipo, config)`
- **Polimorfismo**: Todas cumplen protocolo `SenialBase`

### 💾 Persistencia (DIP + ISP + Factory)
- **`ContextoPickle`**: Persistencia binaria (.pickle)
- **`ContextoArchivo`**: Persistencia texto plano (.dat)
- **Factory**: `FactoryContexto.crear(tipo, config)`
- **Repository Pattern**: `RepositorioSenial(contexto)`
- **ISP**: Interfaces segregadas (BaseAuditor, BaseTrazador)

### 🏭 Configuración (DIP Completo)
- **`config.json`**: Configuración externa del sistema
- **`CargadorConfig`**: Lee y valida JSON
- **`Configurador`**: 8 métodos que delegan a Factories
- **Sin hardcoding**: Todos los tipos determinados por JSON

### 🚀 Orquestación Pura (SRP)
- **Responsabilidad única**: Solo coordinar flujo
- **Sin decisiones**: Delegadas al Configurador + JSON
- **DIP aplicado**: NO conoce tipos concretos

---

## 📖 Uso del Sistema

### 🚀 Ejecución Principal

```bash
# Ejecutar el sistema completo
python -m lanzador.lanzador

# O desde el directorio lanzador
cd lanzador
python lanzador.py
```

### 📁 Configuración del Sistema (config.json)

**Ubicación**: `configurador/config.json`

```json
{
  "version": "1.0.0",
  "descripcion": "Configuración externa del sistema - DIP aplicado",

  "senial_adquisidor": {
    "tipo": "lista",
    "tamanio": 20
  },

  "senial_procesador": {
    "tipo": "pila",
    "tamanio": 20
  },

  "adquisidor": {
    "tipo": "senoidal",
    "num_muestras": 20
  },

  "procesador": {
    "tipo": "amplificador",
    "factor": 4.0
  },

  "contexto_adquisicion": {
    "tipo": "archivo",
    "recurso": "./tmp/datos/adquisicion"
  },

  "contexto_procesamiento": {
    "tipo": "archivo",
    "recurso": "./tmp/datos/procesamiento"
  }
}
```

### 🎯 Cambiar Comportamiento sin Modificar Código

#### Ejemplo 1: Cambiar de Amplificador a Umbral

```json
// Editar config.json
"procesador": {
  "tipo": "umbral",
  "umbral": 100
}
```

```bash
# Ejecutar (sin tocar código)
python -m lanzador.lanzador
# → Sistema usa ProcesadorUmbral automáticamente ✅
```

#### Ejemplo 2: Cambiar Tipo de Señal

```json
// Editar config.json
"senial_adquisidor": {
  "tipo": "cola",
  "tamanio": 50
}
```

```bash
# Ejecutar (sin tocar código)
python -m lanzador.lanzador
# → Sistema usa SenialCola automáticamente ✅
```

#### Ejemplo 3: Cambiar Estrategia de Persistencia

```json
// Editar config.json
"contexto_adquisicion": {
  "tipo": "pickle",
  "recurso": "./tmp/datos/adquisicion"
}
```

```bash
# Ejecutar (sin tocar código)
python -m lanzador.lanzador
# → Sistema usa ContextoPickle automáticamente ✅
```

### ⚙️ Configuración Programática (API)

```python
from configurador import Configurador

# Inicializar con configuración externa
Configurador.inicializar_configuracion()  # Lee config.json

# Crear componentes (tipos determinados por JSON)
adquisidor = Configurador.crear_adquisidor()
procesador = Configurador.crear_procesador()
repo_adquisicion = Configurador.crear_repositorio_adquisicion()

# Usar componentes (polimorfismo puro)
adquisidor.leer_senial()
senial = adquisidor.obtener_senial_adquirida()
procesador.procesar(senial)
repo_adquisicion.guardar(senial)
```

---

## 🏗️ Arquitectura y Patrones

### 📦 Paquetes Independientes (SRP a Nivel de Paquetes)

| Paquete | Versión | Responsabilidad |
|---------|---------|----------------|
| `dominio-senial` | 5.0.0 | Entidades base + FactorySenial |
| `adquisicion-senial` | 3.0.0 | Adquisidores + FactoryAdquisidor |
| `procesamiento-senial` | 3.0.0 | Procesadores + FactoryProcesador |
| `presentacion-senial` | 2.0.0 | Visualización |
| `persistidor-senial` | 7.0.0 | Repository + FactoryContexto |
| `supervisor` | 1.0.0 | Interfaces segregadas (ISP) |
| `configurador` | **3.0.0** | DIP + JSON + Factories |
| `lanzador` | 6.0.0 | Orquestación pura |

### 🏭 Factories Especializados (v3.0.0)

```python
# Cada Factory tiene responsabilidad única
from dominio_senial import FactorySenial
from adquisicion_senial import FactoryAdquisidor
from procesamiento_senial import FactoryProcesador
from persistidor_senial import FactoryContexto

# Uso (internamente en Configurador)
senial = FactorySenial.crear('lista', {'tamanio': 20})
adquisidor = FactoryAdquisidor.crear('archivo', {'ruta_archivo': 'senial.txt'}, senial)
procesador = FactoryProcesador.crear('amplificador', {'factor': 4.0}, senial)
contexto = FactoryContexto.crear('pickle', {'recurso': './datos'})
```

### 🔄 Extensibilidad (OCP Demostrado)

```python
# Agregar nuevo tipo de procesador
# 1. Crear clase (nueva)
class ProcesadorFiltro(BaseProcesador):
    def procesar(self, senial):
        # Implementación
        pass

# 2. Modificar SOLO FactoryProcesador
elif tipo == 'filtro':
    from procesamiento_senial.procesador_filtro import ProcesadorFiltro
    frecuencia = config.get('frecuencia_corte', 50)
    return ProcesadorFiltro(frecuencia, senial)

# 3. Agregar en config.json
{
  "procesador": {
    "tipo": "filtro",
    "frecuencia_corte": 50
  }
}

# ✅ Configurador NO se modifica
# ✅ Lanzador NO se modifica
# ✅ Otros Factories NO se modifican
```

### 🔀 Intercambiabilidad (LSP Aplicado)

```python
# Cualquier señal funciona polimórficamente
from dominio_senial import SenialBase

def procesar_cualquier_senial(senial: SenialBase):
    """Función genérica que funciona con CUALQUIER tipo"""
    senial.poner_valor(42.0)
    valor = senial.sacar_valor()
    return valor

# ✅ Funciona con las 3 implementaciones
seniales = [
    FactorySenial.crear('lista', {'tamanio': 10}),
    FactorySenial.crear('pila', {'tamanio': 10}),
    FactorySenial.crear('cola', {'tamanio': 10}),
]

for senial in seniales:
    resultado = procesar_cualquier_senial(senial)
    print(f'{type(senial).__name__}: {resultado}')
```

---

## 📚 Documentación Técnica

### 📋 Documentos Disponibles

#### Principios SOLID

- **`docs/IMPLEMETACION DE SRP EN PAQUETES.md`**: Evolución de SRP a nivel de paquetes
- **`docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md`**: Guía completa del patrón OCP
- **`docs/VIOLACIONES DE LSP EN TIPOS DE SEÑAL.md`**: Análisis de violaciones LSP (histórico)
- **`docs/SOLUCION LSP CON ABSTRACCIONES.md`**: Solución completa LSP v4.0.0
- **`docs/CORRECCION ISP CON INTERFACES SEGREGADAS.md`**: ISP aplicado v6.0.0

#### DIP y Configuración Externa (v3.0.0) ⭐ NUEVO

- **`docs/APLICACION DIP CONFIGURACION EXTERNA.md`**: DIP completo con JSON
- **`docs/FACTORIES ESPECIALIZADOS - DELEGACION Y SRP.md`**: Patrón Factory especializado
- **`docs/CARGADOR CONFIG - GESTION DE CONFIGURACION EXTERNA.md`**: CargadorConfig detallado

#### Patrones de Diseño

- **`docs/PATRON REPOSITORY EN PERSISTENCIA.md`**: Repository Pattern aplicado
- **`docs/INCORPORACION DEL CONFIGURADOR CON FACTORY PATTERN.md`**: Factory centralizado
- **`docs/ANTI-PATRONES VS SOLID - ANÁLISIS COMPARATIVO.md`**: Comparativa antipatrones

#### Paquetes

- **Cada paquete**: README.md específico con arquitectura y uso


python 
---

## 🎯 Valor Didáctico

### ✅ Lo que se Demuestra

1. **SRP en 3 Niveles**:
   - Clases: Responsabilidad única por clase
   - Paquetes: Responsabilidad única por paquete
   - Factories: Responsabilidad única por dominio

2. **OCP Práctico**:
   - Extensibilidad editando JSON (config.json)
   - Agregar tipos → Modificar solo Factory correspondiente
   - Sin modificar Configurador ni Lanzador

3. **LSP Aplicado**:
   - Abstracción `SenialBase` con contrato común
   - Intercambiabilidad 100% entre Lista/Pila/Cola
   - Polimorfismo verificado con tests

4. **ISP Corregido**:
   - Interfaces segregadas (BaseAuditor, BaseTrazador)
   - RepositorioSenial: Implementa solo lo necesario
   - RepositorioUsuario: Sin métodos innecesarios

5. **DIP Completo** ⭐:
   - **Configuración externa JSON** determina dependencias
   - CargadorConfig con ruta dinámica (`__file__`)
   - Factories especializados (FactorySenial, FactoryAdquisidor, etc.)
   - Configurador simplificado (21+ → 8 métodos)
   - Cambiar comportamiento → Editar JSON, NO código

### 📊 Métricas de Mejora (v2.2 → v3.0)

```
CONFIGURADOR:
- Métodos: 21+ → 8 (62% reducción)
- Responsabilidades: Múltiples → 1 (orquestar Factories)
- Dependencias directas: Todas las clases → 4 Factories
- Acoplamiento: Alto → Bajo

SISTEMA:
- Configuración: Hardcoded → JSON externo
- Cambiar comportamiento: Modificar código → Editar JSON
- Extensibilidad: Media → Alta
- DIP: Parcial → Completo
```

### 🔄 Evolución Arquitectónica Completa

```
v1.0 → Implementación básica
v2.0 → Factory centralizado (Configurador)
v2.2 → Repository Pattern
v3.0 → DIP COMPLETO (JSON + CargadorConfig + Factories) ⭐
v4.0 → LSP aplicado (SenialBase)
v5.3 → Violación ISP (didáctica)
v6.0 → ISP corregido (interfaces segregadas) - ESTADO ACTUAL
```

---

## 🛠️ Instalación y Configuración

### Requisitos

- Python 3.8+
- pip

### Instalación

```bash
# Clonar repositorio
git clone <repository-url>
cd Senial_SOLID_IS

# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar paquetes (desarrollo)
pip install -e dominio_senial/
pip install -e adquisicion_senial/
pip install -e procesamiento_senial/
pip install -e presentacion_senial/
pip install -e persistidor_senial/
pip install -e supervisor/
pip install -e configurador/
pip install -e lanzador/

# O instalar desde requirements.txt (si existe)
pip install -r requirements.txt
```

### Configuración Inicial

```bash
# 1. Crear directorios de datos (si no existen)
mkdir -p tmp/datos/adquisicion
mkdir -p tmp/datos/procesamiento

# 2. Verificar config.json
cat configurador/config.json

# 3. Crear archivo de datos de ejemplo (si usas tipo "archivo")
echo -e "1.5\n2.8\n3.2\n4.1\n5.7" > senial.txt

# 4. Ejecutar el sistema
python -m lanzador.lanzador
```

### Personalizar Configuración

```bash
# Editar configuración externa
vim configurador/config.json

# Cambiar tipo de adquisidor, procesador, señal, contexto
# Ver ejemplos en docs/APLICACION DIP CONFIGURACION EXTERNA.md

# Ejecutar con nueva configuración
python -m lanzador.lanzador
```

---

## ✅ Corrección ISP Aplicada (v6.0.0)

### 🎯 Propósito Didáctico

Esta versión demuestra la **corrección del principio ISP** mediante interfaces segregadas:

1. **Interfaces Segregadas**:
   - `BaseRepositorio`: Solo métodos básicos (guardar, obtener)
   - `BaseAuditor`: Solo métodos de auditoría
   - `BaseTrazador`: Solo métodos de trazabilidad

2. **Paquete Supervisor**: Interfaces especializadas independientes

3. **Herencia Múltiple Selectiva**:
   - `RepositorioSenial`: BaseRepositorio + BaseAuditor + BaseTrazador
   - `RepositorioUsuario`: Solo BaseRepositorio

4. **Auditoría Automática**: Interna al repositorio (no llamadas explícitas)


**Salida esperada**:
- ✅ `RepositorioSenial`: Con auditoría y trazabilidad
- ✅ `RepositorioUsuario`: Solo persistencia
- ✅ Verificación: `hasattr(repo_usuario, 'auditar')` → `False`

---

## 📖 Conclusión

Este proyecto demuestra la **aplicación completa de los 5 principios SOLID** en un sistema real:

- **S**: Responsabilidad única en clases, paquetes, y Factories
- **O**: Extensibilidad mediante Factories y configuración JSON
- **L**: Polimorfismo garantizado con SenialBase
- **I**: Interfaces segregadas (BaseAuditor, BaseTrazador)
- **D**: **Configuración externa JSON determina TODAS las dependencias**

**El valor principal de este caso de estudio es mostrar que SOLID no es solo teoría - es una filosofía de diseño práctica que resulta en sistemas flexibles, extensibles, y mantenibles.**

---

## 📦 Distribución y Paquetización

Este proyecto incluye scripts completos de build e instalación para distribución multiplataforma.

### Build del Release

```bash
# Linux/macOS
./packaging/build/build_all.sh

# Windows
packaging\build\build_all.bat
```

**Genera**: 9 paquetes wheel + 9 distribuciones fuente en `packaging/release/`

### Instalación desde Release

```bash
# Linux/macOS
./packaging/install/install.sh

# Windows
packaging\install\install.bat
```

### Instalación Manual

```bash
# Instalar meta-paquete (instala todo el sistema)
pip install packaging/release/wheels/senial_solid-6.0.0-py3-none-any.whl

# O instalar componentes individuales
pip install packaging/release/wheels/*.whl
```

### Uso Después de Instalación

```bash
# Comando directo
senial-solid

# O como módulo
python -m lanzador.lanzador
```

### Estructura de Packaging

El directorio `packaging/` contiene:
- **metapackage/**: Meta-paquete senial-solid
- **build/**: Scripts de construcción
  - `verify_versions.py` - Verificar consistencia de versiones
  - `build_all.sh` - Build completo (Linux/macOS)
  - `build_all.bat` - Build completo (Windows)
- **install/**: Scripts de instalación
  - `install.sh` - Instalación automática (Linux/macOS)
  - `install.bat` - Instalación automática (Windows)
  - `verify_installation.py` - Verificar instalación
- **release/**: Artefactos generados (wheels, source, config, docs)

### Documentación de Paquetización

Ver `docs/PLAN_PAQUETIZACION_PASO_A_PASO.md` para el plan completo de implementación de la infraestructura de build y distribución.

---

**📖 Proyecto Didáctico - Victor Valotto**
**🎯 Objetivo**: Demostración práctica de principios SOLID aplicados progresivamente
**🔄 Estado v6.0.0**: ✅ TODOS los principios SOLID correctamente aplicados con DIP completo
