import enum
import os
import subprocess
import ctypes
from typing import Type


class OS_Type(enum.Enum):
    LINUX = 1
    WINDOWS = 2


class OsSystemCallInterface:
    def shutdown(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError

    def hibernate(self):
        raise NotImplementedError

    def sleep(self):
        raise NotImplementedError

    def run_file_with_default_app(self, file_path: str):
        raise NotImplementedError

    def run_file_with_default_as_admin(self, file_path: str):
        raise NotImplementedError

    def _is_could_run_as_admin(self) -> bool:
        raise NotImplementedError


class LinuxSystemCall(OsSystemCallInterface):
    def shutdown(self):
        subprocess.run(["shutdown", "now"])

    def restart(self):
        subprocess.run(["reboot"])

    def hibernate(self):
        subprocess.run(["systemctl", "hibernate"])

    def sleep(self):
        subprocess.run(["systemctl", "suspend"])

    def run_file_with_default_app(self, file_path: str):
        subprocess.run(["xdg-open", file_path])

    def run_file_with_default_as_admin(self, file_path: str):
        if self._is_could_run_as_admin():
            subprocess.run(["pkexec", "xdg-open", file_path])
        else:
            raise PermissionError("You are not admin")

    def _is_could_run_as_admin(self) -> bool:
        return os.geteuid() == 0


class WindowsSystemCall(OsSystemCallInterface):
    def shutdown(self):
        subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)

    def restart(self):
        subprocess.run(["shutdown", "/r", "/t", "0"], shell=True)

    def hibernate(self):
        subprocess.run(["shutdown", "/h"], shell=True)

    def sleep(self):
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], shell=True
        )

    def run_file_with_default_app(self, file_path: str):
        os.startfile(file_path)

    def run_file_with_default_as_admin(self, file_path: str):
        if self._is_could_run_as_admin():
            subprocess.run(["runas", "/user:Administrator", file_path], shell=True)
        else:
            raise PermissionError("You are not admin")

    def _is_could_run_as_admin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False


class SystemCallFactory:
    def __init__(self):
        pass

    def create_by_type(self, type: OS_Type) -> OsSystemCallInterface:
        if type == OS_Type.LINUX:
            return LinuxSystemCall()
        elif type == OS_Type.WINDOWS:
            return WindowsSystemCall()
        else:
            raise ValueError("Invalid OS type")
