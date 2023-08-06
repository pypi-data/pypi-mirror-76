from ctypes import *
from unittest import TestCase
from .wraped_kernel32 import Kernel32, FailedKernel32, MAX_COMPUTERNAME_LENGTH
from wrapdll import DllError
from socket import gethostname

class WrapedKernel32TestCase(TestCase):

    def setUp(self):
        self.__dll = Kernel32()

    def tearDown(self):
        del self.__dll

    def test_GetCurrentProcess(self):
        self.assertEqual(self.__dll.GetCurrentProcess(), wintypes.HANDLE(-1).value)

    def test_IsWow64Process(self):
        current_process = self.__dll.GetCurrentProcess()
        import platform
        python_arch = platform.architecture()[0]
        PFALSE = pointer(wintypes.BOOL(False))
        is_wow = self.__dll.IsWow64Process(current_process, PFALSE)
        self.assertEqual(is_wow, python_arch=='32bit')

    def test_GetComputerNameA(self):
        lpBuffer = create_string_buffer(MAX_COMPUTERNAME_LENGTH)
        size = len(lpBuffer)
        p_size = pointer(wintypes.DWORD(size))
        is_success = self.__dll.GetComputerNameA(lpBuffer, p_size)
        real_hostname = gethostname()
        self.assertTrue(is_success)
        self.assertEqual(p_size.contents.value, len(real_hostname))
        self.assertEqual(lpBuffer.value.decode('utf8'), real_hostname)

class WrapedFailedKernel32TestCase(TestCase):

    def setUp(self):
        self.__dll = FailedKernel32()

    def tearDown(self):
        del self.__dll

    def test_forbidden_values(self):
        with self.assertRaises(DllError):
            self.__dll.GetCurrentProcess()
