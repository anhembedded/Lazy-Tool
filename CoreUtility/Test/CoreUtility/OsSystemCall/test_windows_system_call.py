import unittest
from unittest.mock import patch, MagicMock
import os
from CoreUtility.OsSystemCall.windows_system_call import WindowsSystemCall


class TestWindowsSystemCall(unittest.TestCase):
    """Test cases for WindowsSystemCall"""

    def setUp(self):
        """Set up test fixtures"""
        self.windows_call = WindowsSystemCall()

    @patch("subprocess.run")
    def test_shutdown_success(self, mock_run):
        """Test successful shutdown command"""
        self.windows_call.shutdown()
        mock_run.assert_called_once_with(
            ["shutdown", "/s", "/t", "0"], check=True, shell=False
        )

    @patch("subprocess.run", side_effect=Exception("Command failed"))
    def test_shutdown_failure(self, mock_run):
        """Test shutdown raises exception on failure"""
        with self.assertRaises(Exception):
            self.windows_call.shutdown()

    @patch("subprocess.run")
    def test_restart_success(self, mock_run):
        """Test successful restart command"""
        self.windows_call.restart()
        mock_run.assert_called_once_with(
            ["shutdown", "/r", "/t", "0"], check=True, shell=False
        )

    @patch("subprocess.run")
    def test_hibernate_success(self, mock_run):
        """Test successful hibernate command"""
        self.windows_call.hibernate()
        mock_run.assert_called_once_with(
            ["shutdown", "/h"], check=True, shell=False
        )

    @patch("subprocess.run")
    def test_sleep_success(self, mock_run):
        """Test successful sleep command"""
        self.windows_call.sleep()
        mock_run.assert_called_once_with(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
            check=True,
            shell=False,
        )

    @patch("os.path.exists")
    @patch("os.startfile")
    def test_run_file_with_default_app_success(self, mock_startfile, mock_exists):
        """Test opening file with default app"""
        mock_exists.return_value = True
        self.windows_call.run_file_with_default_app("C:\\path\\to\\file.txt")
        mock_startfile.assert_called_once_with("C:\\path\\to\\file.txt")

    @patch("os.path.exists")
    def test_run_file_with_default_app_not_found(self, mock_exists):
        """Test opening file raises error when file not found"""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.windows_call.run_file_with_default_app("C:\\nonexistent\\file.txt")

    @patch("os.path.exists")
    @patch("ctypes.windll.shell32.ShellExecuteW")
    def test_run_file_with_default_as_admin_success(self, mock_shell_execute, mock_exists):
        """Test opening file as admin succeeds"""
        mock_exists.return_value = True
        mock_shell_execute.return_value = 42  # Success code (>32)
        self.windows_call.run_file_with_default_as_admin("C:\\path\\to\\file.txt")
        mock_shell_execute.assert_called_once()

    @patch("os.path.exists")
    def test_run_file_with_default_as_admin_file_not_found(self, mock_exists):
        """Test opening file as admin raises error when file not found"""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.windows_call.run_file_with_default_as_admin("C:\\nonexistent\\file.txt")

    @patch("os.path.exists")
    @patch("ctypes.windll.shell32.ShellExecuteW")
    def test_run_file_with_default_as_admin_shell_execute_fails(self, mock_shell_execute, mock_exists):
        """Test opening file as admin raises error on ShellExecute failure"""
        mock_exists.return_value = True
        mock_shell_execute.return_value = 5  # Error code (<=32)
        with self.assertRaises(PermissionError):
            self.windows_call.run_file_with_default_as_admin("C:\\path\\to\\file.txt")

    @patch("subprocess.run")
    def test_stop_process_by_name_success(self, mock_run):
        """Test stopping process by name"""
        self.windows_call.stop_process_by_name("notepad.exe")
        mock_run.assert_called_once_with(
            ["taskkill", "/f", "/im", "notepad.exe"], check=True, shell=False
        )

    @patch("ctypes.windll.shell32.IsUserAnAdmin")
    def test_is_could_run_as_admin_true(self, mock_is_admin):
        """Test admin check returns True when user is admin"""
        mock_is_admin.return_value = 1
        self.assertTrue(self.windows_call._is_could_run_as_admin())

    @patch("ctypes.windll.shell32.IsUserAnAdmin")
    def test_is_could_run_as_admin_false(self, mock_is_admin):
        """Test admin check returns False when user is not admin"""
        mock_is_admin.return_value = 0
        self.assertFalse(self.windows_call._is_could_run_as_admin())

    @patch("ctypes.windll.shell32.IsUserAnAdmin", side_effect=Exception("API error"))
    def test_is_could_run_as_admin_exception(self, mock_is_admin):
        """Test admin check returns False on exception"""
        self.assertFalse(self.windows_call._is_could_run_as_admin())


if __name__ == "__main__":
    unittest.main()
