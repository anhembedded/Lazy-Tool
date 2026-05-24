from AlokeCore.Entity.Task.ITaskBase import ITaskBase
from .Port.SystemCall import SystemCall

class Task_Stop_Process_With_Name(ITaskBase):
    def __init__(self,  process_name : list[str]):
        super().__init__("Stop Process With Name")
        self.process_name = process_name
        self.system_call = SystemCall()
    def execute(self):
        for name in self.process_name:
            self.system_call.stop_process_by_name(name)