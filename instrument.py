import re
import os
import types
import inspect
from functools import wraps
import logging


logger = logging.getLogger('instrumentation')
handler = logging.FileHandler('/tmp/foo.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def instrument_function(obj):

    @wraps(obj)
    def wrapper(*args, **kwargs):
        result = obj(*args, **kwargs)
        logger.debug('called {function} from module {module} with args {args}, {kwargs} returned {result}'.format(
            function=obj.__qualname__,
            module=obj.__module__,
            args=args,
            kwargs=kwargs,
            result=result
        ))
        return result
    return wrapper

def instrument_class(decorator):
    
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            #import ipdb; ipdb.set_trace()
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def instrument_this_module():
    """When called at the bottom of a module, monkeypatch module to instrument functions, classes
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    # monkeypatch the module...
    for name, obj in module.__dict__.items():
        if isinstance(obj, types.FunctionType):
            module.__dict__[name] = instrument_function(obj)
        elif isinstance(obj, type):
            instrument_class(instrument_function)(obj)
