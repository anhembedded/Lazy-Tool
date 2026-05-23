from typing import Optional
import sys
import os
from AlokeCore.Entity.WorkingDir.WoringDir import WorkingDir, configKey
import subprocess
from CoreUtility.OsSystemCall.system_call_factory import OsSystemCall , SystemCallFactory


class ManualTask:
    def __init__(self,WorkingDir : WorkingDir):
        self.workingDir = WorkingDir
        self.os_system_call :  OsSystemCall = SystemCallFactory().create_by_current_os()

    def Open_Aloke_Sln(self) -> None:
        solution_dir = self.workingDir.getConfig(configKey.PROJECT_SOLUTION_DIR)
        if solution_dir is None:
            raise ValueError("Project solution directory not configured")
        else:
            self.os_system_call.run_file_with_default_as_admin(solution_dir)
    def Stop_Process_With_Name(self, process_name : list[str]) -> None:
        for name in process_name:
            self.os_system_call.stop_process_by_name(name)
