import os

from .os_types import OS_Type
from .os_system_call_protocol import OsSystemCall
from .linux_system_call import LinuxSystemCall
from .windows_system_call import WindowsSystemCall


class SystemCallFactory:
    @staticmethod
    def create_by_type(os_type: OS_Type) -> OsSystemCall:
        if os_type == OS_Type.LINUX:
            return LinuxSystemCall()
        if os_type == OS_Type.WINDOWS:
            return WindowsSystemCall()
        raise ValueError("Invalid OS type")

    @staticmethod
    def create_by_current_os() -> OsSystemCall:
        if os.name == "nt":
            return WindowsSystemCall()
        if os.name == "posix":
            return LinuxSystemCall()
        raise ValueError(f"Unsupported OS: {os.name}")
