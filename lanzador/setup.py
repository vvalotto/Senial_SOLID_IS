from setuptools import setup, find_packages

setup(
    name="lanzador",
    version="6.0.0",
    description="Orquestador con DIP Completo - SOLID aplicado con configuración externa JSON",
    long_description="Orquestador que demuestra TODOS los principios SOLID con configuración "
                     "externa JSON. DIP completo: tipos determinados por config.json, no por código. "
                     "Repository Pattern + Factory Pattern + Auditoría automática interna.",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "dominio-senial>=5.0.0",
        "adquisicion-senial>=3.0.0",
        "procesamiento-senial>=3.0.0",
        "presentacion-senial>=2.0.0",
        "configurador>=3.0.0",  # Configuración JSON + Factories
        "persistidor-senial>=7.0.0",  # FactoryContexto + ISP
        "supervisor>=1.0.0",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="solid principles, dip, dependency inversion, json config, repository pattern, factory pattern, orchestrator, signal processing, education",
)