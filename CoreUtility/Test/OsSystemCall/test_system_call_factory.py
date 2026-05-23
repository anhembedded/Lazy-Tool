import unittest
from unittest.mock import patch, MagicMock
from CoreUtility.OsSystemCall.system_call_factory import SystemCallFactory
from CoreUtility.OsSystemCall.os_types import OS_Type
from CoreUtility.OsSystemCall.linux_system_call import LinuxSystemCall
from CoreUtility.OsSystemCall.windows_system_call import WindowsSystemCall


class TestSystemCallFactory(unittest.TestCase):
    """Test cases for SystemCallFactory"""

    def test_create_by_type_linux(self):
        """Test creating LinuxSystemCall instance"""
        result = SystemCallFactory.create_by_type(OS_Type.LINUX)
        self.assertIsInstance(result, LinuxSystemCall)

    def test_create_by_type_windows(self):
        """Test creating WindowsSystemCall instance"""
        result = SystemCallFactory.create_by_type(OS_Type.WINDOWS)
        self.assertIsInstance(result, WindowsSystemCall)

    def test_create_by_type_invalid(self):
        """Test creating with invalid OS type raises ValueError"""
        # Create an invalid enum-like value
        with self.assertRaises(ValueError) as context:
            SystemCallFactory.create_by_type("invalid_os")
        self.assertIn("Invalid OS type", str(context.exception))

    @patch("os.name", "nt")
    def test_create_by_current_os_windows(self, ):
        """Test creating instance for current OS (Windows)"""
        result = SystemCallFactory.create_by_current_os()
        self.assertIsInstance(result, WindowsSystemCall)

    @patch("os.name", "posix")
    def test_create_by_current_os_linux(self):
        """Test creating instance for current OS (Linux)"""
        result = SystemCallFactory.create_by_current_os()
        self.assertIsInstance(result, LinuxSystemCall)

    @patch("os.name", "unsupported")
    def test_create_by_current_os_unsupported(self):
        """Test creating for unsupported OS raises ValueError"""
        with self.assertRaises(ValueError) as context:
            SystemCallFactory.create_by_current_os()
        self.assertIn("Unsupported OS", str(context.exception))
        self.assertIn("unsupported", str(context.exception))

    def test_create_by_type_returns_different_instances(self):
        """Test that factory creates new instances each time"""
        instance1 = SystemCallFactory.create_by_type(OS_Type.LINUX)
        instance2 = SystemCallFactory.create_by_type(OS_Type.LINUX)
        self.assertIsNot(instance1, instance2)
        self.assertEqual(type(instance1), type(instance2))


if __name__ == "__main__":
    unittest.main()
