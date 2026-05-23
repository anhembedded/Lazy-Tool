from typing import List, Optional
from CoreUtility.FileHandle.I_FileHandler import FileRepository, FileInfo

class InMemoryFileRepository(FileRepository):
    def __init__(self, file_list: List[FileInfo]):
        super().__init__(file_list)

    def get_all(self) -> List[FileInfo]:
        return self.file_list

    def findByName(self, name: str) -> Optional[FileInfo]:
        for file in self.file_list:
            if file.name == name:
                return file
        return None

    def findByType(self, type: str) -> List[FileInfo]:
        return [file for file in self.file_list if file.type.lower() == type.lower()]

    def __str__(self):
        temp_s :str = "Name\tPath\tType\n"
        for file in self.file_list:
            temp_s += f"{file.name}\t{file.path}\t{file.type}\n"
        return temp_s

    def __getitem__(self, index: int) -> FileInfo:
        return self.file_list[index]

    def __len__(self) -> int:
        return len(self.file_list)   