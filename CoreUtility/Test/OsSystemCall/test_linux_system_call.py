import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import sys
from CoreUtility.OsSystemCall.linux_system_call import LinuxSystemCall


class TestLinuxSystemCall(unittest.TestCase):
    """Test cases for LinuxSystemCall"""

    def setUp(self):
        """Set up test fixtures"""
        self.linux_call = LinuxSystemCall()

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_shutdown_success(self, mock_which, mock_run):
        """Test successful shutdown command"""
        mock_which.return_value = "/usr/sbin/shutdown"
        self.linux_call.shutdown()
        mock_run.assert_called_once_with(["shutdown", "now"], check=True)

    @patch("shutil.which")
    def test_shutdown_command_not_found(self, mock_which):
        """Test shutdown raises error when command not found"""
        mock_which.return_value = None
        with self.assertRaises(FileNotFoundError) as context:
            self.linux_call.shutdown()
        self.assertIn("shutdown command not found", str(context.exception))

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_restart_success(self, mock_which, mock_run):
        """Test successful restart command"""
        mock_which.return_value = "/usr/sbin/reboot"
        self.linux_call.restart()
        mock_run.assert_called_once_with(["reboot"], check=True)

    @patch("shutil.which")
    def test_restart_command_not_found(self, mock_which):
        """Test restart raises error when command not found"""
        mock_which.return_value = None
        with self.assertRaises(FileNotFoundError) as context:
            self.linux_call.restart()
        self.assertIn("reboot command not found", str(context.exception))

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_hibernate_success(self, mock_which, mock_run):
        """Test successful hibernate command"""
        mock_which.return_value = "/usr/bin/systemctl"
        self.linux_call.hibernate()
        mock_run.assert_called_once_with(["systemctl", "hibernate"], check=True)

    @patch("shutil.which")
    def test_hibernate_systemctl_not_found(self, mock_which):
        """Test hibernate raises error when systemctl not found"""
        mock_which.return_value = None
        with self.assertRaises(FileNotFoundError) as context:
            self.linux_call.hibernate()
        self.assertIn("systemctl not found", str(context.exception))

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_sleep_success(self, mock_which, mock_run):
        """Test successful sleep command"""
        mock_which.return_value = "/usr/bin/systemctl"
        self.linux_call.sleep()
        mock_run.assert_called_once_with(["systemctl", "suspend"], check=True)

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_run_file_with_default_app_success(self, mock_which, mock_run):
        """Test opening file with default app"""
        mock_which.return_value = "/usr/bin/xdg-open"
        self.linux_call.run_file_with_default_app("/path/to/file.txt")
        mock_run.assert_called_once_with(["xdg-open", "/path/to/file.txt"], check=True)

    @patch("shutil.which")
    def test_run_file_with_default_app_xdg_not_found(self, mock_which):
        """Test opening file raises error when xdg-open not found"""
        mock_which.return_value = None
        with self.assertRaises(FileNotFoundError) as context:
            self.linux_call.run_file_with_default_app("/path/to/file.txt")
        self.assertIn("xdg-open not found", str(context.exception))

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_stop_process_by_name_success(self, mock_which, mock_run):
        """Test stopping process by name"""
        mock_which.return_value = "/usr/bin/pkill"
        self.linux_call.stop_process_by_name("firefox")
        mock_run.assert_called_once_with(["pkill", "-f", "firefox"], check=True)

    @unittest.skipIf(not hasattr(os, "geteuid"), "geteuid not available on this platform")
    @patch("CoreUtility.OsSystemCall.linux_system_call.os")
    def test_is_could_run_as_admin_true(self, mock_os):
        """Test admin check returns True when user is root"""
        mock_os.geteuid.return_value = 0
        self.assertTrue(self.linux_call._is_could_run_as_admin())

    @unittest.skipIf(not hasattr(os, "geteuid"), "geteuid not available on this platform")
    @patch("CoreUtility.OsSystemCall.linux_system_call.os")
    def test_is_could_run_as_admin_false(self, mock_os):
        """Test admin check returns False when user is not root"""
        mock_os.geteuid.return_value = 1000
        self.assertFalse(self.linux_call._is_could_run_as_admin())

    @unittest.skipIf(not hasattr(os, "geteuid"), "geteuid not available on this platform")
    @patch("CoreUtility.OsSystemCall.linux_system_call.os")
    def test_is_could_run_as_admin_fallback_to_getuid(self, mock_os):
        """Test admin check falls back to getuid when geteuid not available"""
        # Simulate geteuid raising AttributeError
        mock_os.geteuid.side_effect = AttributeError
        mock_os.getuid.return_value = 0
        self.assertTrue(self.linux_call._is_could_run_as_admin())


if __name__ == "__main__":
    unittest.main()
