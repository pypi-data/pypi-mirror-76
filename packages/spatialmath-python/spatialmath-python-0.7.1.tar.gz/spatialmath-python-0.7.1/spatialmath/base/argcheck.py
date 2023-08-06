#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:41:25 2020

@author: corkep
"""
import numpy as np
import math

try:
    import sympy
    _sympy = True
except ImportError:
    _sympy = False

def isscalar(x):
    return isinstance(x, (int, np.int64, float, np.float64))

def matrix(m, shape):
    assert ismatrix(m, shape)


def ismatrix(m, shape):
    if not isinstance(m, np.ndarray):
        return False
    if len(shape) != len(m.shape):
        return False
    if shape[0] is not None and shape[0] > 0 and shape[0] != m.shape[0]:
        return False
    if shape[1] is not None and shape[1] > 0 and shape[1] != m.shape[1]:
        return False
    return True


def verifymatrix(m, shape):
    if not isinstance(m, np.ndarray):
        raise TypeError("input must be a numpy ndarray")

    if not m.shape == shape:
        raise ValueError("incorrect matrix dimensions, "
                         "expecting {0}".format(shape))

 # and not np.iscomplex(m) checks every element, would need to be not np.any(np.iscomplex(m)) which seems expensive


def getvector(v, dim=None, out='array'):
    if isinstance(v, (int, np.int64, float)) or (
            _sympy and isinstance(v, sympy.Expr)):  # handle scalar case
        v = [v]

    if isinstance(v, (list, tuple)):
        if dim is not None and v and len(v) != dim:
            raise ValueError("incorrect vector length")
        if out == 'sequence':
            return v
        elif out == 'array':
            return np.array(v, dtype=np.float64)
        elif out == 'row':
            return np.array(v, dtype=np.float64).reshape(1, -1)
        elif out == 'col':
            return np.array(v, dtype=np.float64).reshape(-1, 1)
        else:
            raise ValueError("invalid output specifier")
    elif isinstance(v, np.ndarray):
        s = v.shape
        if dim is not None:
            if not (s == (dim,) or s == (1, dim) or s == (dim, 1)):
                raise ValueError("incorrect vector length: expected {}, got {}".format(dim, s))

        v = v.flatten()

        if out == 'sequence':
            return list(v.flatten())
        elif out == 'array':
            return v.astype(np.float64)
        elif out == 'row':
            return v.astype(np.float64).reshape(1, -1)
        elif out == 'col':
            return v.astype(np.float64).reshape(-1, 1)
        else:
            raise ValueError("invalid output specifier")
    else:
        raise TypeError("invalid input type")


def vector(v, dim):
    assert isvector(v, dim)


def isvector(v, dim=None, out='sequence'):
    if isinstance(v, (list, tuple)) and (dim is None or len(v) == dim) and all(map(lambda x: isinstance(x, (int, float)), v)):
        return True  # list or tuple

    if isinstance(v, np.ndarray):
        s = v.shape
        if dim is None:
            return (len(s) == 1 and s[0] > 0) or (s[0] == 1 and s[1] > 0) or (s[0] > 0 and s[1] == 1)
        else:
            return s == (dim,) or s == (1, dim) or s == (dim, 1)

    if (dim is None or dim == 1) and isinstance(v, (int, float)):
        return True

    return False


def isscalar(v):
    return isinstance(v, (int, float))


def getunit(v, u):
    if u == "rad":
        return v
    elif u == "deg":
        if isinstance(v, np.ndarray) or np.isscalar(v):
            return v * math.pi / 180
        else:
            return [x * math.pi / 180 for x in v]
    else:
        raise ValueError("invalid angular units")


def isnumberlist(l):
    return isinstance(l, (list, tuple)) and len(l) > 0 and all(map(lambda x: isinstance(x, (float, int)), l))


def isvectorlist(l, n):
    return isinstance(l, (list, tuple)) and len(l) > 0 and all(map(lambda x: isinstance(x, np.ndarray) and len(x) == n, l))


if __name__ == '__main__':
    import pathlib
    import os.path

    exec(open(os.path.join(pathlib.Path(__file__).parent.absolute(), "test_argcheck.py")).read())
