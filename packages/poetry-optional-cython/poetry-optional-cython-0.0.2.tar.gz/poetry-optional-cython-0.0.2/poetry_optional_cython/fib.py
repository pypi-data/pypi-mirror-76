# -*- coding: utf-8 -*-
"""The canonical fibanocci example in pure python"""
try:
    import cython
    if cython.compiled:
        print("### Running as compiled extension ###")
    else:
        print("### Cython installed but extension not compiled ###")
except ImportError:
    print("### Running as pure python module ###")


def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

