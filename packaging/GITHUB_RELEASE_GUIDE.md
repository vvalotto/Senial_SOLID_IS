# Guía para crear GitHub Release v6.0.0

Esta guía explica cómo crear el release en GitHub con el bundle de instalación.

## Paso 1: Build del Bundle

```bash
# 1. Ejecutar build completo
./packaging/build/build_all.sh

# 2. Crear bundle de distribución
./packaging/build/create_bundle.sh

# 3. Verificar que se generó el bundle
ls -lh packaging/release/senial_solid-v6.0.0.tar.gz
```

**Resultado esperado**:
- ✅ 9 wheels en `packaging/release/wheels/`
- ✅ 9 source distributions en `packaging/release/source/`
- ✅ Bundle comprimido: `senial_solid-v6.0.0.tar.gz` (~64KB)

## Paso 2: Verificar el Bundle

```bash
# Listar contenido del bundle
tar -tzf packaging/release/senial_solid-v6.0.0.tar.gz

# Debe contener:
# - senial_solid-v6.0.0/wheels/*.whl (9 archivos)
# - senial_solid-v6.0.0/config.json
# - senial_solid-v6.0.0/install.sh
# - senial_solid-v6.0.0/README.txt
```

## Paso 3: Crear el Release en GitHub

### Opción A: Interfaz Web

1. Ir a: https://github.com/vvalotto/Senial_SOLID_IS/releases/new

2. **Tag version**: `v6.0.0`
   - Crear nuevo tag desde `main` branch

3. **Release title**: `v6.0.0 - DIP Completo con Bundle de Instalación Simplificada`

4. **Description**: (copiar el texto de `RELEASE_NOTES.md`)

5. **Attach binaries**: Subir el bundle:
   - `packaging/release/senial_solid-v6.0.0.tar.gz`

6. Marcar como **Latest release**

7. Click en **Publish release**

### Opción B: GitHub CLI

```bash
# Instalar gh CLI si no lo tienes: https://cli.github.com/

# Autenticarse
gh auth login

# Crear release y subir bundle
gh release create v6.0.0 \
  --title "v6.0.0 - DIP Completo con Bundle de Instalación Simplificada" \
  --notes-file packaging/RELEASE_NOTES.md \
  packaging/release/senial_solid-v6.0.0.tar.gz
```

---

## Paso 4: Verificar el Release

Después de publicar, verificar:

1. **URL del release**: https://github.com/vvalotto/Senial_SOLID_IS/releases/tag/v6.0.0

2. **Probar descarga del bundle**:
```bash
curl -L -O https://github.com/vvalotto/Senial_SOLID_IS/releases/download/v6.0.0/senial_solid-v6.0.0.tar.gz
```

3. **Probar instalación completa**:
```bash
# Descargar bundle
curl -L -O https://github.com/vvalotto/Senial_SOLID_IS/releases/download/v6.0.0/senial_solid-v6.0.0.tar.gz

# Descomprimir
tar -xzf senial_solid-v6.0.0.tar.gz
cd senial_solid-v6.0.0

# Instalar
./install.sh

# Verificar
source senial_env/bin/activate
senial-solid
```

---

## Paso 5: Actualizar README principal

Agregar badge y sección de instalación en el README.md del proyecto:

```markdown
[![Release](https://img.shields.io/github/v/release/vvalotto/Senial_SOLID_IS)](https://github.com/vvalotto/Senial_SOLID_IS/releases/latest)

## 🚀 Instalación Rápida

### Desde GitHub Release

\```bash
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
\```
```

---

## Troubleshooting

### Error: "Could not find release v6.0.0"
- Verificar que el release esté publicado
- Verificar que el tag sea exactamente `v6.0.0`

### Error descargando bundle
- Verificar que el bundle esté adjunto al release
- Verificar que el repositorio sea público o tengas acceso
- URL correcta: `https://github.com/vvalotto/Senial_SOLID_IS/releases/download/v6.0.0/senial_solid-v6.0.0.tar.gz`

### Error al ejecutar install.sh
```bash
# Dar permisos de ejecución
chmod +x install.sh
./install.sh
```

### Error de permisos con curl
```bash
# Descargar manualmente desde:
# https://github.com/vvalotto/Senial_SOLID_IS/releases/tag/v6.0.0
# Luego descomprimir y ejecutar install.sh
```

---

## Distribución Alternativa

Si prefieres distribuir los wheels por separado (sin bundle):

```bash
# Subir todos los wheels individuales
gh release create v6.0.0 \
  --title "v6.0.0 - DIP Completo" \
  --notes-file packaging/RELEASE_NOTES.md \
  packaging/release/wheels/*.whl

# Instrucciones de instalación manual:
# pip install supervisor-1.0.0-py3-none-any.whl
# pip install dominio_senial-5.0.0-py3-none-any.whl
# ... (resto de paquetes)
```

**Recomendación**: Usar el bundle es más simple para el usuario final.

---

## Checklist de Release

- [ ] Build completado (`./packaging/build/build_all.sh`)
- [ ] Bundle creado (`./packaging/build/create_bundle.sh`)
- [ ] Bundle verificado (`tar -tzf senial_solid-v6.0.0.tar.gz`)
- [ ] Release creado en GitHub con tag `v6.0.0`
- [ ] Bundle subido al release
- [ ] Descarga del bundle verificada
- [ ] Instalación desde bundle probada
- [ ] README principal actualizado con instrucciones
- [ ] Badge de release agregado

---

**Fecha de Release**: 2025-10-04
**Tag**: v6.0.0
**Archivo**: senial_solid-v6.0.0.tar.gz (~64KB)
