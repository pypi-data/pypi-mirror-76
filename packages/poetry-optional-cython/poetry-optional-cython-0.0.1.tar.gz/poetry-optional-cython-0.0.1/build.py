# -*- coding: utf-8 -*-
# from setuptools import Extension
from distutils.command.build_ext import build_ext

# extensions = [
#     Extension("poetry_optional_cython.fib", ['poetry_optional_cython/fib.py']),
# ]

class BuildExt(build_ext):
    def build_extensions(self):
        try:
            super().build_extensions()
        except Exception:
            pass


def build(setup_kwargs):
    try:
        from Cython.Build import cythonize
    except ImportError:
        pass
    else:
        setup_kwargs.update(
            dict(
                cmdclass=dict(build_ext=BuildExt),
                ext_modules=cythonize(['poetry_optional_cython/fib.py'], exclude_failures=True),
            )
        )
