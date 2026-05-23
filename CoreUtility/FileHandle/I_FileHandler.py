from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class FileInfo:
    path: str
    name: str
    type: str

class FileRepository(ABC):
    def __init__(self, file_list : List[FileInfo]) -> None:
        self.file_list = file_list
    @abstractmethod
    def get_all(self) -> List[FileInfo]:
        pass
    @abstractmethod
    def findByName(self, name: str) -> FileInfo:
        pass
    @abstractmethod
    def findByType(self, type: str) -> List[FileInfo]:
        pass
    def clear(self) -> None:
        pass