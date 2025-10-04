# Senial SOLID v6.0.0 - DIP Completo con Paquetización Multiplataforma

Release mayor que implementa **DIP completo** con configuración externa JSON, **Factories especializados** delegados, y **infraestructura completa de build y distribución multiplataforma**.

## 🎯 Características Principales

### ✨ DIP y Configuración Externa
- **CargadorConfig** con ruta dinámica basada en `__file__`
- **config.json** como configuración externa del sistema
- Inicialización desde JSON en `Configurador.inicializar_configuracion()`
- Configuración versionable y portable

### 🏭 Factories Especializados
- **FactorySenial** - Crea SenialLista, SenialPila, SenialCola
- **FactoryAdquisidor** - Crea adquisidores según configuración
- **FactoryProcesador** - Crea procesadores según configuración
- **FactoryContexto** - Crea contextos de persistencia

### 📦 Infraestructura de Build y Distribución
- **Meta-paquete senial-solid** - Instala todo el sistema con un comando
- Scripts de build para Linux/macOS y Windows
- Scripts de instalación multiplataforma
- Instalación remota desde GitHub Release

## 🚀 Instalación Rápida

### Desde GitHub Release (recomendado)

```bash
curl -sSL https://raw.githubusercontent.com/vvalotto/Senial_SOLID_IS/main/packaging/install/install_from_github.sh | bash
```

### Instalación Manual

```bash
# Descargar wheels de este release
# Luego instalar:
pip install senial_solid-6.0.0-py3-none-any.whl
```

### Desde Código Fuente

```bash
git clone https://github.com/vvalotto/Senial_SOLID_IS.git
cd Senial_SOLID_IS
./packaging/build/build_all.sh
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
- pip >= 21.0
- Linux, macOS o Windows

## 🔗 Enlaces

- **Repositorio**: https://github.com/vvalotto/Senial_SOLID_IS
- **Licencia**: MIT
- **Autor**: Victor Valotto - vvalotto@gmail.com

---

**Fecha de Release**: 2025-10-04
**Tag**: v6.0.0
