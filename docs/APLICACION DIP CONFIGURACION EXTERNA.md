# APLICACIÓN DIP CON CONFIGURACIÓN EXTERNA JSON - Inversión de Dependencias Completa

**Proyecto**: Senial SOLID IS
**Autor**: Victor Valotto
**Fecha**: Octubre 2024
**Versión**: 3.0.0
**Objetivo**: Demostrar la aplicación completa del Dependency Inversion Principle mediante configuración externa JSON y Factories especializados

---

## 📋 Resumen Ejecutivo

Este documento presenta la **implementación completa del Dependency Inversion Principle (DIP)** en el sistema de procesamiento de señales, mediante **configuración externa JSON** que determina TODAS las dependencias del sistema. La arquitectura resultante permite cambiar el comportamiento completo del sistema editando un archivo JSON, sin modificar una sola línea de código fuente.

### 🎯 **Innovación Principal**

Transformar el sistema de configuración hardcoded/XML a **configuración externa JSON** con **delegación a Factories especializados**, logrando que el código de alto nivel (Lanzador) NO dependa de detalles de implementación, sino que ambos dependan de abstracciones configurables externamente.

### 🔄 **Evolución Arquitectónica**

```
v1.0 → Configuración hardcoded (código fuente)
v2.0 → Configuración XML (minidom.parse)
v2.2 → Factory Pattern con inyección programática
v3.0 → DIP COMPLETO: JSON + CargadorConfig + Factories especializados (ACTUAL)
```

---

## 🎯 El Principio DIP (Dependency Inversion Principle)

### Definición Formal

> **Módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.**
>
> **Abstracciones no deben depender de detalles. Detalles deben depender de abstracciones.**
>
> — Robert C. Martin

### Aplicación en Nuestro Sistema

#### ❌ **ANTES - Violación de DIP**

```python
# Lanzador depende de detalles concretos
class Lanzador:
    def ejecutar():
        # ❌ Código conoce tipos específicos
        senial = SenialLista(10)
        adquisidor = AdquisidorArchivo("senial.txt", senial)
        procesador = ProcesadorUmbral(100, senial)

        # ✅ Orquestación (legítimo)
        adquisidor.leer_senial()
        procesador.procesar(senial)
```

**Problemas:**
- Lanzador conoce `SenialLista`, `AdquisidorArchivo`, `ProcesadorUmbral`
- Cambiar tipo de señal → Modificar código del Lanzador
- Cambiar tipo de adquisidor → Modificar código del Lanzador
- Acoplamiento fuerte con implementaciones concretas

#### ✅ **DESPUÉS - DIP Aplicado**

```python
# Lanzador depende solo de abstracciones obtenidas del Configurador
class Lanzador:
    def ejecutar():
        # ✅ Inicializar desde configuración externa
        Configurador.inicializar_configuracion()  # Lee config.json

        # ✅ Obtener componentes (tipos determinados por JSON)
        adquisidor = Configurador.crear_adquisidor()
        procesador = Configurador.crear_procesador()

        # ✅ Orquestación pura (sin conocer tipos concretos)
        adquisidor.leer_senial()
        procesador.procesar(senial)
```

**Beneficios:**
- Lanzador NO conoce tipos concretos
- Cambiar tipo de señal → Editar `config.json` (NO código)
- Cambiar tipo de adquisidor → Editar `config.json` (NO código)
- Desacoplamiento total mediante abstracciones

---

## 🏗️ Arquitectura DIP Completa

### Flujo de Dependencias

```
┌────────────────────────────────────────────────────────────────┐
│                    config.json                                 │
│           (Configuración Externa - DIP)                        │
│   Determina: tipos, parámetros, estrategias                   │
└───────────────────────────┬────────────────────────────────────┘
                            ↓ leído por
┌───────────────────────────────────────────────────────────────┐
│                   CargadorConfig                              │
│        (Lee y valida JSON - SRP)                              │
│   - Usa __file__ para ruta dinámica                           │
│   - Singleton en Configurador                                 │
└───────────────────────────┬───────────────────────────────────┘
                            ↓ proporciona datos a
┌───────────────────────────────────────────────────────────────┐
│                   CONFIGURADOR                                │
│      (Delega a Factories - Factory Centralizado)             │
│   8 métodos públicos (simplificado v3.0)                      │
└───────────────────────────┬───────────────────────────────────┘
                            ↓ delega creación a
┌───────────────────────────────────────────────────────────────┐
│              FACTORIES ESPECIALIZADOS                         │
│  ┌──────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │FactorySenial│  │FactoryAdquisidor│  │FactoryProcesador│ │
│  └──────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐│
│  │            FactoryContexto                                ││
│  └──────────────────────────────────────────────────────────┘│
└───────────────────────────┬───────────────────────────────────┘
                            ↓ crean
┌───────────────────────────────────────────────────────────────┐
│              OBJETOS CONCRETOS                                │
│   SenialLista/Pila/Cola, AdquisidorConsola/Archivo/Senoidal, │
│   ProcesadorAmplificador/Umbral, ContextoPickle/Archivo      │
└───────────────────────────┬───────────────────────────────────┘
                            ↓ usados por
┌───────────────────────────────────────────────────────────────┐
│                      LANZADOR                                 │
│        (Orquestador - NO conoce tipos concretos)              │
│   Solo conoce abstracciones y métodos del Configurador       │
└───────────────────────────────────────────────────────────────┘
```

### Inversión de Control

**DIP = Inversión de Control del Flujo de Dependencias**

```
❌ ANTES (sin DIP):
Lanzador → SenialLista (dependencia concreta)
Lanzador → AdquisidorArchivo (dependencia concreta)
Lanzador → ProcesadorUmbral (dependencia concreta)

✅ DESPUÉS (con DIP):
Lanzador → Configurador → Abstracciones
                ↓
          config.json determina tipos concretos
                ↓
          Factories crean instancias
                ↓
          Objetos concretos (desconocidos para Lanzador)
```

---

## 📄 Configuración Externa JSON

### Estructura del config.json

```json
{
  "version": "1.0.0",
  "descripcion": "Configuración externa del sistema - DIP aplicado",

  "dir_recurso_datos": "./tmp/datos",

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
    "tipo": "pickle",
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
// ANTES (config.json)
"procesador": {
  "tipo": "amplificador",
  "factor": 4.0
}

// DESPUÉS (solo editar JSON)
"procesador": {
  "tipo": "umbral",
  "umbral": 100
}
```

**Resultado:** Sistema usa ProcesadorUmbral sin tocar código fuente ✅

#### Ejemplo 2: Cambiar Estrategia de Persistencia

```json
// ANTES (config.json)
"contexto_adquisicion": {
  "tipo": "pickle",
  "recurso": "./tmp/datos/adquisicion"
}

// DESPUÉS (solo editar JSON)
"contexto_adquisicion": {
  "tipo": "archivo",
  "recurso": "./tmp/datos/adquisicion"
}
```

**Resultado:** Sistema usa ContextoArchivo sin tocar código fuente ✅

#### Ejemplo 3: Cambiar Tipo de Señal

```json
// ANTES (config.json)
"senial_adquisidor": {
  "tipo": "lista",
  "tamanio": 20
}

// DESPUÉS (solo editar JSON)
"senial_adquisidor": {
  "tipo": "cola",
  "tamanio": 50
}
```

**Resultado:** Sistema usa SenialCola sin tocar código fuente ✅

---

## 🔧 Componente CargadorConfig

### Responsabilidad Única

```python
class CargadorConfig:
    """
    SRP: SOLO leer y validar configuración JSON
    DIP: Proporciona datos para que Configurador delegue a Factories
    """

    def __init__(self, ruta_config: str = None):
        """
        🎯 Ruta Dinámica: Si no se proporciona ruta, usa __file__
        para encontrar config.json en el directorio del módulo configurador,
        independientemente de desde dónde se ejecute el lanzador.
        """
        if ruta_config is None:
            # Determinar ruta relativa al módulo configurador, no al CWD
            modulo_dir = Path(__file__).parent
            self.ruta_config = modulo_dir / 'config.json'
        else:
            self.ruta_config = Path(ruta_config)
        self._config = None

    def cargar(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo JSON"""
        if not self.ruta_config.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.ruta_config}")

        with open(self.ruta_config, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

        return self._config

    def obtener_config_senial_adquisidor(self) -> Dict[str, Any]:
        """Retorna configuración de señal para adquisidor"""
        if self._config is None:
            self.cargar()
        return self._config.get('senial_adquisidor', {
            'tipo': 'lista',
            'tamanio': 10
        })

    # ... métodos similares para otras configuraciones
```

### Características Clave

#### 🎯 **Ruta Dinámica con `__file__`**

```python
# ✅ Funciona desde cualquier directorio
# Ejecutar desde raíz del proyecto:
cd /Users/victor/PycharmProjects/Senial_SOLID_IS
python3 -m lanzador.lanzador
# → Encuentra: /Users/victor/.../configurador/config.json ✓

# Ejecutar desde /tmp:
cd /tmp
python3 -m lanzador.lanzador
# → Encuentra: /Users/victor/.../configurador/config.json ✓
```

**Beneficio:** No depende del Current Working Directory (CWD)

#### 📋 **Fallbacks por Defecto**

```python
# Si config.json no existe o falta una sección:
return self._config.get('procesador', {
    'tipo': 'amplificador',  # ← Valor por defecto
    'factor': 4.0
})
```

**Beneficio:** Sistema robusto ante configuraciones incompletas

---

## 🏭 Refactorización del Configurador v3.0

### Simplificación Radical

#### ❌ **ANTES v2.2 - 21+ métodos redundantes**

```python
class Configurador:
    # Métodos específicos (redundantes)
    @staticmethod
    def crear_senial_lista(tamanio):
        return SenialLista(tamanio)

    @staticmethod
    def crear_senial_pila(tamanio):
        return SenialPila(tamanio)

    @staticmethod
    def crear_senial_cola(tamanio):
        return SenialCola(tamanio)

    @staticmethod
    def crear_adquisidor_consola(num_muestras, senial):
        return AdquisidorConsola(num_muestras, senial)

    @staticmethod
    def crear_adquisidor_archivo(ruta, senial):
        return AdquisidorArchivo(ruta, senial)

    # ... 15+ métodos más
```

**Problemas:**
- 21+ métodos públicos (violación Pylint)
- Código repetitivo y redundante
- Difícil de mantener
- No escala para nuevos tipos

#### ✅ **DESPUÉS v3.0 - 8 métodos esenciales**

```python
class Configurador:
    _cargador = None  # Singleton CargadorConfig

    @staticmethod
    def inicializar_configuracion(ruta_config: str = None):
        """🚀 Inicializa el sistema de configuración externa"""
        Configurador._cargador = CargadorConfig(ruta_config)
        Configurador._cargador.cargar()
        print(f"✅ Configuración cargada desde {Configurador._cargador.ruta_config}")

    @staticmethod
    def crear_senial_adquisidor():
        """🏭 Señal para adquisición (tipo desde JSON)"""
        if Configurador._cargador is None:
            config = {'tamanio': 10}
            return FactorySenial.crear('lista', config)

        config = Configurador._cargador.obtener_config_senial_adquisidor()
        tipo = config.get('tipo', 'lista')
        return FactorySenial.crear(tipo, config)  # ← Delegación a Factory

    @staticmethod
    def crear_adquisidor():
        """🏭 Adquisidor (tipo desde JSON)"""
        if Configurador._cargador is None:
            config = {'ruta_archivo': 'senial.txt'}
            senial = Configurador.crear_senial_adquisidor()
            return FactoryAdquisidor.crear('archivo', config, senial)

        config = Configurador._cargador.obtener_config_adquisidor()
        tipo = config.get('tipo', 'archivo')
        senial = Configurador.crear_senial_adquisidor()
        return FactoryAdquisidor.crear(tipo, config, senial)  # ← Delegación

    # ... 6 métodos más (total 8)
```

**Beneficios:**
- Solo 8 métodos públicos (cumple Pylint)
- Eliminación de redundancia
- Delegación a Factories especializados
- Escalable para nuevos tipos (agregar en Factory, no en Configurador)

### Los 8 Métodos Esenciales

| # | Método | Responsabilidad |
|---|--------|-----------------|
| 1 | `inicializar_configuracion()` | Cargar config.json |
| 2 | `crear_senial_adquisidor()` | Señal para adquisición (JSON) |
| 3 | `crear_senial_procesador()` | Señal para procesamiento (JSON) |
| 4 | `crear_adquisidor()` | Adquisidor (JSON + Factory) |
| 5 | `crear_procesador()` | Procesador (JSON + Factory) |
| 6 | `crear_visualizador()` | Visualizador (simple) |
| 7 | `crear_repositorio_adquisicion()` | Repo + Contexto (JSON + Factory) |
| 8 | `crear_repositorio_procesamiento()` | Repo + Contexto (JSON + Factory) |

---

## 🏭 Factories Especializados

### Patrón de Delegación

```
Configurador (orquestador) → Factories (creadores especializados)
                                ↓
                          Objetos concretos
```

### FactorySenial

```python
class FactorySenial:
    @staticmethod
    def crear(tipo: str, config: Dict[str, Any]):
        """Factory para crear señales según tipo"""
        tamanio = config.get('tamanio', 10)

        if tipo == 'lista':
            return SenialLista(tamanio)
        elif tipo == 'pila':
            return SenialPila(tamanio)
        elif tipo == 'cola':
            return SenialCola(tamanio)
        else:
            raise ValueError(f"Tipo de señal desconocido: {tipo}")
```

### FactoryAdquisidor

```python
class FactoryAdquisidor:
    @staticmethod
    def crear(tipo: str, config: Dict[str, Any], senial):
        """Factory para crear adquisidores con señal inyectada"""
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
            raise ValueError(f"Tipo de adquisidor desconocido: {tipo}")
```

### FactoryProcesador

```python
class FactoryProcesador:
    @staticmethod
    def crear(tipo: str, config: Dict[str, Any], senial):
        """Factory para crear procesadores con señal inyectada"""
        if tipo == 'amplificador':
            factor = config.get('factor', 4.0)
            return ProcesadorAmplificador(factor, senial)
        elif tipo == 'umbral':
            umbral = config.get('umbral', 100)
            return ProcesadorUmbral(umbral, senial)
        else:
            raise ValueError(f"Tipo de procesador desconocido: {tipo}")
```

### FactoryContexto

```python
class FactoryContexto:
    @staticmethod
    def crear(tipo: str, config: Dict[str, Any]):
        """Factory para crear contextos de persistencia"""
        recurso = config.get('recurso', './datos_persistidos')

        if tipo == 'pickle':
            return ContextoPickle(recurso)
        elif tipo == 'archivo':
            return ContextoArchivo(recurso)
        else:
            raise ValueError(f"Tipo de contexto desconocido: {tipo}")
```

### Ventajas del Patrón Factory

1. **SRP**: Cada Factory tiene responsabilidad única
2. **OCP**: Agregar nuevo tipo → Modificar solo el Factory correspondiente
3. **Encapsulación**: Lógica de creación aislada
4. **Testabilidad**: Factories testeables independientemente
5. **DIP**: Configurador NO conoce detalles de construcción

---

## 🔄 Integración en el Lanzador

### Flujo Completo

```python
class Lanzador:
    @staticmethod
    def ejecutar():
        try:
            # 🎯 PASO 0: Inicializar configuración externa (JSON)
            print("🔧 INICIALIZANDO CONFIGURACIÓN EXTERNA")
            try:
                # No se pasa ruta - usa config.json en directorio del módulo
                # Funciona independientemente de desde dónde se ejecute
                Configurador.inicializar_configuracion()
                print("✅ Todas las dependencias determinadas externamente (DIP)")
            except FileNotFoundError:
                print("⚠️  config.json no encontrado - usando configuración por defecto")

            # ✅ PASO 1: Obtener componentes configurados (DIP)
            # Tipos determinados por config.json, NO por código
            adquisidor = Configurador.crear_adquisidor()
            procesador = Configurador.crear_procesador()
            visualizador = Configurador.crear_visualizador()

            repo_adquisicion = Configurador.crear_repositorio_adquisicion()
            repo_procesamiento = Configurador.crear_repositorio_procesamiento()

            # ✅ PASO 2: Orquestación pura (sin conocer tipos)
            adquisidor.leer_senial()
            senial_original = adquisidor.obtener_senial_adquirida()

            # Persistir
            repo_adquisicion.guardar(senial_original)

            # Procesar
            procesador.procesar(senial_original)
            senial_procesada = procesador.obtener_senial_procesada()

            # Persistir
            repo_procesamiento.guardar(senial_procesada)

            # Recuperar desde repositorios
            senial_recuperada = repo_adquisicion.obtener(str(senial_original.id))

            # Visualizar
            visualizador.mostrar_datos(senial_recuperada)

            print("✅ DIP COMPLETO: Configuración externa JSON determinó TODAS las dependencias")

        except Exception as e:
            print(f"❌ Error: {e}")
```

### Transparencia Total

**Lanzador NO conoce:**
- ❌ Tipo de señal usado (`SenialLista`, `SenialPila`, `SenialCola`)
- ❌ Tipo de adquisidor (`AdquisidorConsola`, `AdquisidorArchivo`, `AdquisidorSenoidal`)
- ❌ Tipo de procesador (`ProcesadorAmplificador`, `ProcesadorUmbral`)
- ❌ Tipo de contexto (`ContextoPickle`, `ContextoArchivo`)

**Lanzador SOLO conoce:**
- ✅ Abstracciones (`adquisidor`, `procesador`, `visualizador`, `repositorio`)
- ✅ Métodos del Configurador (`crear_adquisidor()`, `crear_procesador()`, etc.)
- ✅ Protocolo de orquestación (`leer_senial()`, `procesar()`, `mostrar_datos()`)

---

## 📊 Comparativa: Antes vs Después

### Tabla Comparativa

| Aspecto | v2.2 (XML/Hardcoded) | v3.0 (JSON + DIP) |
|---------|---------------------|------------------|
| **Configuración** | XML (minidom.parse) | JSON (CargadorConfig) |
| **Métodos Configurador** | 21+ métodos | 8 métodos esenciales |
| **Factories** | ❌ No | ✅ Sí (4 especializados) |
| **Delegación** | ❌ No | ✅ Sí (Factories) |
| **Ruta Config** | Relativa a CWD | Dinámica con `__file__` |
| **DIP** | ⚠️ Parcial | ✅ Completo |
| **Cambiar comportamiento** | Modificar código | Editar JSON |
| **Acoplamiento** | Alto | Bajo |
| **Testabilidad** | Media | Alta |
| **Mantenibilidad** | Media | Alta |

### Métricas de Mejora

```
Reducción de métodos: 21 → 8 (62% menos)
Redundancia: Alta → Eliminada
Acoplamiento: Fuerte → Débil
Extensibilidad: Baja → Alta
Configurabilidad: Media → Completa
```

---

## 🎯 Principios SOLID Aplicados

### SRP (Single Responsibility Principle)

| Componente | Responsabilidad Única |
|------------|----------------------|
| `CargadorConfig` | Leer y validar JSON |
| `Configurador` | Leer JSON + Delegar a Factories |
| `FactorySenial` | Crear señales |
| `FactoryAdquisidor` | Crear adquisidores |
| `FactoryProcesador` | Crear procesadores |
| `FactoryContexto` | Crear contextos |
| `Lanzador` | Orquestar flujo |

### OCP (Open/Closed Principle)

✅ **Extensible sin modificación:**
- Agregar nuevo tipo de señal → Modificar `FactorySenial` + agregar opción en JSON
- Agregar nuevo adquisidor → Modificar `FactoryAdquisidor` + agregar opción en JSON
- Agregar nuevo procesador → Modificar `FactoryProcesador` + agregar opción en JSON
- **Lanzador y Configurador NO se modifican**

### LSP (Liskov Substitution Principle)

✅ **Tipos intercambiables:**
- `SenialLista`, `SenialPila`, `SenialCola` → Todas cumplen protocolo `SenialBase`
- `AdquisidorConsola`, `AdquisidorArchivo`, `AdquisidorSenoidal` → Protocolo común
- `ProcesadorAmplificador`, `ProcesadorUmbral` → Protocolo común
- `ContextoPickle`, `ContextoArchivo` → Protocolo `BaseContexto`

### ISP (Interface Segregation Principle)

✅ **Interfaces segregadas:**
- `BaseRepositorio`: Solo métodos básicos (`guardar`, `obtener`)
- `BaseAuditor`: Solo métodos de auditoría (paquete supervisor)
- `BaseTrazador`: Solo métodos de trazabilidad (paquete supervisor)
- **Clientes NO dependen de métodos que no usan**

### DIP (Dependency Inversion Principle) ⭐

✅ **DIP COMPLETO:**
- **Configuración externa (JSON)** determina TODAS las dependencias
- Lanzador depende de **Configurador** (abstracción)
- Configurador depende de **Factories** (abstracciones)
- Factories dependen de **config.json** (configuración externa)
- Repositorio depende de **BaseContexto** (abstracción)
- **Cambiar comportamiento**: Editar JSON, NO código

---

## 🧪 Ejemplos Prácticos de DIP

### Caso 1: Cambiar de Lista a Cola

```json
// config.json - ANTES
"senial_adquisidor": {
  "tipo": "lista",
  "tamanio": 20
}

// config.json - DESPUÉS
"senial_adquisidor": {
  "tipo": "cola",
  "tamanio": 50
}
```

```bash
# Ejecutar sin modificar código
python3 -m lanzador.lanzador
# → Sistema usa SenialCola(50) automáticamente ✅
```

### Caso 2: Cambiar de Archivo a Senoidal

```json
// config.json - ANTES
"adquisidor": {
  "tipo": "archivo",
  "ruta_archivo": "senial.txt"
}

// config.json - DESPUÉS
"adquisidor": {
  "tipo": "senoidal",
  "num_muestras": 100
}
```

```bash
# Ejecutar sin modificar código
python3 -m lanzador.lanzador
# → Sistema usa AdquisidorSenoidal(100) automáticamente ✅
```

### Caso 3: Cambiar de Amplificador a Umbral

```json
// config.json - ANTES
"procesador": {
  "tipo": "amplificador",
  "factor": 4.0
}

// config.json - DESPUÉS
"procesador": {
  "tipo": "umbral",
  "umbral": 150
}
```

```bash
# Ejecutar sin modificar código
python3 -m lanzador.lanzador
# → Sistema usa ProcesadorUmbral(150) automáticamente ✅
```

### Caso 4: Cambiar de Pickle a Archivo

```json
// config.json - ANTES
"contexto_procesamiento": {
  "tipo": "pickle",
  "recurso": "./tmp/datos/procesamiento"
}

// config.json - DESPUÉS
"contexto_procesamiento": {
  "tipo": "archivo",
  "recurso": "./tmp/datos/procesamiento"
}
```

```bash
# Ejecutar sin modificar código
python3 -m lanzador.lanzador
# → Sistema usa ContextoArchivo automáticamente ✅
```

---

## 📚 Lecciones Aprendidas

### ✅ **Hacer (Best Practices)**

1. **Configuración Externa**: Usar JSON para determinar dependencias
2. **Ruta Dinámica**: Usar `__file__` para rutas independientes del CWD
3. **Factories Especializados**: Delegar creación a componentes específicos
4. **Singleton Config**: Una sola instancia de `CargadorConfig` en `Configurador`
5. **Fallbacks**: Valores por defecto para configuraciones incompletas
6. **Validación**: Tipos en JSON deben coincidir con tipos esperados (int vs str)
7. **Delegación**: Configurador delega, NO implementa lógica de creación
8. **Separación**: SRP estricto - cada componente una responsabilidad

### ❌ **Evitar (Anti-Patterns)**

1. **Hardcoding**: No codificar tipos concretos en Lanzador
2. **Redundancia**: No duplicar métodos en Configurador
3. **Acoplamiento**: No hacer que Lanzador conozca implementaciones
4. **CWD Dependence**: No asumir directorio de trabajo actual
5. **Wrappers Innecesarios**: No crear métodos que solo llaman a otros
6. **Tipos Mixtos**: No mezclar strings y numbers en JSON sin validación
7. **Múltiples Responsabilidades**: No mezclar configuración con orquestación

---

## 🔮 Evolución Futura

### v4.0 - Validación de Esquemas JSON

```python
# JSON Schema para validar config.json
schema = {
    "type": "object",
    "properties": {
        "senial_adquisidor": {
            "type": "object",
            "properties": {
                "tipo": {"type": "string", "enum": ["lista", "pila", "cola"]},
                "tamanio": {"type": "integer", "minimum": 1}
            },
            "required": ["tipo", "tamanio"]
        },
        # ...
    },
    "required": ["senial_adquisidor", "adquisidor", "procesador"]
}
```

### v5.0 - IoC Container Completo

```python
# Contenedor de Inversión de Control
class Container:
    _bindings = {}

    @classmethod
    def bind(cls, interface, implementation):
        cls._bindings[interface] = implementation

    @classmethod
    def resolve(cls, interface):
        return cls._bindings[interface]()

# Uso
Container.bind('adquisidor', lambda: Configurador.crear_adquisidor())
adquisidor = Container.resolve('adquisidor')
```

---

## 📖 Conclusión

La implementación de **DIP con configuración externa JSON** representa la **culminación de los principios SOLID** en el sistema de procesamiento de señales. Al invertir el control de las dependencias desde el código fuente hacia un archivo de configuración externo, logramos:

1. ✅ **Desacoplamiento total** entre orquestación y configuración
2. ✅ **Flexibilidad completa** para cambiar comportamiento sin modificar código
3. ✅ **Mantenibilidad alta** mediante SRP estricto en cada componente
4. ✅ **Extensibilidad óptima** mediante Factories especializados
5. ✅ **Testabilidad superior** mediante inyección de configuración

**DIP no es solo un principio técnico - es una filosofía de diseño que invierte el flujo tradicional de dependencias, permitiendo que el código de alto nivel permanezca estable mientras los detalles de implementación varían según la configuración externa.**

---

**📖 Documento Técnico - Sistema SOLID Completo**
**Victor Valotto - Octubre 2024**
**v3.0.0 - DIP Aplicado con Configuración Externa JSON**
