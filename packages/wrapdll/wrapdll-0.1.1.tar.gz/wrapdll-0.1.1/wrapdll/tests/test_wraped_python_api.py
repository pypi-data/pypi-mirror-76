from ctypes import *
from unittest import TestCase
from sys import getrefcount as grc
from .wraped_python_api import PythonAPI

class WrapedPythonAPITestCase(TestCase):
    """
    Copied from ctypes test_python_api.py
    """
    dll = None

    @classmethod
    def setUpClass(cls):
        cls.dll = PythonAPI()

    def test_PyBytes_FromStringAndSize(self):
        PyBytes_FromStringAndSize = self.dll.PyBytes_FromStringAndSize

        # PyBytes_FromStringAndSize.restype = py_object
        # PyBytes_FromStringAndSize.argtypes = c_char_p, c_py_ssize_t

        self.assertEqual(PyBytes_FromStringAndSize(b"abcdefghi", 3), b"abc")

    def test_PyString_FromString(self):
        # pythonapi.PyBytes_FromString.restype = py_object
        # pythonapi.PyBytes_FromString.argtypes = (c_char_p,)

        s = b"abc"
        refcnt = grc(s)
        pyob = self.dll.PyBytes_FromString(s)
        self.assertEqual(grc(s), refcnt)
        self.assertEqual(s, pyob)
        del pyob
        self.assertEqual(grc(s), refcnt)

    def test_PyLong_Long(self):
        ref42 = grc(42)
        # pythonapi.PyLong_FromLong.restype = py_object
        self.assertEqual(self.dll.PyLong_FromLong(42), 42)

        self.assertEqual(grc(42), ref42)

        # pythonapi.PyLong_AsLong.argtypes = (py_object,)
        # pythonapi.PyLong_AsLong.restype = c_long

        res = self.dll.PyLong_AsLong(42)
        self.assertEqual(grc(res), ref42 + 1)
        del res
        self.assertEqual(grc(42), ref42)

    def test_PyOS_snprintf(self):
        PyOS_snprintf = self.dll.PyOS_snprintf
        # PyOS_snprintf.argtypes = POINTER(c_char), c_size_t, c_char_p

        buf = c_buffer(256)
        PyOS_snprintf(buf, sizeof(buf), b"Hello from %s", b"ctypes")
        self.assertEqual(buf.value, b"Hello from ctypes")

        PyOS_snprintf(buf, sizeof(buf), b"Hello from %s (%d, %d, %d)", b"ctypes", 1, 2, 3)
        self.assertEqual(buf.value, b"Hello from ctypes (1, 2, 3)")

        # not enough arguments
        self.assertRaises(TypeError, PyOS_snprintf, buf)
