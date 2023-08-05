*******************
apispec-py35-compat
*******************

A simple package that provides a deprecated `apispec.compat` package for Python 3.5.
This package was removed from `apispec` during migration from Python 3.5.
It was required however `apispec-webframeworks` 0.4.0 - the last version supporting Python 3.5.

Be careful while uninstalling this package - it will drop `apispec` package as well.

File `apispec/compat.py` is copied from marshmallow-code package file `src/marshmallow/compat.py`
