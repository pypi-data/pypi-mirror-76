

__all__ = ['fproperty']


def fproperty(func):
    """Decorator for a function that returns (fget, fset, fdel, doc)"""
    result = func()
    if not isinstance(result, (tuple, list)):
        raise ValueError('Expected tuple from builder')

    fget = fset = fdel = doc = None
    x = len(result)
    if x == 0:
        pass
    elif x == 1:
        fget, = result
    elif x == 2:
        fget, fset = result
    elif x == 3:
        fget, fset, fdel = result
    elif x == 4:
        fget, fset, fdel, doc = result
    else:
        raise ValueError('too many return values: %i' % x)

    return property(fget, fset, fdel, doc)
