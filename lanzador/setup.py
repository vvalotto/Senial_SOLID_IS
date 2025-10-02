from setuptools import setup, find_packages

setup(
    name="lanzador",
    version="5.0.0",
    description="Orquestador puro con SRP - Demostración completa de principios SOLID (SRP + OCP + LSP + DIP)",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "dominio-senial>=4.0.0",
        "adquisicion-senial>=2.1.0",
        "procesamiento-senial>=2.1.0",
        "presentacion-senial>=2.0.0",
        "configurador>=2.1.1",
    ],
    entry_points={
        "console_scripts": [
            "lanzador=lanzador.lanzador:ejecutar",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
    ],
    keywords="solid principles, orchestrator, signal processing, education",
)