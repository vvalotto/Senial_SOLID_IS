#!/bin/bash
# install.sh - Instalación de Senial SOLID

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGING_DIR="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$(dirname "$PACKAGING_DIR")"
RELEASE_DIR="$PACKAGING_DIR/release"

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
        print_warning "Ejecute primero: ./packaging/build/build_all.sh"
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
