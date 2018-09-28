import re
import os
import types
import inspect
from functools import wraps
import logging


def instrument_function(obj):

    @wraps(obj)
    def wrapper(*args, **kwargs):
        result = obj(*args, **kwargs)
        logging.error('called {function} with args {args}, {kwargs} returned {result}'.format(
            function=obj.__name__,
            args=args,
            kwargs=kwargs,
            result=result
        ))
        return result
    return wrapper

def instrument_class(decorator):
    
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def instrument_this_module():
    """When called at the bottom of a module, monkeypatch module to instrument functions, classes
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    # this is silly, but it allows us to include __main__ (when module is executed)
    module_name = re.sub('\.py[co]?$', '', os.path.basename(module.__file__))
    # monkeypatch the module...
    for name, obj in module.__dict__.items():
        if isinstance(obj, types.FunctionType):
            module.__dict__[name] = instrument_function(obj)
        elif isinstance(obj, type):
            instrument_class(instrument_function)(obj)


# @instrument
# def myfun(arg1, arg2, kwarg1=None):
#     return id(arg1) + id(arg2) + id(kwarg1)
# myfun(1, 2, kwarg1=3)


