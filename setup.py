#!/usr/bin/env python
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


libraries = []  # add any libraries, such as sqlite3, here

ext_modules = [
    Extension(
        'unidecode', [
            'src/module.cpp',
        ],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True),
            'include',
        ],
        libraries=libraries,
        language='c++'
    ),
]


class BuildExt(build_ext):
    def build_extensions(self):
        compiler_type = self.compiler.compiler_type

        opts = ['-O2', '-march=native']
        if sys.platform == 'darwin':
            opts += ['-stdlib=libc++', '-mmacosx-version-min=10.8']

        if compiler_type == 'unix':
            opts.extend([
                '-DVERSION_INFO="{}"'.format(self.distribution.get_version()),
                '-std=c++1z',
            ])

        for ext in self.extensions:
            ext.extra_compile_args = opts

        build_ext.build_extensions(self)


setup(
    name='unidecode-fast',
    description='Fast Unidecode',
    version='0.1.0',
    setup_requires=['pybind11>=2.2.4'],
    install_requires=['pybind11>=2.2.4'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    test_suite='tests',
    zip_safe=False,
)
