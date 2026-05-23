import pytest
import re
from unittest.mock import MagicMock
from pathlib import Path
from typing import List
from CoreUtility.FileHandle.FileHandler import FileHandler
from CoreUtility.FileHandle.I_FileHandler import FileInfo, FileRepository
from CoreUtility.OsSystemCall import OsSystemCall

class DummyFileRepository(FileRepository):
    def get_all(self) -> List[FileInfo]:
        return self.file_list
        
    def findByName(self, name: str) -> FileInfo:
        for file in self.file_list:
            if file.name == name:
                return file
        raise ValueError("Not found")
        
    def findByType(self, file_type: str) -> List[FileInfo]:
        return [f for f in self.file_list if f.type == file_type]
        
    def clear(self) -> None:
        self.file_list.clear()

def test_fileinfo_dataclass():
    info = FileInfo(path="/fake/path.txt", name="path.txt", type="txt")
    assert info.path == "/fake/path.txt"
    assert info.name == "path.txt"
    assert info.type == "txt"

class TestFileHandler:
    @pytest.fixture
    def mock_os_system_call(self):
        return MagicMock(spec=OsSystemCall)

    @pytest.fixture
    def handler(self, mock_os_system_call):
        repo = DummyFileRepository([])
        return FileHandler(repo, mock_os_system_call)
        
    def test_get_files_by_type_regex(self, handler, tmp_path):
        # Create test files
        (tmp_path / "hello.txt").write_text("hello")
        (tmp_path / "data.csv").write_text("1,2,3")
        (tmp_path / "image.png").write_text("png")
        (tmp_path / "log_2023.txt").write_text("log")
        (tmp_path / "123_test.txt").write_text("num test")
        
        # Test exact extension regex
        result1 = handler.GetFilesByType(str(tmp_path), r"\.txt$")
        names1 = {info.name for info in result1}
        assert names1 == {"hello.txt", "log_2023.txt", "123_test.txt"}
        assert all(info.type == "txt" for info in result1)
        
        # Test word matching regex (files with 'log' in name)
        result2 = handler.GetFilesByType(str(tmp_path), r"log")
        names2 = {info.name for info in result2}
        assert names2 == {"log_2023.txt"}
        
        # Test digit matching regex
        result3 = handler.GetFilesByType(str(tmp_path), r"^\d+")
        names3 = {info.name for info in result3}
        assert names3 == {"123_test.txt"}
        
        # Test match everything (.*)
        result4 = handler.GetFilesByType(str(tmp_path), r".*")
        assert len(result4) == 5
        
        # Test pattern: .*abc* (matches 'ab' followed by zero or more 'c')
        (tmp_path / "helloab.txt").write_text("ab")
        (tmp_path / "helloabc.txt").write_text("abc")
        (tmp_path / "helloabcc.txt").write_text("abcc")
        result5 = handler.GetFilesByType(str(tmp_path), r".*abc*")
        names5 = {info.name for info in result5}
        assert "helloab.txt" in names5
        assert "helloabc.txt" in names5
        assert "helloabcc.txt" in names5
        
        # Test invalid regex pattern (*)
        with pytest.raises(re.error):
            handler.GetFilesByType(str(tmp_path), r"*")

    def test_get_files_by_type_non_existent_dir(self, handler, tmp_path):
        fake_path = tmp_path / "does_not_exist"
        result = handler.GetFilesByType(str(fake_path), r".*")
        assert result is None

    def test_open_file_success(self, handler, mock_os_system_call, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("dummy content", encoding="utf-8")
        
        info = FileInfo(path=str(test_file), name="test.txt", type="txt")
        handler.open_file(info)
        
        mock_os_system_call.run_file_with_default_app.assert_called_once_with(str(test_file))

    def test_open_file_not_found(self, handler, mock_os_system_call, tmp_path):
        fake_file = tmp_path / "missing.txt"
        info = FileInfo(path=str(fake_file), name="missing.txt", type="txt")
        
        with pytest.raises(FileNotFoundError, match="File not found"):
            handler.open_file(info)
            
        mock_os_system_call.run_file_with_default_app.assert_not_called()
