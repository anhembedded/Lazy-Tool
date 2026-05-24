from .ITaskBase import ITaskBase
from .Port.SystemCall import SystemCall


class Task_Open_AloKe_Sln(ITaskBase):
    def __init__(self, sln_dir : str):
        super().__init__("Open Aloke Solution")
        self.sln_dir = sln_dir
        self.system_call = SystemCall()

    def execute(self):
        self.system_call.run_file_with_default_as_admin(self.sln_dir)