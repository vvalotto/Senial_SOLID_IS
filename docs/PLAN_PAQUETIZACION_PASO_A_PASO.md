# Plan de Paquetización Paso a Paso - Senial SOLID v6.0.0

**Proyecto**: Senial SOLID IS
**Autor**: Victor Valotto
**Fecha**: Octubre 2024
**Versión**: 6.0.0
**Objetivo**: Plan de ejecución completo para crear scripts de build, instalación y meta-paquete

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Prerrequisitos](#prerrequisitos)
3. [Fase 1: Preparación del Entorno](#fase-1-preparación-del-entorno)
4. [Fase 2: Script de Verificación de Versiones](#fase-2-script-de-verificación-de-versiones)
5. [Fase 3: Scripts de Build](#fase-3-scripts-de-build)
6. [Fase 4: Meta-Paquete](#fase-4-meta-paquete)
7. [Fase 5: Scripts de Instalación](#fase-5-scripts-de-instalación)
8. [Fase 6: Script de Verificación](#fase-6-script-de-verificación)
9. [Fase 7: Pruebas y Validación](#fase-7-pruebas-y-validación)
10. [Fase 8: Documentación Final](#fase-8-documentación-final)

---

## 🎯 Visión General

### Objetivo Final

Crear una estructura completa de distribución que incluya:

```
Senial_SOLID_IS/
├── build/                     ✅ Scripts de construcción
├── install/                   ✅ Scripts de instalación
├── senial_solid_metapackage/  ✅ Meta-paquete
└── release/                   ✅ Distribución final (generado)
```

### Tiempo Estimado

- **Total**: 4-6 horas
- **Fase 1-2**: 30 minutos
- **Fase 3**: 1 hora
- **Fase 4**: 1 hora
- **Fase 5**: 1 hora
- **Fase 6**: 30 minutos
- **Fase 7**: 1 hora
- **Fase 8**: 30 minutos

---

## ✅ Prerrequisitos

### Software Requerido

- [ ] Python 3.8 o superior instalado
- [ ] pip actualizado (`python -m pip install --upgrade pip`)
- [ ] Git instalado
- [ ] Editor de texto (VS Code, Vim, nano, etc.)

### Verificación de Prerrequisitos

```bash
# Ejecutar estos comandos para verificar:
python3 --version          # Debe mostrar >= 3.8
pip --version              # Debe estar instalado
git --version              # Debe estar instalado

# Instalar herramientas de build
pip install --upgrade setuptools wheel build
```

### Estado del Proyecto

- [ ] Proyecto en estado v6.0.0 (commit actual)
- [ ] Todos los paquetes tienen setup.py configurado
- [ ] Documentación en docs/ actualizada
- [ ] config.json en configurador/ presente

---

## 📂 Fase 1: Preparación del Entorno

**Tiempo estimado**: 15 minutos

### Paso 1.1: Crear Estructura de Directorios

```bash
# Ubicarse en raíz del proyecto
cd /Users/victor/PycharmProjects/Senial_SOLID_IS

# Crear directorios
mkdir -p build
mkdir -p install
mkdir -p senial_solid_metapackage/senial_solid
mkdir -p senial_solid_metapackage/config
```

**Verificación:**
```bash
ls -la | grep -E "(build|install|senial_solid_metapackage)"
```

**Resultado esperado:**
```
drwxr-xr-x  build/
drwxr-xr-x  install/
drwxr-xr-x  senial_solid_metapackage/
```

### Paso 1.2: Crear .gitignore para Nuevos Directorios

```bash
# Agregar a .gitignore
cat >> .gitignore << 'EOF'

# Build artifacts
build/__pycache__/
*.pyc

# Release directory (generado)
release/

# Virtual environments de prueba
test_env/
senial_env/

EOF
```

**Verificación:**
```bash
cat .gitignore | grep -A 5 "Build artifacts"
```

---

## 🔍 Fase 2: Script de Verificación de Versiones

**Tiempo estimado**: 30 minutos

### Paso 2.1: Crear `build/verify_versions.py`

**Comando:**
```bash
cat > build/verify_versions.py << 'SCRIPT_EOF'
#!/usr/bin/env python3
"""
Script de verificación de versiones de paquetes.
Verifica consistencia entre setup.py de todos los paquetes.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[0;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

class VersionVerifier:
    """Verificador de versiones de paquetes"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.packages = [
            ("supervisor", "supervisor"),
            ("dominio_senial", "dominio-senial"),
            ("adquisicion_senial", "adquisicion-senial"),
            ("procesamiento_senial", "procesamiento-senial"),
            ("presentacion_senial", "presentacion-senial"),
            ("persistidor_senial", "persistidor-senial"),
            ("configurador", "configurador"),
            ("lanzador", "lanzador"),
        ]
        self.versions = {}
        self.dependencies = {}
        self.errors = []

    def extract_version(self, setup_path: Path) -> str:
        """Extraer versión de setup.py"""
        if not setup_path.exists():
            return None

        content = setup_path.read_text()

        # Buscar version="X.Y.Z"
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)

        return None

    def extract_dependencies(self, setup_path: Path) -> List[str]:
        """Extraer install_requires de setup.py"""
        if not setup_path.exists():
            return []

        content = setup_path.read_text()

        # Buscar install_requires=[...]
        match = re.search(
            r'install_requires\s*=\s*\[(.*?)\]',
            content,
            re.DOTALL
        )

        if not match:
            return []

        deps_text = match.group(1)

        # Extraer cada dependencia
        deps = []
        for line in deps_text.split('\n'):
            line = line.strip().strip(',').strip('"').strip("'")
            if line and not line.startswith('#'):
                deps.append(line)

        return deps

    def verify_all_packages(self):
        """Verificar todas las versiones"""
        print(f"{Colors.BLUE}==>{Colors.NC} Verificando versiones de paquetes...\n")

        for dir_name, package_name in self.packages:
            setup_path = self.root_dir / dir_name / "setup.py"

            version = self.extract_version(setup_path)
            if version:
                self.versions[package_name] = version
                print(f"  {Colors.GREEN}✓{Colors.NC} {package_name}: v{version}")
            else:
                error = f"No se encontró versión en {setup_path}"
                self.errors.append(error)
                print(f"  {Colors.RED}✗{Colors.NC} {package_name}: {error}")

            deps = self.extract_dependencies(setup_path)
            if deps:
                self.dependencies[package_name] = deps

    def check_dependency_consistency(self):
        """Verificar consistencia de dependencias"""
        print(f"\n{Colors.BLUE}==>{Colors.NC} Verificando consistencia de dependencias...\n")

        for package, deps in self.dependencies.items():
            for dep in deps:
                # Parsear dependencia (ej: "dominio-senial>=5.0.0")
                match = re.match(r'([a-z-]+)([><=]+)([0-9.]+)', dep)
                if not match:
                    continue

                dep_name = match.group(1)
                operator = match.group(2)
                required_version = match.group(3)

                if dep_name not in self.versions:
                    continue

                actual_version = self.versions[dep_name]

                # Verificación simple (solo para >=)
                if operator == ">=":
                    if self._compare_versions(actual_version, required_version) >= 0:
                        print(f"  {Colors.GREEN}✓{Colors.NC} {package} requiere "
                              f"{dep_name}>={required_version} (actual: {actual_version})")
                    else:
                        error = (f"{package} requiere {dep_name}>={required_version} "
                                f"pero versión actual es {actual_version}")
                        self.errors.append(error)
                        print(f"  {Colors.RED}✗{Colors.NC} {error}")

    def _compare_versions(self, v1: str, v2: str) -> int:
        """Comparar versiones (v1 vs v2). Retorna: 1 si v1>v2, 0 si igual, -1 si v1<v2"""
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]

        for i in range(max(len(v1_parts), len(v2_parts))):
            p1 = v1_parts[i] if i < len(v1_parts) else 0
            p2 = v2_parts[i] if i < len(v2_parts) else 0

            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1

        return 0

    def print_report(self):
        """Imprimir reporte final"""
        print("\n" + "=" * 60)

        if self.errors:
            print(f"{Colors.RED}✗ Verificación FALLÓ{Colors.NC}")
            print(f"\n{Colors.RED}Errores encontrados:{Colors.NC}")
            for error in self.errors:
                print(f"  • {error}")
            return False
        else:
            print(f"{Colors.GREEN}✓ Todas las versiones son consistentes{Colors.NC}")
            return True

    def run(self) -> bool:
        """Ejecutar verificación completa"""
        print("=" * 60)
        print("  Verificación de Versiones - Senial SOLID v6.0.0")
        print("=" * 60)
        print()

        self.verify_all_packages()
        self.check_dependency_consistency()
        success = self.print_report()

        print("=" * 60)
        print()

        return success

if __name__ == "__main__":
    import sys
    verifier = VersionVerifier()
    success = verifier.run()
    sys.exit(0 if success else 1)
SCRIPT_EOF

chmod +x build/verify_versions.py
```

### Paso 2.2: Probar el Script de Verificación

```bash
# Ejecutar
python3 build/verify_versions.py
```

**Resultado esperado:**
```
============================================================
  Verificación de Versiones - Senial SOLID v6.0.0
============================================================

==> Verificando versiones de paquetes...

  ✓ supervisor: v1.0.0
  ✓ dominio-senial: v5.0.0
  ✓ adquisicion-senial: v3.0.0
  ✓ procesamiento-senial: v3.0.0
  ✓ presentacion-senial: v2.0.0
  ✓ persistidor-senial: v7.0.0
  ✓ configurador: v3.0.0
  ✓ lanzador: v6.0.0

==> Verificando consistencia de dependencias...

  ✓ adquisicion-senial requiere dominio-senial>=5.0.0 (actual: 5.0.0)
  ...

============================================================
✓ Todas las versiones son consistentes
============================================================
```

**Checklist Fase 2:**
- [ ] Script verify_versions.py creado
- [ ] Script ejecutable (`chmod +x`)
- [ ] Ejecución exitosa sin errores
- [ ] Todas las versiones detectadas correctamente

---

## 🔨 Fase 3: Scripts de Build

**Tiempo estimado**: 1 hora

### Paso 3.1: Crear `build/build_all.sh` (Linux/macOS)

```bash
cat > build/build_all.sh << 'SCRIPT_EOF'
#!/bin/bash
# build_all.sh - Build de todos los paquetes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
RELEASE_DIR="$ROOT_DIR/release"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_step() { echo -e "${BLUE}==>${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

clean_previous_build() {
    print_step "Limpiando builds anteriores..."

    for dir in dominio_senial adquisicion_senial procesamiento_senial \
               presentacion_senial persistidor_senial supervisor \
               configurador lanzador senial_solid_metapackage; do
        if [ -d "$ROOT_DIR/$dir" ]; then
            rm -rf "$ROOT_DIR/$dir/dist"
            rm -rf "$ROOT_DIR/$dir/build"
            rm -rf "$ROOT_DIR/$dir"/*.egg-info
        fi
    done

    rm -rf "$RELEASE_DIR"
    print_success "Limpieza completada"
}

create_release_structure() {
    print_step "Creando estructura de release..."
    mkdir -p "$RELEASE_DIR"/{wheels,source,config,docs,scripts}
    print_success "Estructura creada"
}

verify_versions() {
    print_step "Verificando versiones..."
    python3 "$SCRIPT_DIR/verify_versions.py" || exit 1
    print_success "Versiones verificadas"
}

build_package() {
    local package_dir=$1
    local package_name=$2

    print_step "Building $package_name..."
    cd "$ROOT_DIR/$package_dir"
    python3 -m build || exit 1

    cp dist/*.whl "$RELEASE_DIR/wheels/" 2>/dev/null || true
    cp dist/*.tar.gz "$RELEASE_DIR/source/" 2>/dev/null || true

    print_success "$package_name built"
    cd "$ROOT_DIR"
}

check_build_tools() {
    print_step "Verificando herramientas..."
    python3 -m pip install --upgrade pip setuptools wheel build --quiet
    print_success "Herramientas verificadas"
}

main() {
    echo "================================================"
    echo "  Build de Senial SOLID v6.0.0"
    echo "================================================"
    echo ""

    check_build_tools
    verify_versions
    clean_previous_build
    create_release_structure

    print_step "Iniciando build de paquetes..."
    echo ""

    build_package "supervisor" "supervisor"
    build_package "dominio_senial" "dominio-senial"
    build_package "adquisicion_senial" "adquisicion-senial"
    build_package "procesamiento_senial" "procesamiento-senial"
    build_package "presentacion_senial" "presentacion-senial"
    build_package "persistidor_senial" "persistidor-senial"
    build_package "configurador" "configurador"
    build_package "lanzador" "lanzador"
    build_package "senial_solid_metapackage" "senial-solid"

    print_step "Copiando archivos adicionales..."
    cp "$ROOT_DIR/configurador/config.json" "$RELEASE_DIR/config/" 2>/dev/null || true
    cp "$ROOT_DIR/docs/"*.md "$RELEASE_DIR/docs/" 2>/dev/null || true
    cp "$ROOT_DIR/README.md" "$RELEASE_DIR/" 2>/dev/null || true
    cp "$ROOT_DIR/LICENSE" "$RELEASE_DIR/" 2>/dev/null || true
    print_success "Archivos copiados"

    echo ""
    echo "================================================"
    print_success "Build completado"
    echo "================================================"
    echo ""
    echo "📦 Wheels: $(ls -1 $RELEASE_DIR/wheels/*.whl 2>/dev/null | wc -l) archivos"
    echo "📦 Source: $(ls -1 $RELEASE_DIR/source/*.tar.gz 2>/dev/null | wc -l) archivos"
    echo "📁 Ubicación: $RELEASE_DIR"
    echo ""
}

main
SCRIPT_EOF

chmod +x build/build_all.sh
```

### Paso 3.2: Crear `build/build_all.bat` (Windows)

```bash
cat > build/build_all.bat << 'SCRIPT_EOF'
@echo off
REM build_all.bat - Build Windows

setlocal enabledelayedexpansion
set "ROOT_DIR=%~dp0.."
set "RELEASE_DIR=%ROOT_DIR%\release"

echo ================================================
echo   Build de Senial SOLID v6.0.0
echo ================================================
echo.

python --version >nul 2>&1 || (
    echo ERROR: Python no encontrado
    exit /b 1
)

echo ==^> Instalando herramientas...
python -m pip install --upgrade pip setuptools wheel build --quiet
echo OK Herramientas instaladas

echo ==^> Verificando versiones...
python "%ROOT_DIR%\build\verify_versions.py" || exit /b 1
echo OK Versiones verificadas

echo ==^> Limpiando builds anteriores...
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
echo OK Limpieza completada

echo ==^> Creando estructura...
mkdir "%RELEASE_DIR%\wheels"
mkdir "%RELEASE_DIR%\source"
mkdir "%RELEASE_DIR%\config"
mkdir "%RELEASE_DIR%\docs"
mkdir "%RELEASE_DIR%\scripts"
echo OK Estructura creada

goto :main

:build_package
set "package_dir=%~1"
set "package_name=%~2"
echo ==^> Building %package_name%...
cd "%ROOT_DIR%\%package_dir%"
python -m build || exit /b 1
if exist "dist\*.whl" copy "dist\*.whl" "%RELEASE_DIR%\wheels\" >nul
if exist "dist\*.tar.gz" copy "dist\*.tar.gz" "%RELEASE_DIR%\source\" >nul
echo OK %package_name% built
cd "%ROOT_DIR%"
goto :eof

:main
echo ==^> Iniciando build...
call :build_package "supervisor" "supervisor"
call :build_package "dominio_senial" "dominio-senial"
call :build_package "adquisicion_senial" "adquisicion-senial"
call :build_package "procesamiento_senial" "procesamiento-senial"
call :build_package "presentacion_senial" "presentacion-senial"
call :build_package "persistidor_senial" "persistidor-senial"
call :build_package "configurador" "configurador"
call :build_package "lanzador" "lanzador"
call :build_package "senial_solid_metapackage" "senial-solid"

echo ==^> Copiando archivos adicionales...
copy "%ROOT_DIR%\configurador\config.json" "%RELEASE_DIR%\config\" >nul 2>nul
copy "%ROOT_DIR%\README.md" "%RELEASE_DIR%\" >nul 2>nul
copy "%ROOT_DIR%\LICENSE" "%RELEASE_DIR%\" >nul 2>nul
echo OK Archivos copiados

echo ================================================
echo OK Build completado
echo ================================================

endlocal
SCRIPT_EOF
```

**Checklist Fase 3:**
- [ ] build_all.sh creado y ejecutable
- [ ] build_all.bat creado (Windows)
- [ ] Scripts verificados sintácticamente

---

## 📦 Fase 4: Meta-Paquete

**Tiempo estimado**: 1 hora

### Paso 4.1: Crear Estructura del Meta-Paquete

```bash
# Ya existe de Paso 1.1, verificar:
ls -la senial_solid_metapackage/
```

### Paso 4.2: Crear `senial_solid_metapackage/setup.py`

```bash
cat > senial_solid_metapackage/setup.py << 'SETUP_EOF'
from setuptools import setup, find_packages
import os

def read_long_description():
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, encoding='utf-8') as f:
            return f.read()
    return "Sistema completo de procesamiento de señales con principios SOLID"

setup(
    name="senial-solid",
    version="6.0.0",
    description="Sistema completo de procesamiento de señales con principios SOLID aplicados",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/Senial_SOLID_IS/issues",
        "Documentation": "https://github.com/vvalotto/Senial_SOLID_IS/tree/main/docs",
        "Source Code": "https://github.com/vvalotto/Senial_SOLID_IS",
    },
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "lanzador>=6.0.0",
    ],
    entry_points={
        'console_scripts': [
            'senial-solid=lanzador.lanzador:ejecutar',
        ],
    },
    include_package_data=True,
    package_data={
        'senial_solid': ['config/*.json'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ],
    keywords="solid principles signal-processing architecture design-patterns",
    zip_safe=False,
)
SETUP_EOF
```

### Paso 4.3: Crear `senial_solid_metapackage/senial_solid/__init__.py`

```bash
cat > senial_solid_metapackage/senial_solid/__init__.py << 'INIT_EOF'
"""
Senial SOLID - Sistema de Procesamiento de Señales

Meta-paquete que instala el sistema completo.

Componentes:
- dominio-senial (v5.0.0)
- adquisicion-senial (v3.0.0)
- procesamiento-senial (v3.0.0)
- presentacion-senial (v2.0.0)
- persistidor-senial (v7.0.0)
- supervisor (v1.0.0)
- configurador (v3.0.0)
- lanzador (v6.0.0)
"""

__version__ = "6.0.0"
__author__ = "Victor Valotto"
__email__ = "vvalotto@gmail.com"
__license__ = "MIT"

__all__ = ['__version__', '__author__', '__email__', '__license__']
INIT_EOF
```

### Paso 4.4: Crear `senial_solid_metapackage/README.md`

```bash
cat > senial_solid_metapackage/README.md << 'README_EOF'
# Senial SOLID - Sistema de Procesamiento de Señales

Sistema completo de procesamiento de señales digitales con **principios SOLID aplicados**.

## Instalación

```bash
pip install senial-solid
```

## Uso

```bash
# Comando directo
senial-solid

# O como módulo
python -m lanzador.lanzador
```

## Componentes Instalados

- dominio-senial (v5.0.0)
- adquisicion-senial (v3.0.0)
- procesamiento-senial (v3.0.0)
- presentacion-senial (v2.0.0)
- persistidor-senial (v7.0.0)
- supervisor (v1.0.0)
- configurador (v3.0.0)
- lanzador (v6.0.0)

## Documentación

https://github.com/vvalotto/Senial_SOLID_IS

## Licencia

MIT
README_EOF
```

### Paso 4.5: Crear `senial_solid_metapackage/MANIFEST.in`

```bash
cat > senial_solid_metapackage/MANIFEST.in << 'MANIFEST_EOF'
include README.md
include LICENSE
recursive-include config *.json
MANIFEST_EOF
```

### Paso 4.6: Copiar LICENSE al Meta-Paquete

```bash
cp LICENSE senial_solid_metapackage/
```

### Paso 4.7: Copiar config.json de Ejemplo

```bash
cp configurador/config.json senial_solid_metapackage/config/
```

### Paso 4.8: Crear `senial_solid_metapackage/pyproject.toml`

```bash
cat > senial_solid_metapackage/pyproject.toml << 'TOML_EOF'
[build-system]
requires = ["setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "senial-solid"
version = "6.0.0"
description = "Sistema completo de procesamiento de señales con principios SOLID"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [{name = "Victor Valotto", email = "vvalotto@gmail.com"}]
keywords = ["solid", "principles", "signal-processing"]

dependencies = ["lanzador>=6.0.0"]

[project.scripts]
senial-solid = "lanzador.lanzador:ejecutar"

[project.urls]
Homepage = "https://github.com/vvalotto/Senial_SOLID_IS"
TOML_EOF
```

**Checklist Fase 4:**
- [ ] setup.py creado
- [ ] __init__.py creado
- [ ] README.md creado
- [ ] MANIFEST.in creado
- [ ] LICENSE copiado
- [ ] config.json copiado
- [ ] pyproject.toml creado

---

## 🔧 Fase 5: Scripts de Instalación

**Tiempo estimado**: 1 hora

### Paso 5.1: Crear `install/install.sh` (Linux/macOS)

**NOTA**: Este es un script largo. Se creará por partes.

```bash
cat > install/install.sh << 'INSTALL_EOF'
#!/bin/bash
# install.sh - Instalación de Senial SOLID

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
RELEASE_DIR="$ROOT_DIR/release"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() { echo -e "${BLUE}==>${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

check_python() {
    print_step "Verificando Python..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no encontrado"
        exit 1
    fi
    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python $python_version detectado"
}

check_pip() {
    print_step "Verificando pip..."
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip no encontrado"
        exit 1
    fi
    print_success "pip encontrado"
}

ask_venv() {
    echo ""
    echo "¿Desea instalar en un entorno virtual? (recomendado)"
    echo "  [Y] Sí - Crear entorno virtual 'senial_env'"
    echo "  [N] No - Instalar en sistema"
    read -p "Selección [Y/n]: " choice
    case "$choice" in n|N) return 1 ;; *) return 0 ;; esac
}

create_venv() {
    print_step "Creando entorno virtual 'senial_env'..."
    python3 -m venv senial_env
    source senial_env/bin/activate
    print_success "Entorno virtual creado y activado"
}

install_from_wheels() {
    print_step "Instalando paquetes desde wheels..."

    if [ ! -d "$RELEASE_DIR/wheels" ]; then
        print_error "Directorio wheels no encontrado"
        print_warning "Ejecute primero: ./build/build_all.sh"
        exit 1
    fi

    python3 -m pip install --upgrade pip --quiet

    pip install "$RELEASE_DIR/wheels/supervisor"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/dominio_senial"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/adquisicion_senial"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/procesamiento_senial"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/presentacion_senial"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/persistidor_senial"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/configurador"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/lanzador"*.whl --quiet
    pip install "$RELEASE_DIR/wheels/senial_solid"*.whl --quiet

    print_success "Todos los paquetes instalados"
}

setup_config() {
    print_step "Configurando directorio de trabajo..."
    mkdir -p ~/.senial_solid
    if [ -f "$RELEASE_DIR/config/config.json" ]; then
        cp "$RELEASE_DIR/config/config.json" ~/.senial_solid/config.json
        print_success "Configuración copiada a: ~/.senial_solid/config.json"
    fi
    mkdir -p ~/.senial_solid/tmp/datos/adquisicion
    mkdir -p ~/.senial_solid/tmp/datos/procesamiento
    print_success "Directorio de trabajo configurado"
}

verify_installation() {
    print_step "Verificando instalación..."
    python3 -c "from dominio_senial import SenialBase" 2>/dev/null && print_success "dominio_senial OK"
    python3 -c "from configurador import Configurador" 2>/dev/null && print_success "configurador OK"
    python3 -c "from lanzador import Lanzador" 2>/dev/null && print_success "lanzador OK"
    return 0
}

show_summary() {
    echo ""
    echo "================================================"
    print_success "Instalación completada"
    echo "================================================"
    echo ""
    echo "🚀 Ejecutar: senial-solid"
    echo "   o: python -m lanzador.lanzador"
    echo ""
    echo "📁 Config: ~/.senial_solid/config.json"
    echo ""
}

main() {
    echo "================================================"
    echo "  Instalación de Senial SOLID v6.0.0"
    echo "================================================"
    echo ""

    check_python
    check_pip

    if ask_venv; then
        create_venv
    fi

    install_from_wheels
    setup_config
    verify_installation
    show_summary
}

main
INSTALL_EOF

chmod +x install/install.sh
```

### Paso 5.2: Crear `install/install.bat` (Windows CMD)

```bash
cat > install/install.bat << 'INSTALL_BAT_EOF'
@echo off
REM install.bat - Instalación Windows

setlocal
set "ROOT_DIR=%~dp0.."
set "RELEASE_DIR=%ROOT_DIR%\release"

echo ================================================
echo   Instalacion de Senial SOLID v6.0.0
echo ================================================
echo.

python --version >nul 2>&1 || (
    echo ERROR: Python no encontrado
    exit /b 1
)

echo ==^> Instalando paquetes...
python -m pip install --upgrade pip --quiet

for %%p in (supervisor dominio_senial adquisicion_senial procesamiento_senial ^
            presentacion_senial persistidor_senial configurador lanzador senial_solid) do (
    echo Instalando %%p...
    for %%f in ("%RELEASE_DIR%\wheels\%%p*.whl") do (
        python -m pip install "%%f" --quiet
    )
)

echo OK Paquetes instalados

echo ==^> Configurando...
if not exist "%USERPROFILE%\.senial_solid" mkdir "%USERPROFILE%\.senial_solid"
if exist "%RELEASE_DIR%\config\config.json" (
    copy "%RELEASE_DIR%\config\config.json" "%USERPROFILE%\.senial_solid\" >nul
)
echo OK Configuracion completada

echo ================================================
echo OK Instalacion completada
echo ================================================
echo.
echo Ejecutar: senial-solid
echo.

endlocal
INSTALL_BAT_EOF
```

**Checklist Fase 5:**
- [ ] install.sh creado y ejecutable
- [ ] install.bat creado

---

## ✅ Fase 6: Script de Verificación

**Tiempo estimado**: 30 minutos

### Paso 6.1: Crear `install/verify_installation.py`

```bash
cat > install/verify_installation.py << 'VERIFY_EOF'
#!/usr/bin/env python3
"""Script de verificación de instalación"""

import sys

def verificar():
    print("=" * 60)
    print("  Verificación de Instalación - Senial SOLID v6.0.0")
    print("=" * 60)
    print()

    componentes = [
        'dominio_senial',
        'adquisicion_senial',
        'procesamiento_senial',
        'presentacion_senial',
        'persistidor_senial',
        'supervisor',
        'configurador',
        'lanzador'
    ]

    errors = 0

    for comp in componentes:
        try:
            __import__(comp)
            print(f"✓ {comp}")
        except ImportError as e:
            print(f"✗ {comp} - ERROR: {e}")
            errors += 1

    print()
    print("=" * 60)

    if errors == 0:
        print("✓ Todos los componentes instalados correctamente")
        return 0
    else:
        print(f"✗ {errors} componente(s) con errores")
        return 1

if __name__ == "__main__":
    sys.exit(verificar())
VERIFY_EOF

chmod +x install/verify_installation.py
```

**Checklist Fase 6:**
- [ ] verify_installation.py creado y ejecutable

---

## 🧪 Fase 7: Pruebas y Validación

**Tiempo estimado**: 1 hora

### Paso 7.1: Ejecutar Build

```bash
# Desde raíz del proyecto
./build/build_all.sh
```

**Verificaciones:**
- [ ] Build ejecuta sin errores
- [ ] Directorio `release/` creado
- [ ] `release/wheels/` contiene 9 archivos .whl
- [ ] `release/source/` contiene 9 archivos .tar.gz
- [ ] `release/config/config.json` existe
- [ ] `release/docs/` contiene archivos .md

### Paso 7.2: Listar Artefactos Generados

```bash
# Ver wheels
ls -lh release/wheels/

# Ver source
ls -lh release/source/

# Contar archivos
echo "Wheels: $(ls -1 release/wheels/*.whl | wc -l)"
echo "Source: $(ls -1 release/source/*.tar.gz | wc -l)"
```

**Resultado esperado:**
```
Wheels: 9
Source: 9
```

### Paso 7.3: Verificar Wheels con twine

```bash
# Instalar twine si no está
pip install twine

# Verificar todos los wheels
twine check release/wheels/*.whl
```

**Resultado esperado:**
```
Checking release/wheels/dominio_senial-5.0.0-py3-none-any.whl: PASSED
Checking release/wheels/adquisicion_senial-3.0.0-py3-none-any.whl: PASSED
...
Checking release/wheels/senial_solid-6.0.0-py3-none-any.whl: PASSED
```

### Paso 7.4: Prueba de Instalación en Entorno Limpio

```bash
# Crear entorno de prueba
python3 -m venv test_env
source test_env/bin/activate

# Instalar desde wheels
pip install release/wheels/senial_solid-6.0.0-py3-none-any.whl

# Verificar instalación
python3 install/verify_installation.py

# Probar comando
senial-solid --help 2>/dev/null || python3 -m lanzador.lanzador --help 2>/dev/null || echo "Comando no disponible (normal si no implementado)"

# Limpiar
deactivate
rm -rf test_env
```

**Checklist Paso 7.4:**
- [ ] Entorno de prueba creado
- [ ] Instalación exitosa
- [ ] Verificación pasó sin errores
- [ ] Entorno limpiado

### Paso 7.5: Prueba del Script de Instalación

```bash
# Crear otro entorno limpio
python3 -m venv test_install_env

# NO activar, dejar que install.sh maneje

# Ejecutar script de instalación
./install/install.sh
# Seleccionar "N" para no usar venv adicional

# Verificar
source test_install_env/bin/activate  # Si se creó
python3 install/verify_installation.py

# Limpiar
deactivate 2>/dev/null || true
rm -rf test_install_env senial_env
```

**Checklist Paso 7.5:**
- [ ] Script de instalación ejecutó sin errores
- [ ] Todos los paquetes instalados
- [ ] Verificación pasó

---

## 📖 Fase 8: Documentación Final

**Tiempo estimado**: 30 minutos

### Paso 8.1: Crear `release/README.md`

```bash
cat > release/README.md << 'RELEASE_README_EOF'
# Senial SOLID v6.0.0 - Release Distribution

Distribución completa del sistema de procesamiento de señales con principios SOLID.

## Contenido

```
release/
├── wheels/          # Paquetes wheels (instalación rápida)
├── source/          # Código fuente (tar.gz)
├── config/          # Configuración de ejemplo
├── docs/            # Documentación
├── scripts/         # Scripts de instalación
└── README.md        # Este archivo
```

## Instalación Rápida

### Linux/macOS

```bash
./scripts/install.sh
```

### Windows

```cmd
scripts\install.bat
```

## Instalación Manual

```bash
# Instalar meta-paquete (instala todo)
pip install wheels/senial_solid-6.0.0-py3-none-any.whl

# O instalar paquetes individuales
pip install wheels/*.whl
```

## Uso

```bash
# Comando directo
senial-solid

# O como módulo
python -m lanzador.lanzador
```

## Componentes Incluidos

- dominio-senial v5.0.0
- adquisicion-senial v3.0.0
- procesamiento-senial v3.0.0
- presentacion-senial v2.0.0
- persistidor-senial v7.0.0
- supervisor v1.0.0
- configurador v3.0.0
- lanzador v6.0.0
- senial-solid v6.0.0 (meta-paquete)

## Requisitos

- Python >= 3.8
- pip

## Documentación

Ver `docs/` para documentación completa.

## Licencia

MIT License - Ver LICENSE
RELEASE_README_EOF

# Copiar a release si ya existe
cp release/README.md release/ 2>/dev/null || true
```

### Paso 8.2: Actualizar README Principal del Proyecto

```bash
# Agregar sección de distribución al README.md principal
cat >> README.md << 'README_APPEND_EOF'

---

## 📦 Distribución y Paquetización

Este proyecto incluye scripts completos de build e instalación para distribución multiplataforma.

### Build del Release

```bash
# Linux/macOS
./build/build_all.sh

# Windows
build\build_all.bat
```

### Instalación desde Release

```bash
# Linux/macOS
./install/install.sh

# Windows
install\install.bat
```

### Estructura de Release

El directorio `release/` contiene:
- **wheels/**: Paquetes wheel para instalación rápida
- **source/**: Distribuciones fuente (.tar.gz)
- **config/**: Configuración de ejemplo
- **docs/**: Documentación completa
- **scripts/**: Scripts de instalación

### Documentación de Paquetización

Ver `docs/PLAN_PAQUETIZACION_PASO_A_PASO.md` para el plan completo de implementación.

README_APPEND_EOF
```

### Paso 8.3: Crear CHANGELOG para Release

```bash
cat > CHANGELOG_v6.0.0.md << 'CHANGELOG_EOF'
# CHANGELOG - v6.0.0

## [6.0.0] - 2024-10-04

### Agregado
- ✅ DIP completo con configuración externa JSON
- ✅ CargadorConfig con ruta dinámica (`__file__`)
- ✅ Factories especializados (FactorySenial, FactoryAdquisidor, FactoryProcesador, FactoryContexto)
- ✅ Meta-paquete `senial-solid` para instalación completa
- ✅ Scripts de build multiplataforma (build_all.sh, build_all.bat)
- ✅ Scripts de instalación multiplataforma (install.sh, install.bat)
- ✅ Script de verificación de versiones
- ✅ Script de verificación de instalación
- ✅ Documentación completa de paquetización

### Modificado
- 🔄 Configurador simplificado de 21+ métodos a 8 métodos esenciales
- 🔄 Configuración desde config.json (antes hardcoded)
- 🔄 Lanzador v6.0.0 con inicialización JSON
- 🔄 README principal con sección de distribución

### Documentación
- 📚 APLICACION DIP CONFIGURACION EXTERNA.md
- 📚 FACTORIES ESPECIALIZADOS - DELEGACION Y SRP.md
- 📚 CARGADOR CONFIG - GESTION DE CONFIGURACION EXTERNA.md
- 📚 PLAN_PAQUETIZACION_PASO_A_PASO.md

### Componentes (Versiones)
- dominio-senial v5.0.0
- adquisicion-senial v3.0.0
- procesamiento-senial v3.0.0
- presentacion-senial v2.0.0
- persistidor-senial v7.0.0
- supervisor v1.0.0
- configurador v3.0.0
- lanzador v6.0.0
- senial-solid v6.0.0 (meta-paquete)

### Beneficios
✅ Cambiar comportamiento del sistema: Editar config.json, NO código
✅ Instalación con un solo comando
✅ Distribución multiplataforma
✅ Build automatizado
✅ Todos los principios SOLID aplicados
CHANGELOG_EOF
```

**Checklist Fase 8:**
- [ ] release/README.md creado
- [ ] README.md principal actualizado
- [ ] CHANGELOG_v6.0.0.md creado

---

## 📋 Checklist Final Completo

### Estructura de Archivos Creados

```
✅ build/
   ✅ verify_versions.py
   ✅ build_all.sh
   ✅ build_all.bat

✅ install/
   ✅ install.sh
   ✅ install.bat
   ✅ verify_installation.py

✅ senial_solid_metapackage/
   ✅ setup.py
   ✅ README.md
   ✅ LICENSE
   ✅ MANIFEST.in
   ✅ pyproject.toml
   ✅ senial_solid/
      ✅ __init__.py
   ✅ config/
      ✅ config.json

✅ docs/
   ✅ PLAN_PAQUETIZACION_PASO_A_PASO.md (este archivo)

✅ Documentación actualizada
   ✅ README.md principal
   ✅ CHANGELOG_v6.0.0.md
```

### Tests de Validación

- [ ] `python3 build/verify_versions.py` - Pasa sin errores
- [ ] `./build/build_all.sh` - Ejecuta sin errores
- [ ] `release/` directorio creado con todos los artefactos
- [ ] 9 wheels en `release/wheels/`
- [ ] 9 tar.gz en `release/source/`
- [ ] `twine check release/wheels/*.whl` - Todos PASSED
- [ ] Instalación en entorno limpio funciona
- [ ] `./install/install.sh` ejecuta sin errores
- [ ] `python3 install/verify_installation.py` - Todos los componentes OK

---

## 🚀 Comandos de Ejecución Rápida

### Ejecución Completa del Plan

```bash
# 1. Verificar versiones
python3 build/verify_versions.py

# 2. Build completo
./build/build_all.sh

# 3. Verificar wheels
twine check release/wheels/*.whl

# 4. Crear entorno de prueba e instalar
python3 -m venv test_env
source test_env/bin/activate
pip install release/wheels/senial_solid-6.0.0-py3-none-any.whl

# 5. Verificar instalación
python3 install/verify_installation.py

# 6. Limpiar
deactivate
rm -rf test_env
```

### Solo Build

```bash
./build/build_all.sh
```

### Solo Instalación

```bash
./install/install.sh
```

---

## 📊 Métricas de Éxito

Al completar este plan, deberías tener:

✅ **9 paquetes wheel** en `release/wheels/`
✅ **9 distribuciones source** en `release/source/`
✅ **Meta-paquete** funcional que instala todo
✅ **Scripts de build** para Linux/macOS/Windows
✅ **Scripts de instalación** para Linux/macOS/Windows
✅ **Instalación verificable** con script automático
✅ **Documentación completa** del proceso
✅ **Sistema instalable** con un solo comando

---

## 🎯 Próximos Pasos (Opcional)

1. **Publicar en PyPI**
   - Crear cuenta en PyPI
   - Configurar API token
   - `twine upload release/wheels/*`

2. **Crear GitHub Release**
   - Tag: `v6.0.0`
   - Subir wheels como assets
   - Agregar CHANGELOG

3. **Automatizar con CI/CD**
   - GitHub Actions para build automático
   - Tests automáticos en cada push
   - Release automático en cada tag

---

## 📝 Notas Importantes

- **Ejecutar siempre desde raíz del proyecto**: `/Users/victor/PycharmProjects/Senial_SOLID_IS`
- **No ejecutar scripts desde sus directorios**: Scripts usan rutas relativas desde raíz
- **Verificar Python >= 3.8**: Scripts requieren Python moderno
- **Windows**: Usar PowerShell o CMD como administrador si es necesario
- **Permisos**: Scripts .sh necesitan `chmod +x` en Linux/macOS

---

**📖 Plan Completo de Paquetización - Victor Valotto**
**🎯 Estado**: Listo para ejecutar
**📅 Fecha**: Octubre 2024
**🔄 Versión**: 6.0.0
