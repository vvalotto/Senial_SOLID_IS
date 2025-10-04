# CHANGELOG - v6.0.0

## [6.0.0] - 2025-10-04

### 🎯 Resumen

Release mayor que implementa **DIP completo** con configuración externa JSON, **Factories especializados** delegados, y **infraestructura completa de build y distribución multiplataforma**.

---

### ✨ Agregado

#### DIP y Configuración Externa
- ✅ **CargadorConfig** con ruta dinámica basada en `__file__`
- ✅ **config.json** como configuración externa del sistema
- ✅ Inicialización desde JSON en `Configurador.inicializar_configuracion()`
- ✅ Configuración versionable y portable

#### Factories Especializados
- ✅ **FactorySenial** (dominio_senial) - Crea SenialLista, SenialPila, SenialCola
- ✅ **FactoryAdquisidor** (adquisicion_senial) - Crea adquisidores según config
- ✅ **FactoryProcesador** (procesamiento_senial) - Crea procesadores según config
- ✅ **FactoryContexto** (persistidor_senial) - Crea contextos de persistencia

#### Infraestructura de Build y Distribución
- ✅ **packaging/metapackage/** - Meta-paquete senial-solid v6.0.0 (instala todo el sistema)
- ✅ **packaging/build/verify_versions.py** - Verifica consistencia de versiones entre paquetes
- ✅ **packaging/build/build_all.sh** - Script de build para Linux/macOS
- ✅ **packaging/build/build_all.bat** - Script de build para Windows
- ✅ **packaging/install/install.sh** - Script de instalación para Linux/macOS
- ✅ **packaging/install/install.bat** - Script de instalación para Windows
- ✅ **packaging/install/verify_installation.py** - Verifica que todos los componentes estén instalados
- ✅ **packaging/release/** - Directorio con wheels, source distributions, config, docs
- ✅ Entry point `senial-solid` - Comando de consola

#### Documentación
- ✅ `APLICACION_DIP_CONFIGURACION_EXTERNA.md` - DIP con JSON explicado
- ✅ `FACTORIES_ESPECIALIZADOS_-_DELEGACION_Y_SRP.md` - Patrón Factory aplicado
- ✅ `CARGADOR_CONFIG_-_GESTION_DE_CONFIGURACION_EXTERNA.md` - CargadorConfig
- ✅ `PLAN_PAQUETIZACION_PASO_A_PASO.md` - Plan de 8 fases de paquetización
- ✅ `packaging/release/README.md` - Instrucciones de distribución
- ✅ Actualización README.md principal con sección de distribución

---

### 🔄 Modificado

#### Configurador (v2.2.0 → v3.0.0)
- **BREAKING**: Eliminados 13+ métodos redundantes
- **Simplificado**: De 21 métodos a 8 métodos esenciales
- **Delegación**: Ya no crea objetos directamente, delega a Factories especializados
- **Configuración**: Lee config.json en vez de valores hardcoded
- **DIP**: Configuración externa determina todas las dependencias

**API anterior (v2.2.0 - hardcoded)**:
```python
# Métodos hardcoded eliminados:
crear_senial_lista(tamanio)
crear_senial_pila(tamanio)
crear_senial_cola(tamanio)
crear_adquisidor_consola(senial)
crear_adquisidor_archivo(senial, ruta)
# ... 16+ métodos más
```

**API nueva (v3.0.0 - config JSON)**:
```python
# Solo 8 métodos, configurables desde JSON:
inicializar_configuracion(ruta_config)  # Nuevo
crear_senial_adquisidor()
crear_senial_procesador()
crear_adquisidor()
crear_procesador()
crear_visualizador()
crear_repositorio_adquisicion()
crear_repositorio_procesamiento()
```

#### Lanzador (v5.0.0 → v6.0.0)
- **Inicialización JSON**: Llama a `Configurador.inicializar_configuracion()`
- **Simplificado**: Usa nuevos métodos del Configurador v3.0.0
- **DIP completo**: Todo configurado desde JSON

#### Packaging
- **Setup.py fixes**: Todos los paquetes corregidos para usar `package_dir`
- **Estructura plana**: Soporta estructura donde setup.py está al nivel de __init__.py

---

### 🐛 Corregido

- ✅ **supervisor/setup.py**: Manejo robusto de README.md en builds aislados
- ✅ **dominio_senial/setup.py**: Configuración correcta de `package_dir`
- ✅ **Todos los setup.py**: Estructura de packaging para módulos de nivel superior
- ✅ **Build isolation**: Los paquetes se construyen correctamente en entornos aislados

---

### 📦 Componentes y Versiones

| Paquete | Versión | Cambios |
|---------|---------|---------|
| **senial-solid** | 6.0.0 | ✨ NUEVO - Meta-paquete |
| **lanzador** | 6.0.0 | 🔄 Inicialización JSON |
| **configurador** | 3.0.0 | 🔄 DIP + Factories delegados |
| **persistidor-senial** | 7.0.0 | ✨ FactoryContexto |
| **dominio-senial** | 5.0.0 | ✨ FactorySenial |
| **adquisicion-senial** | 3.0.0 | ✨ FactoryAdquisidor |
| **procesamiento-senial** | 3.0.0 | ✨ FactoryProcesador |
| **presentacion-senial** | 2.0.0 | Sin cambios |
| **supervisor** | 1.0.0 | 🐛 Fix setup.py |

---

### 🏗️ Arquitectura DIP Completa

```
config.json (Configuración Externa - DIP)
    ↓
CargadorConfig (Lee y valida JSON)
    ↓
Configurador (Orquesta Factories)
    ↓
Factories Especializados (SRP + OCP)
    ↓ ↓ ↓ ↓
    FactorySenial
    FactoryAdquisidor
    FactoryProcesador
    FactoryContexto
    ↓
Objetos Concretos (LSP garantizado)
```

---

### 📊 Métricas del Release

- **Paquetes distribuibles**: 9 (8 componentes + 1 meta-paquete)
- **Formato wheels**: 9 archivos `.whl`
- **Distribuciones fuente**: 9 archivos `.tar.gz`
- **Scripts de build**: 3 (verify_versions, build_all.sh, build_all.bat)
- **Scripts de instalación**: 3 (install.sh, install.bat, verify_installation)
- **Documentación**: 12+ archivos markdown
- **Compatibilidad**: Python >= 3.8
- **Plataformas**: Linux, macOS, Windows

---

### 🎓 Principios SOLID Aplicados

- **✅ S (SRP)**: Factories especializados, CargadorConfig separado
- **✅ O (OCP)**: Extensible mediante config JSON sin modificar código
- **✅ L (LSP)**: Jerarquía SenialBase con intercambiabilidad garantizada
- **✅ I (ISP)**: Interfaces segregadas (BaseAuditor, BaseTrazador)
- **✅ D (DIP)**: **Configuración externa JSON determina TODAS las dependencias**

---

### 🚀 Instalación y Uso

#### Build
```bash
./packaging/build/build_all.sh  # Linux/macOS
packaging\build\build_all.bat   # Windows
```

#### Instalación
```bash
./packaging/install/install.sh  # Linux/macOS
packaging\install\install.bat   # Windows
```

#### Uso
```bash
senial-solid  # Comando directo
python -m lanzador.lanzador  # Como módulo
```

---

### 📚 Migración desde v5.x

#### Cambios BREAKING en Configurador

**Antes (v2.2.0)**:
```python
from configurador import Configurador

# Métodos específicos hardcoded
senial = Configurador.crear_senial_lista(20)
adq = Configurador.crear_adquisidor_archivo(senial, "./datos.txt")
```

**Ahora (v3.0.0)**:
```python
from configurador import Configurador

# 1. Inicializar con config JSON
Configurador.inicializar_configuracion()  # Usa config.json del paquete

# 2. Crear componentes (configurados desde JSON)
senial = Configurador.crear_senial_adquisidor()
adq = Configurador.crear_adquisidor()
```

#### Ventajas
- ✅ Cambiar comportamiento editando JSON, no código
- ✅ Diferentes configs para dev/test/prod
- ✅ Configuración versionable en git
- ✅ DIP completo aplicado

---

### 🔗 Enlaces

- **Repositorio**: https://github.com/vvalotto/Senial_SOLID_IS
- **Documentación**: `docs/`
- **Plan de Paquetización**: `docs/PLAN_PAQUETIZACION_PASO_A_PASO.md`
- **Licencia**: MIT

---

### 👨‍💻 Autor

**Victor Valotto** - vvalotto@gmail.com

---

### 📅 Fechas

- **Inicio v6.0.0**: 2025-10-03
- **Release v6.0.0**: 2025-10-04
- **Duración**: 2 días (DIP + Factories + Build infrastructure)

---

**Estado**: ✅ **RELEASE COMPLETO - v6.0.0**
