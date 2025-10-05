# Senial SOLID v6.0.0 - DIP Completo con Bundle de Instalación Simplificada

Release mayor que implementa **DIP completo** con configuración externa JSON, **Factories especializados** delegados, y **bundle auto-contenido** para instalación simplificada.

## 🎯 Características Principales

### ✨ DIP y Configuración Externa
- **CargadorConfig** con ruta dinámica basada en `__file__`
- **config.json** incluido en paquete configurador y en bundle
- Inicialización automática desde JSON en `Configurador.inicializar_configuracion()`
- Configuración versionable y portable

### 🏭 Factories Especializados
- **FactorySenial** - Crea SenialLista, SenialPila, SenialCola
- **FactoryAdquisidor** - Crea adquisidores según configuración
- **FactoryProcesador** - Crea procesadores según configuración
- **FactoryContexto** - Crea contextos de persistencia

### 📦 Bundle de Instalación Auto-Contenido
- **Archivo único**: `senial_solid-v6.0.0.tar.gz` (~64KB)
- **Contenido completo**: Todos los wheels + config.json + instalador
- **Instalación simplificada**: Descomprimir y ejecutar `./install.sh`
- **Sin dependencias externas**: Todo incluido en el bundle

## 🚀 Instalación Rápida

### Desde GitHub Release (Recomendado)

```bash
# 1. Descargar bundle
curl -L -O https://github.com/vvalotto/Senial_SOLID_IS/releases/download/v6.0.0/senial_solid-v6.0.0.tar.gz

# 2. Descomprimir
tar -xzf senial_solid-v6.0.0.tar.gz
cd senial_solid-v6.0.0

# 3. Instalar
./install.sh

# 4. Activar y ejecutar
source senial_env/bin/activate
senial-solid
```

El instalador automáticamente:
- ✅ Crea entorno virtual `senial_env`
- ✅ Instala todos los paquetes
- ✅ Configura `~/.senial_solid/` con config.json y directorios

### Desde Código Fuente (Desarrollo)

```bash
git clone https://github.com/vvalotto/Senial_SOLID_IS.git
cd Senial_SOLID_IS

# Build y crear bundle
./packaging/build/build_all.sh
./packaging/build/create_bundle.sh

# Instalar desde el repositorio
./packaging/install/install.sh
```

## 📋 Componentes Incluidos

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **senial-solid** | 6.0.0 | Meta-paquete (instala todos) |
| **lanzador** | 6.0.0 | Orquestador principal |
| **configurador** | 3.0.0 | Factory con config JSON (DIP) |
| **persistidor-senial** | 7.0.0 | Persistencia con Repository |
| **dominio-senial** | 5.0.0 | Entidades del dominio |
| **adquisicion-senial** | 3.0.0 | Adquisidores de señales |
| **procesamiento-senial** | 3.0.0 | Procesadores de señales |
| **presentacion-senial** | 2.0.0 | Visualización |
| **supervisor** | 1.0.0 | Auditoría y trazabilidad (ISP) |

## 🎓 Principios SOLID Aplicados

- **✅ S (SRP)**: Factories especializados, CargadorConfig separado
- **✅ O (OCP)**: Extensible mediante config JSON sin modificar código
- **✅ L (LSP)**: Jerarquía SenialBase con intercambiabilidad garantizada
- **✅ I (ISP)**: Interfaces segregadas (BaseAuditor, BaseTrazador)
- **✅ D (DIP)**: Configuración externa JSON determina TODAS las dependencias

## 📚 Documentación

- [README principal](https://github.com/vvalotto/Senial_SOLID_IS/blob/main/README.md)
- [CHANGELOG completo](https://github.com/vvalotto/Senial_SOLID_IS/blob/main/CHANGELOG_v6.0.0.md)
- [Plan de Paquetización](https://github.com/vvalotto/Senial_SOLID_IS/blob/main/docs/PLAN_PAQUETIZACION_PASO_A_PASO.md)

## ⚙️ Requisitos

- Python >= 3.8
- pip
- Linux o macOS (instalador bash)

## 🔗 Enlaces

- **Repositorio**: https://github.com/vvalotto/Senial_SOLID_IS
- **Licencia**: MIT
- **Autor**: Victor Valotto - vvalotto@gmail.com

---

**Fecha de Release**: 2025-10-04
**Tag**: v6.0.0
