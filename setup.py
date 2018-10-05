"""Setup script for cursed-life."""

from setuptools import setup

import life

setup(
    name="cursed-life",
    version=life.__version__,
    description="Conway's Game of Life",
    url="https://github.com/artemmavrin/cursed-life",
    author="Artem Mavrin",
    author_email="amavrin@ucsd.edu",
    packages=["life"],
    install_requires=[
        "numpy",
        "scipy"
    ],
    zip_safe=False
)
