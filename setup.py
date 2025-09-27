from setuptools import setup, find_packages
import pathlib

# Leer el README para la descripción larga
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="Senial_SOLID_IS",
    version="0.1.0",
    description="Caso de estudio didáctico de los principios SOLID en Python",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Proyecto Académico",
    author_email="proyecto.academico@ejemplo.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "solid-demo=lanzador:ejecutar",
        ],
    },
    py_modules=["lanzador"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
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
    ],
    keywords="solid principles, software engineering, design patterns, education",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/Senial_SOLID_IS/issues",
        "Source": "https://github.com/vvalotto/Senial_SOLID_IS",
        "Documentation": "",
    },
)