# Guía para crear GitHub Release v6.0.0

Esta guía explica cómo crear el release en GitHub y subir los artefactos.

## Paso 1: Build de los artefactos

```bash
# Ejecutar build completo
./packaging/build/build_all.sh

# Verificar que se generaron 9 wheels + 9 source distributions
ls packaging/release/wheels/
ls packaging/release/source/
```

## Paso 2: Crear el Release en GitHub

### Opción A: Interfaz Web

1. Ir a: https://github.com/vvalotto/Senial_SOLID_IS/releases/new

2. **Tag version**: `v6.0.0`
   - Crear nuevo tag desde `main` branch

3. **Release title**: `v6.0.0 - DIP Completo con Paquetización Multiplataforma`

4. **Description**: (copiar el texto de abajo)

5. **Attach binaries**: Subir los 9 wheels:
   - `packaging/release/wheels/supervisor-1.0.0-py3-none-any.whl`
   - `packaging/release/wheels/dominio_senial-5.0.0-py3-none-any.whl`
   - `packaging/release/wheels/adquisicion_senial-3.0.0-py3-none-any.whl`
   - `packaging/release/wheels/procesamiento_senial-3.0.0-py3-none-any.whl`
   - `packaging/release/wheels/presentacion_senial-2.0.0-py3-none-any.whl`
   - `packaging/release/wheels/persistidor_senial-7.0.0-py3-none-any.whl`
   - `packaging/release/wheels/configurador-3.0.0-py3-none-any.whl`
   - `packaging/release/wheels/lanzador-6.0.0-py3-none-any.whl`
   - `packaging/release/wheels/senial_solid-6.0.0-py3-none-any.whl`

6. Marcar como **Latest release**

7. Click en **Publish release**

### Opción B: GitHub CLI

```bash
# Instalar gh CLI si no lo tienes: https://cli.github.com/

# Autenticarse
gh auth login

# Crear release y subir wheels
gh release create v6.0.0 \
  --title "v6.0.0 - DIP Completo con Paquetización Multiplataforma" \
  --notes-file packaging/RELEASE_NOTES.md \
  packaging/release/wheels/*.whl
```

---

## Texto para la Descripción del Release

```markdown
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
```

---

## Paso 3: Verificar el Release

Después de publicar, verificar:

1. **URL del release**: https://github.com/vvalotto/Senial_SOLID_IS/releases/tag/v6.0.0

2. **Probar instalación remota**:
```bash
curl -sSL https://raw.githubusercontent.com/vvalotto/Senial_SOLID_IS/main/packaging/install/install_from_github.sh | bash
```

3. **Verificar que los wheels se descarguen**:
```bash
curl -L -O https://github.com/vvalotto/Senial_SOLID_IS/releases/download/v6.0.0/senial_solid-6.0.0-py3-none-any.whl
```

## Paso 4: Actualizar README principal

Agregar badge y sección de instalación en README.md:

```markdown
[![Release](https://img.shields.io/github/v/release/vvalotto/Senial_SOLID_IS)](https://github.com/vvalotto/Senial_SOLID_IS/releases/latest)

## Instalación

### Desde GitHub Release
\```bash
curl -sSL https://raw.githubusercontent.com/vvalotto/Senial_SOLID_IS/main/packaging/install/install_from_github.sh | bash
\```
```

## Troubleshooting

### Error: "Could not find release v6.0.0"
- Verificar que el release esté publicado
- Verificar que el tag sea exactamente `v6.0.0`

### Error descargando wheels
- Verificar que los 9 wheels estén adjuntos al release
- Verificar que el repositorio sea público o tengas acceso

### Permisos de curl
Si el script falla con permisos:
```bash
# Descargar y ejecutar manualmente
curl -sSL https://raw.githubusercontent.com/vvalotto/Senial_SOLID_IS/main/packaging/install/install_from_github.sh -o install.sh
chmod +x install.sh
./install.sh
```
