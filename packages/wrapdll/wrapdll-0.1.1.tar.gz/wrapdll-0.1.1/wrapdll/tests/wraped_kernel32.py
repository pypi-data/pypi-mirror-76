from ctypes import *
from wrapdll import BaseDllWrapper, wrapdll, forbidden_values, allowed_values


MAX_COMPUTERNAME_LENGTH = 32

class Kernel32(BaseDllWrapper):
    """
    A wrapper to ctypes.windll.kernel32
    """

    def __init__(self):
        # Doesn't use windll.kernel32 in order to not change it
        super().__init__(windll.LoadLibrary('kernel32'))

    @wrapdll
    def GetCurrentProcess(self) -> wintypes.HANDLE:
        """
        Retrieves a pseudo handle for the current process.
        """
        pass

    @forbidden_values(0, exception=lambda x: WinError())
    @wrapdll
    def IsWow64Process(self, hProcess: wintypes.HANDLE, Wow64Process: wintypes.PBOOL) -> wintypes.BOOL:
        """
        Determines whether the specified process is running under WOW64 or an Intel64 of x64 processor.
        """
        pass

    @forbidden_values(0, exception=lambda x: WinError())
    @wrapdll
    def GetComputerNameA(lpBuffer: wintypes.LPSTR, nSize: wintypes.LPDWORD) -> wintypes.BOOL:
        """
        Retrieves the NetBIOS name of the local computer. 
        This name is established at system startup, when the system reads it from the registry.
        """
        pass

class FailedKernel32(BaseDllWrapper):
    def __init__(self):
        # Doesn't use windll.kernel32 in order to not change it
        super().__init__(windll.LoadLibrary('kernel32'))

    @forbidden_values(wintypes.HANDLE(-1))
    @wrapdll
    def GetCurrentProcess(self) -> wintypes.HANDLE:
        """
        Retrieves a pseudo handle for the current process.
        """
        pass