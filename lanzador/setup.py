from setuptools import setup, find_packages

setup(
    name="lanzador",
    version="3.0.0",
    description="Orquestador principal para demostración de principios SOLID",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "dominio-senial>=1.0.0",
        "adquisicion-senial>=1.0.0",
        "procesamiento-senial>=1.0.0",
        "presentacion-senial>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "lanzador=lanzador.lanzador:main",
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