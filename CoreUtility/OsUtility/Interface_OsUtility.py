from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

@dataclass
class ProcessInfo:
    pid: int
    name: str
    dll_name: str

class OsUtilityInterface(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def get_process_by_dinamic_lib(self, dinamic_lib_name: str) -> List[ProcessInfo]:
        pass
    @abstractmethod
    def stop_process_use_dinamic_lib(self, dinamic_lib_name: str) -> bool:
        pass
    
