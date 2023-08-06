from ctypes import *
from wrapdll import BaseDllWrapper, wrapdll 

class PythonAPI(BaseDllWrapper):
    """
    A wrapper to ctypes.pythonapi
    """

    def __init__(self):
        super().__init__(pythonapi)

    @wrapdll
    def PyBytes_FromStringAndSize(self, v: c_char_p, len: c_size_t) -> py_object:
        """
        Return a new bytes object with a copy of the string v as value and length len on success, and NULL on failure.
        If v is NULL, the contents of the bytes object are uninitialized.
        """
        pass

    @wrapdll
    def PyBytes_FromString(self, v: c_char_p) -> py_object:
        """
        Return a new bytes object with a copy of the string v as value on success, and NULL on failure.
        The parameter v must not be NULL; it will not be checked.
        """
        pass

    @wrapdll
    def PyLong_FromLong(self, v: c_long) -> py_object:
        """
        Return a new PyLongObject object from v, or NULL on failure.
        """
        pass

    @wrapdll
    def PyLong_AsLong(self, obj: py_object) -> c_long:
        """
        Return a C long representation of obj.
        If obj is not an instance of PyLongObject, first call its __index__ or
        __int__ method (if present) to convert it to a PyLongObject.
        """
        pass

    @wrapdll
    def PyOS_snprintf(self, str: POINTER(c_char), size: c_size_t, format: c_char_p):
        """
        Output not more than size bytes to str according to the format string 
        format and the extra arguments. See the Unix man page snprintf(2).
        """
        pass
