# Poetry with optional Cython extension

This is a python packaging example project.

## Installation
Install this package as pure python with `pip install poetry-optional-cython`.
Install with cython extension `pip install poetry-optional-cython[fast]`.

## Running
Try running the installed command:

```bash
$ pocy
### Running as compiled extension ###
Hello Poetry with optional cython extension
Calculating fib(36)
14930352
```

The first line of the command output will indicate if the cython extension module
compilation succeeded during installation.


