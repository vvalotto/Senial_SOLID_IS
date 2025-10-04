# Configurador - Factory Centralizado con Configuración Externa (DIP Aplicado)

**Versión:** 3.0.0
**Autor:** Victor Valotto
**Fecha:** 2025-10-04

## 📖 Descripción

El paquete `configurador` implementa un **Factory Centralizado** que aplica completamente el **Principio de Inversión de Dependencias (DIP)** mediante configuración externa JSON, delegando la creación de objetos a **Factories especializados**.

## 🎯 Principios SOLID Aplicados

- **SRP**: Responsabilidad única - leer configuración JSON y delegar a factories
- **OCP**: Extensible para nuevos tipos sin modificar código cliente
- **LSP**: Todos los objetos creados son intercambiables polimórficamente
- **DIP**: **Configuración externa (JSON) determina las dependencias del sistema**

## 🏗️ Arquitectura DIP

```
config.json (Configuración Externa)
    ↓
CargadorConfig (Lee JSON)
    ↓
Configurador (Orquestador)
    ↓
Factories Especializados
    ↓ ↓ ↓ ↓
    FactorySenial
    FactoryAdquisidor
    FactoryProcesador
    FactoryContexto
    ↓
Objetos Concretos
```

## 🔄 Migración XML → JSON

| Versión | Configuración | Factories |
|---------|--------------|-----------|
| v2.0.0 | XML (minidom.parse) | ❌ No |
| v2.2.0 | Hardcoded | ❌ No |
| **v3.0.0** | **JSON** | **✅ Sí** |

## 📋 API del Configurador

### Inicialización (Obligatorio)

```python
from configurador import Configurador

# Inicializar con configuración externa (sin ruta - usa default)
# Busca config.json en el directorio del módulo configurador
# Funciona independientemente de desde dónde se ejecute
Configurador.inicializar_configuracion()

# O con ruta explícita (opcional)
Configurador.inicializar_configuracion('/ruta/custom/config.json')
```

**🎯 Ruta Dinámica**: Si no se proporciona ruta, `CargadorConfig` usa `__file__` para encontrar `config.json` en el directorio del módulo `configurador`, independientemente del directorio de trabajo actual (CWD).

### Métodos Disponibles (8 métodos públicos)

#### 1. Creación de Señales

```python
# Señal para adquisidor (lee tipo del JSON)
senial_adq = Configurador.crear_senial_adquisidor()

# Señal para procesador (lee tipo del JSON)
senial_pro = Configurador.crear_senial_procesador()
```

#### 2. Creación de Adquisidor

```python
# Tipo y parámetros desde JSON
adquisidor = Configurador.crear_adquisidor()
```

#### 3. Creación de Procesador

```python
# Tipo y parámetros desde JSON
procesador = Configurador.crear_procesador()
```

#### 4. Creación de Visualizador

```python
visualizador = Configurador.crear_visualizador()
```

#### 5. Creación de Repositorios

```python
# Repositorio para señales adquiridas (contexto desde JSON)
repo_adq = Configurador.crear_repositorio_adquisicion()

# Repositorio para señales procesadas (contexto desde JSON)
repo_pro = Configurador.crear_repositorio_procesamiento()
```

## 📄 Archivo config.json

### Ubicación

```
proyecto/
├── configurador/
│   ├── config.json          ← Configuración externa
│   ├── configurador.py
│   └── cargador_config.py
```

### Estructura Completa

```json
{
  "version": "1.0.0",
  "descripcion": "Configuración externa del sistema de señales",

  "dir_recurso_datos": "./tmp/datos",

  "senial_adquisidor": {
    "tipo": "cola",
    "tamanio": 20
  },

  "senial_procesador": {
    "tipo": "pila",
    "tamanio": 20
  },

  "adquisidor": {
    "tipo": "archivo",
    "ruta_archivo": "./adquisidor/datos.txt"
  },

  "procesador": {
    "tipo": "umbral",
    "umbral": 100
  },

  "contexto_adquisicion": {
    "tipo": "pickle",
    "recurso": "./tmp/datos/adquisicion"
  },

  "contexto_procesamiento": {
    "tipo": "pickle",
    "recurso": "./tmp/datos/procesamiento"
  }
}
```

### Tipos Soportados

#### Señales
- `"lista"`: Señal con comportamiento de lista
- `"pila"`: Señal LIFO (Last In, First Out)
- `"cola"`: Señal FIFO (First In, First Out)

#### Adquisidores
- `"consola"`: Lectura desde consola
- `"archivo"`: Lectura desde archivo
- `"senoidal"`: Generación sintética senoidal

#### Procesadores
- `"amplificador"`: Amplifica valores por factor
- `"umbral"`: Filtra valores bajo umbral

#### Contextos
- `"pickle"`: Serialización binaria (rápida)
- `"archivo"`: Texto plano (human-readable)

## 💡 Ejemplos de Uso

### Ejemplo Básico

```python
from configurador import Configurador

# 1. Inicializar configuración externa
Configurador.inicializar_configuracion('./configurador/config.json')

# 2. Crear componentes (ya configurados desde JSON)
adquisidor = Configurador.crear_adquisidor()
procesador = Configurador.crear_procesador()
visualizador = Configurador.crear_visualizador()

# 3. Usar componentes
adquisidor.leer_senial()
senial_original = adquisidor.obtener_senial_adquirida()

procesador.procesar(senial_original)
senial_procesada = procesador.obtener_senial_procesada()

visualizador.mostrar_datos(senial_procesada)
```

### Ejemplo con Persistencia

```python
from configurador import Configurador

# Inicializar
Configurador.inicializar_configuracion('./configurador/config.json')

# Crear componentes
adquisidor = Configurador.crear_adquisidor()
procesador = Configurador.crear_procesador()
visualizador = Configurador.crear_visualizador()

# Crear repositorios (contextos desde JSON)
repo_adq = Configurador.crear_repositorio_adquisicion()
repo_pro = Configurador.crear_repositorio_procesamiento()

# Adquirir y persistir
adquisidor.leer_senial()
senial_original = adquisidor.obtener_senial_adquirida()
senial_original.id = 1000
repo_adq.guardar(senial_original)

# Procesar y persistir
procesador.procesar(senial_original)
senial_procesada = procesador.obtener_senial_procesada()
senial_procesada.id = 2000
repo_pro.guardar(senial_procesada)

# Recuperar
senial_recuperada = repo_adq.obtener("1000")
visualizador.mostrar_datos(senial_recuperada)
```

### Cambiar Configuración sin Modificar Código

**Escenario 1: Cambiar tipo de señal**

```json
{
  "senial_adquisidor": {
    "tipo": "lista",    // Cambiar de "cola" a "lista"
    "tamanio": 50       // Cambiar tamaño
  }
}
```

**Escenario 2: Cambiar procesador**

```json
{
  "procesador": {
    "tipo": "amplificador",  // Cambiar de "umbral" a "amplificador"
    "factor": 2.5            // Nuevo parámetro
  }
}
```

**Escenario 3: Cambiar formato de persistencia**

```json
{
  "contexto_adquisicion": {
    "tipo": "archivo",  // Cambiar de "pickle" a "archivo"
    "recurso": "./datos/texto/adquisicion"
  }
}
```

## 🏭 Factories Especializados Utilizados

El Configurador **delega** la creación a estos factories:

### FactorySenial
- **Ubicación**: `dominio_senial.FactorySenial`
- **Método**: `crear(tipo, config)`
- **Crea**: SenialLista, SenialPila, SenialCola

### FactoryAdquisidor
- **Ubicación**: `adquisicion_senial.FactoryAdquisidor`
- **Método**: `crear(tipo, config, senial)`
- **Crea**: AdquisidorConsola, AdquisidorArchivo, AdquisidorSenoidal

### FactoryProcesador
- **Ubicación**: `procesamiento_senial.FactoryProcesador`
- **Método**: `crear(tipo, config, senial)`
- **Crea**: ProcesadorAmplificador, ProcesadorConUmbral

### FactoryContexto
- **Ubicación**: `persistidor_senial.FactoryContexto`
- **Método**: `crear(tipo, config)`
- **Crea**: ContextoPickle, ContextoArchivo

## 🔧 Componentes del Paquete

### Configurador
**Responsabilidad**: Orquestador que lee JSON y delega a factories

**Métodos públicos** (8):
- `inicializar_configuracion(ruta)`
- `crear_senial_adquisidor()`
- `crear_senial_procesador()`
- `crear_adquisidor()`
- `crear_procesador()`
- `crear_visualizador()`
- `crear_repositorio_adquisicion()`
- `crear_repositorio_procesamiento()`

### CargadorConfig
**Responsabilidad**: Leer y validar archivo JSON

**Métodos principales**:
- `cargar()`: Lee el archivo JSON
- `obtener_config_senial_adquisidor()`
- `obtener_config_senial_procesador()`
- `obtener_config_adquisidor()`
- `obtener_config_procesador()`
- `obtener_config_contexto_adquisicion()`
- `obtener_config_contexto_procesamiento()`

## ✅ Beneficios del Enfoque DIP

### 1. Configuración Externa
✅ Cambiar comportamiento sin modificar código
✅ Diferentes configuraciones para testing/producción
✅ Configuración versionable (JSON en git)

### 2. Desacoplamiento Total
✅ Configurador no depende de implementaciones concretas
✅ Solo conoce abstracciones (Factories)
✅ Nuevos tipos sin modificar Configurador

### 3. Mantenibilidad
✅ Cambios centralizados en config.json
✅ Código más limpio (8 métodos vs 21 anteriores)
✅ Testing simplificado

### 4. Extensibilidad
✅ Agregar nuevos tipos editando JSON
✅ Sin recompilación ni redeploy
✅ Facilita experimentación

## 📊 Comparación de Versiones

| Aspecto | v2.2.0 | v3.0.0 |
|---------|--------|--------|
| Configuración | Hardcoded | JSON externo |
| Métodos públicos | 21 | 8 |
| Factories | No usa | Delega a 4 |
| DIP | Parcial | Completo |
| Wrappers redundantes | Sí | No |
| Flexibilidad | Baja | Alta |




Valida:
- ✅ Carga correcta del JSON
- ✅ Creación de todos los componentes
- ✅ Tipos coinciden con configuración
- ✅ DIP aplicado correctamente

## 📦 Instalación

```bash
pip install configurador
```

## 📚 Dependencias

- `dominio-senial >= 5.0.0` (FactorySenial)
- `adquisicion-senial >= 3.0.0` (FactoryAdquisidor)
- `procesamiento-senial >= 3.0.0` (FactoryProcesador)
- `persistidor-senial >= 7.0.0` (FactoryContexto)
- `presentacion-senial >= 2.0.0`

## 📖 Documentación Relacionada

- **DIP con JSON**: `docs/APLICACION_DIP_CONFIGURACION_EXTERNA.md`
- **Estado del proyecto**: `docs/ESTADO_Y_PROXIMOS_PASOS.md`
- **SRP en paquetes**: `docs/IMPLEMETACION DE SRP EN PAQUETES.md`
- **Patrón Repository**: `docs/PATRON REPOSITORY EN PERSISTENCIA.md`

## 🔄 Roadmap

### v3.0.0 (Actual) ✅
- [x] Configuración externa JSON
- [x] Delegación a Factories especializados
- [x] DIP completo aplicado
- [x] Eliminación de wrappers redundantes

### v4.0.0 (Futuro)
- [ ] Validación de esquemas JSON (JSON Schema)
- [ ] Soporte para múltiples archivos de configuración
- [ ] Variables de entorno en config

### v5.0.0 (Futuro)
- [ ] IoC Container completo
- [ ] Configuración en runtime
- [ ] Plugin architecture
