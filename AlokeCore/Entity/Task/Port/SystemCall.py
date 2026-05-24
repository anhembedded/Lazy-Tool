from .....CoreUtility.OsSystemCall import SystemCallFactory, OsSystemCall


class SystemCall:
    def __init__(self):
        self.os_system_call :  OsSystemCall = SystemCallFactory().create_by_current_os()

    def run_file_with_default_as_admin(self, file_path: str) -> None:
        self.os_system_call.run_file_with_default_as_admin(file_path)

    def stop_process_by_name(self, process_name: str) -> None:
        self.os_system_call.stop_process_by_name(process_name)