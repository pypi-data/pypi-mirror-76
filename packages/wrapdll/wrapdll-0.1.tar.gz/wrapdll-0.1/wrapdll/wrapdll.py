"""
Help wrap dll using python annotations as type hints
"""
from ctypes import cdll
from functools import wraps
from enum import IntEnum


def wrapdll(method):
    """
    Used to wrap methods of BaseDllWrapper's subcasses.
    Will replace the method with a dll exported function with the same name
    while using the annotations as typing hints 
    """
    @wraps(method)
    def _wrapdll_impl(self, *method_args, **method_kwargs):
        dll_func = getattr(self._dll, method.__name__)
        types = dict(method.__annotations__)
        # Add restype from annotations
        if 'return' in types:
            dll_func.restype = types['return']
            del types['return']
        # Add argtypes from annotations
        dll_func.argtypes = list(types.values())
        # Add defaults valeus if exists
        dll_func.__defaults__ = method.__defaults__
        dll_func.__kwdefaults__ = method.__kwdefaults__
        # Add errcheck func from the errcheck decorator
        errcheck = method_kwargs.pop('_errcheck_', None)
        if errcheck is not None:
            dll_func.errcheck = errcheck
        return dll_func(*method_args, **method_kwargs)
    return _wrapdll_impl

class BaseDllWrapper():
    """
    Derive from this class in conjucture with wrapdll decorator to wrap dlls
    """

    def __init__(self, ctypes_dll):
        """
        :param ctypes_dll: A ctypes dll (cdll or windll) or a str.
                           If got a str then tries to convert it to a cdll
        """
        if isinstance(ctypes_dll, str):
            ctypes_dll = cdll(ctypes_dll)
        self._dll = ctypes_dll

class RCEnum(IntEnum):
    """
    Derive from this cass to create return code enums with a msg.
    Ex:
    class CustomRC(RCEnum):
        SUCCESS = 0x00, 'No problem'
        CONNECTION_ERROR = 0x01, 'Failed to connect!'
        NO_MSG = 0x03
    """
    def __new__(cls, value, msg=None):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.msg = msg
        return obj

    def __repr__(self):
        return "<{}.{}: 0x{:X}>".format(self.__class__.__name__, self._name_, self._value_)

    def __str__(self):
        if self.msg:
            return "{}.{}: {}".format(self.__class__.__name__, self._name_, self.msg)
        return "{}.{}".format(self.__class__.__name__, self._name_)

def errcheck(err_func):
    """
    Adds an errcheck callable to a wrapdll method.
    err_func signature should be err_func(result, func, arguments) (Read ctypes doc for more)
    Notice the wrapdll decorator must be bellow this decorator.
    EX:
        def validate(result, func, arguments):
            if result:
                raise DllError(result)
        @errcheck(validate)
        @wrapdll
        def func():
            pass
    """
    def decorator(method):
        @wraps(method)
        def _errcheck_impl(self, *method_args, **method_kwargs):
            method_kwargs['_errcheck_'] = err_func
            return method(self, *method_args, **method_kwargs)
        return _errcheck_impl
    return decorator

class DllError(Exception):
    pass

def allowed_values(*values, exception=DllError):
    """
    Like errcheck decorator, but instead of a callable gets allowed values.
    Useful with RCEnum to check for invalid return codes
    """
    return _assert_values(*values, exception=exception, is_allowed=False)

def forbidden_values(*values, exception=DllError):
    """
    Like errcheck decorator, but instead of a callable gets forbidden values.
    Useful with RCEnum to check for invalid return codes
    """
    return _assert_values(*values, exception=exception, is_allowed=True)

def _assert_values(*values, exception=DllError, is_allowed=True):
    def _assert(result, func, arguments):
        # restype automatically dereference pointers, so add dereferenced pointers from values 
        dereferences = [value.value for value in values if hasattr(value, 'value')]
        dereferences.extend(values)
        if is_allowed:
            # Treat as allowed_values
            check = result in dereferences
        else:
            # Treat as forbidden_values
            check = result not in dereferences
        if check:
            raise exception(result)
        return result
    return errcheck(_assert)


