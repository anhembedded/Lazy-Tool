import os
import subprocess
import ctypes

from .os_system_call_protocol import OsSystemCall


class WindowsSystemCall(OsSystemCall):
    def shutdown(self) -> None:
        subprocess.run(["shutdown", "/s", "/t", "0"], check=True, shell=False)

    def restart(self) -> None:
        subprocess.run(["shutdown", "/r", "/t", "0"], check=True, shell=False)

    def hibernate(self) -> None:
        subprocess.run(["shutdown", "/h"], check=True, shell=False)

    def sleep(self) -> None:
        # Using rundll32 for suspend; may require privileges
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True, shell=False)

    def run_file_with_default_app(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        os.startfile(file_path)

    def run_file_with_default_as_admin(self, file_path: str) -> None:
        # Use ShellExecute with verb "runas" to elevate
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        try:
            # ShellExecuteW returns >32 on success
            rc = ctypes.windll.shell32.ShellExecuteW(None, "runas", file_path, None, None, 1)
            if rc <= 32:
                raise OSError(f"ShellExecute failed with code {rc}")
        except Exception as e:
            raise PermissionError("Failed to run as admin") from e

    def stop_process_by_name(self, process_name: str) -> None:
        subprocess.run(["taskkill", "/f", "/im", process_name], check=True, shell=False)

    def _is_could_run_as_admin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
