#!/usr/bin/env python
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext


__version__ = '0.2.0'
libraries = []  # add any libraries, such as sqlite3, here

ext_modules = [
    Pybind11Extension(
        'unidecode', [
            'src/module.cpp',
        ],
        include_dirs=[
            'include',
        ],
        libraries=libraries,
        define_macros=[('VERSION_INFO', __version__)],
    ),
]


setup(
    name='unidecode-fast',
    description='Fast Unidecode',
    version=__version__,
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    test_suite='tests',
    zip_safe=False,
)
