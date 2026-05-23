from typing import List
from pathlib import Path
import re
import os
from CoreUtility.FileHandle.I_FileHandler import FileInfo, FileRepository
from CoreUtility.OsSystemCall import OsSystemCall

class FileHandler:
    def __init__(self, file_repository: FileRepository, os_system_call : OsSystemCall):
        self.file_repository = file_repository
        self.os_system_call = os_system_call
    
    def GetFilesByType(self, directory: str , type: str):
        self.file_repository.clear()
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            return

        pattern = re.compile(type)

        for root, dirs, files in os.walk(str(path)):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if pattern.search(file):
                    file_path = Path(root) / file
                    self.file_repository.file_list.append(FileInfo(
                        path=str(file_path),
                        name=file,
                        type=file_path.suffix.lstrip(".")
                    ))
        return self.file_repository.file_list

    def open_file(self, file: FileInfo):
        if not Path(file.path).exists():
            raise FileNotFoundError(f"File not found: {file.path}")

        self.os_system_call.run_file_with_default_app(file.path)