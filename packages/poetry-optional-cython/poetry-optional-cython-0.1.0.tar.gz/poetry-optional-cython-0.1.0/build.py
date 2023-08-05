# -*- coding: utf-8 -*-
from distutils.command.build_ext import build_ext


class BuildExt(build_ext):
    def build_extensions(self):
        try:
            super().build_extensions()
        except Exception:
            print("Cython build failed. Using pure Python mode.")


def build(setup_kwargs):
    try:
        from Cython.Build import cythonize
    except ImportError:
        print("Cython not installed. Using pure Python mode.")
    else:
        setup_kwargs.update(
            dict(
                cmdclass=dict(build_ext=BuildExt),
                ext_modules=cythonize(["poetry_optional_cython/fib.py"]),
            )
        )
