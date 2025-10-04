#!/bin/bash
# build_all.sh - Build de todos los paquetes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGING_DIR="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$(dirname "$PACKAGING_DIR")"
RELEASE_DIR="$PACKAGING_DIR/release"

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
               configurador lanzador; do
        if [ -d "$ROOT_DIR/$dir" ]; then
            rm -rf "$ROOT_DIR/$dir/dist"
            rm -rf "$ROOT_DIR/$dir/build"
            rm -rf "$ROOT_DIR/$dir"/*.egg-info
        fi
    done

    # Limpiar metapackage
    if [ -d "$PACKAGING_DIR/metapackage" ]; then
        rm -rf "$PACKAGING_DIR/metapackage/dist"
        rm -rf "$PACKAGING_DIR/metapackage/build"
        rm -rf "$PACKAGING_DIR/metapackage"/*.egg-info
    fi

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

    # Build metapackage
    print_step "Building senial-solid..."
    cd "$PACKAGING_DIR/metapackage"
    python3 -m build || exit 1
    cp dist/*.whl "$RELEASE_DIR/wheels/" 2>/dev/null || true
    cp dist/*.tar.gz "$RELEASE_DIR/source/" 2>/dev/null || true
    print_success "senial-solid built"
    cd "$ROOT_DIR"

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
