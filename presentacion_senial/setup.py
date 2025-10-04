from setuptools import setup, find_packages

setup(
    name="presentacion-senial",
    version="2.0.0",
    description="Visualización polimórfica de señales con soporte para SenialBase",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    package_dir={'presentacion_senial': '.'},
    packages=['presentacion_senial'],
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
    keywords="solid principles, data visualization, education",
)