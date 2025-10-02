from setuptools import setup, find_packages
import pathlib

# Leer el README para la descripción larga
HERE = pathlib.Path(__file__).parent
README_PATH = HERE / "README.md"
if README_PATH.exists():
    README = README_PATH.read_text(encoding="utf-8")
else:
    README = "Paquete de adquisición de datos para procesamiento de señales digitales"

setup(
    name="adquisicion-senial",
    version="2.1.0",
    description="Adquisición de datos con soporte polimórfico para SenialBase",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "dominio-senial>=4.0.0",
    ],
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
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="solid principles, data acquisition, signal processing, education",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/Senial_SOLID_IS/issues",
        "Source": "https://github.com/vvalotto/Senial_SOLID_IS",
        "Documentation": "https://github.com/vvalotto/Senial_SOLID_IS/blob/main/README.md",
    },
)