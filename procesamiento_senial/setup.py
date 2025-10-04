from setuptools import setup, find_packages

setup(
    name="procesamiento-senial",
    version="3.0.0",
    description="Factory Pattern + Configuración Externa para procesamiento de señales con DIP",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    package_dir={'procesamiento_senial': '.'},
    packages=['procesamiento_senial'],
    python_requires=">=3.8",
    install_requires=[
        "dominio-senial>=4.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="solid principles, signal processing, education",
)