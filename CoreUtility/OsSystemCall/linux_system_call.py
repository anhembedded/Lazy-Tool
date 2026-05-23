import os
import subprocess
import shutil

from .os_system_call_protocol import OsSystemCall


class LinuxSystemCall(OsSystemCall):
    def shutdown(self) -> None:
        if shutil.which("shutdown") is None:
            raise FileNotFoundError("shutdown command not found")
        subprocess.run(["shutdown", "now"], check=True)

    def restart(self) -> None:
        if shutil.which("reboot") is None:
            raise FileNotFoundError("reboot command not found")
        subprocess.run(["reboot"], check=True)

    def hibernate(self) -> None:
        if shutil.which("systemctl") is None:
            raise FileNotFoundError("systemctl not found")
        subprocess.run(["systemctl", "hibernate"], check=True)

    def sleep(self) -> None:
        if shutil.which("systemctl") is None:
            raise FileNotFoundError("systemctl not found")
        subprocess.run(["systemctl", "suspend"], check=True)

    def run_file_with_default_app(self, file_path: str) -> None:
        if shutil.which("xdg-open") is None:
            raise FileNotFoundError("xdg-open not found")
        subprocess.run(["xdg-open", file_path], check=True)

    def run_file_with_default_as_admin(self, file_path: str) -> None:
        # Note: elevating a GUI "open" on Linux is environment-dependent and may fail.
        if not self._is_could_run_as_admin():
            # Try to use pkexec; may still fail in some desktop environments
            if shutil.which("pkexec"):
                # pkexec may not forward DISPLAY/XAUTHORITY; best-effort
                try:
                    subprocess.run(["pkexec", "xdg-open", file_path], check=True)
                    return
                except subprocess.CalledProcessError as e:
                    raise PermissionError("Failed to open as admin via pkexec") from e
            raise PermissionError("You are not admin")
        # already admin
        self.run_file_with_default_app(file_path)

    def _is_could_run_as_admin(self) -> bool:
        try:
            return os.geteuid() == 0
        except AttributeError:
            try:
                return os.getuid() == 0
            except Exception:
                return False

    def stop_process_by_name(self, process_name: str) -> None:
        subprocess.run(["pkill", "-f", process_name], check=True)
