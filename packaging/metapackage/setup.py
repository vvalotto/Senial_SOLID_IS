from setuptools import setup, find_packages
import os

def read_long_description():
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, encoding='utf-8') as f:
            return f.read()
    return "Sistema completo de procesamiento de señales con principios SOLID"

setup(
    name="senial-solid",
    version="6.0.0",
    description="Sistema completo de procesamiento de señales con principios SOLID aplicados",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/Senial_SOLID_IS/issues",
        "Documentation": "https://github.com/vvalotto/Senial_SOLID_IS/tree/main/docs",
        "Source Code": "https://github.com/vvalotto/Senial_SOLID_IS",
    },
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "lanzador>=6.0.0",
    ],
    entry_points={
        'console_scripts': [
            'senial-solid=lanzador.lanzador:ejecutar',
        ],
    },
    include_package_data=True,
    package_data={
        'senial_solid': ['config/*.json'],
    },
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ],
    keywords="solid principles signal-processing architecture design-patterns",
    zip_safe=False,
)
