import builtins

__all__ = ['fproperty', 'property']


_property = builtins.property


def fproperty(func):
    """Decorator for a function that returns (fget, fset, fdel, doc)"""
    result = func()
    if not isinstance(result, (tuple, list)):
        raise ValueError('Expected tuple, not %s' % type(result))

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

    return _property(fget, fset, fdel, doc)


fproperty.apply = fproperty


class property(_property):
    def apply(func):
        return fproperty(func)
