# `fproperty` - a simpler property decorator

Define the `fget`/`fset`/`fdel` functions and return them:

    from fproperty import fproperty

    class Thing:

        @fproperty
        def my_attribute():

            def fget(self):
                return self._attr

            def fset(self, value):
                self._attr = value

            def fdel(self):
                del self._attr

            return (fget, fset, fdel, "doc")

instead of `property` chaining:

    class Thing:

        @property
        def my_attribute(self):
            return self._attr

        @my_attribute.setter
        def my_attribute(self, value):
            self._attr = value

        @my_attribute.deleter
        def my_attribute(self):
            del self._attr

which requires typing `my_attribute` five times,
or by using the non-decorator case:

    class Thing:

        def fget(self):
            return self._attr

        def fset(self, value):
            self._attr = value

        def fdel(self):
            del self._attr

        my_attribute = property(fget, fset, fdel, "doc")
        del fget, fset, fdel

which spreads out the definitions, and requires
namespace cleanup.


## Other examples

The `fproperty` decorator can be returned a partial list:

    @fproperty
    def set_only_attribute():
        def fset(self, value):
            self._value = value
        return (None, fset)


## Install

    pip install fproperty


## License

Licensed under the Apache License, Version 2.0 (the "License")
