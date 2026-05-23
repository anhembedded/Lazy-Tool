import unittest
from CoreUtility.OsSystemCall.os_types import OS_Type


class TestOsTypes(unittest.TestCase):
    """Test cases for OS_Type enum"""

    def test_os_type_linux(self):
        """Test LINUX enum value"""
        self.assertEqual(OS_Type.LINUX.value, 1)
        self.assertEqual(OS_Type.LINUX.name, "LINUX")

    def test_os_type_windows(self):
        """Test WINDOWS enum value"""
        self.assertEqual(OS_Type.WINDOWS.value, 2)
        self.assertEqual(OS_Type.WINDOWS.name, "WINDOWS")

    def test_os_type_members(self):
        """Test all enum members"""
        members = list(OS_Type)
        self.assertEqual(len(members), 2)
        self.assertIn(OS_Type.LINUX, members)
        self.assertIn(OS_Type.WINDOWS, members)

    def test_os_type_comparison(self):
        """Test OS_Type comparison"""
        self.assertEqual(OS_Type.LINUX, OS_Type.LINUX)
        self.assertNotEqual(OS_Type.LINUX, OS_Type.WINDOWS)

    def test_os_type_by_value(self):
        """Test accessing enum by value"""
        self.assertEqual(OS_Type(1), OS_Type.LINUX)
        self.assertEqual(OS_Type(2), OS_Type.WINDOWS)


if __name__ == "__main__":
    unittest.main()
