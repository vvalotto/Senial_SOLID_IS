#!/bin/bash
# install_from_github.sh - Instalación desde GitHub Release

set -e

# Configuración
GITHUB_REPO="vvalotto/Senial_SOLID_IS"
VERSION="6.0.0"
RELEASE_TAG="v${VERSION}"
TEMP_DIR="/tmp/senial_solid_install_$$"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() { echo -e "${BLUE}==>${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup EXIT

check_dependencies() {
    print_step "Verificando dependencias..."

    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no encontrado"
        exit 1
    fi

    if ! command -v curl &> /dev/null; then
        print_error "curl no encontrado. Instale curl primero."
        exit 1
    fi

    print_success "Dependencias OK"
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

download_wheels() {
    print_step "Descargando wheels desde GitHub Release ${RELEASE_TAG}..."

    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"

    # Lista de paquetes en orden de dependencias
    local packages=(
        "supervisor-1.0.0-py3-none-any.whl"
        "dominio_senial-5.0.0-py3-none-any.whl"
        "adquisicion_senial-3.0.0-py3-none-any.whl"
        "procesamiento_senial-3.0.0-py3-none-any.whl"
        "presentacion_senial-2.0.0-py3-none-any.whl"
        "persistidor_senial-7.0.0-py3-none-any.whl"
        "configurador-3.0.0-py3-none-any.whl"
        "lanzador-6.0.0-py3-none-any.whl"
        "senial_solid-6.0.0-py3-none-any.whl"
    )

    for wheel in "${packages[@]}"; do
        local url="https://github.com/${GITHUB_REPO}/releases/download/${RELEASE_TAG}/${wheel}"
        echo "  Descargando ${wheel}..."

        if ! curl -L -f -o "${wheel}" "${url}" --progress-bar; then
            print_error "Error descargando ${wheel}"
            print_warning "URL: ${url}"
            print_warning "Verifique que el release ${RELEASE_TAG} existe y contiene los wheels"
            exit 1
        fi
    done

    print_success "Todos los wheels descargados"
}

install_packages() {
    print_step "Instalando paquetes..."

    python3 -m pip install --upgrade pip --quiet

    # Instalar en orden de dependencias
    pip install "$TEMP_DIR/supervisor-1.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/dominio_senial-5.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/adquisicion_senial-3.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/procesamiento_senial-3.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/presentacion_senial-2.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/persistidor_senial-7.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/configurador-3.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/lanzador-6.0.0-py3-none-any.whl" --quiet
    pip install "$TEMP_DIR/senial_solid-6.0.0-py3-none-any.whl" --quiet

    print_success "Todos los paquetes instalados"
}

setup_config() {
    print_step "Configurando directorio de trabajo..."

    mkdir -p ~/.senial_solid

    # Descargar config.json de ejemplo
    local config_url="https://raw.githubusercontent.com/${GITHUB_REPO}/main/configurador/config.json"
    if curl -L -f -o ~/.senial_solid/config.json "${config_url}" --silent; then
        print_success "Configuración descargada: ~/.senial_solid/config.json"
    else
        print_warning "No se pudo descargar config.json (se puede configurar manualmente después)"
    fi

    mkdir -p ~/.senial_solid/tmp/datos/adquisicion
    mkdir -p ~/.senial_solid/tmp/datos/procesamiento
    print_success "Directorio de trabajo configurado"
}

verify_installation() {
    print_step "Verificando instalación..."

    if python3 -c "from dominio_senial import SenialBase" 2>/dev/null; then
        print_success "dominio_senial OK"
    fi
    if python3 -c "from configurador import Configurador" 2>/dev/null; then
        print_success "configurador OK"
    fi
    if python3 -c "from lanzador import Lanzador" 2>/dev/null; then
        print_success "lanzador OK"
    fi

    return 0
}

show_summary() {
    echo ""
    echo "================================================"
    print_success "Instalación completada desde GitHub Release"
    echo "================================================"
    echo ""
    echo "🚀 Ejecutar: senial-solid"
    echo "   o: python -m lanzador.lanzador"
    echo ""
    echo "📁 Config: ~/.senial_solid/config.json"
    echo "📦 Release: ${RELEASE_TAG}"
    echo ""
}

main() {
    echo "================================================"
    echo "  Instalación de Senial SOLID ${VERSION}"
    echo "  Desde GitHub Release: ${RELEASE_TAG}"
    echo "================================================"
    echo ""

    check_dependencies

    if ask_venv; then
        create_venv
    fi

    download_wheels
    install_packages
    setup_config
    verify_installation
    show_summary
}

main
