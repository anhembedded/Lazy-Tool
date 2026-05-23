import json
import os
from typing import Dict, List, Any
from unittest.mock import patch
import pytest

from CoreUtility.LoadConfig.LoadConfig import LoadConfigFromJson


@pytest.fixture
def config_loader() -> LoadConfigFromJson:
    """Fixture to provide a clean instance of LoadConfigFromJson."""
    return LoadConfigFromJson()


def test_get_nested_basic(config_loader):
    """Test retrieving a top-level key from a flat dictionary."""
    data = {"key": "value", "number": 42}
    assert config_loader._get_nested(data, "key") == "value"
    assert config_loader._get_nested(data, "number") == 42


def test_get_nested_deep(config_loader):
    """Test retrieving deeply nested keys using dot notation."""
    data = {
        "app": {
            "server": {
                "host": "localhost",
                "port": 8080
            }
        }
    }
    assert config_loader._get_nested(data, "app.server.host") == "localhost"
    assert config_loader._get_nested(data, "app.server.port") == 8080


def test_get_nested_empty_path(config_loader):
    """Test retrieving value with an empty path returns the whole data."""
    data = {"key": "value"}
    assert config_loader._get_nested(data, "") == data


def test_get_nested_missing_keys(config_loader):
    """Test that missing keys return the default value or the default empty string."""
    data = {"key": "value"}
    assert config_loader._get_nested(data, "missing_key") == ""
    assert config_loader._get_nested(data, "missing_key", default="fallback") == "fallback"
    assert config_loader._get_nested(data, "key.nested") == ""


def test_get_nested_non_dict_midpath(config_loader):
    """Test that attempting to query nested path on a non-dictionary value returns default."""
    data = {
        "app": "not_a_dict"
    }
    assert config_loader._get_nested(data, "app.server") == ""
    assert config_loader._get_nested(data, "app.server.host", default="fallback") == "fallback"


def test_set_nested_basic(config_loader):
    """Test setting a single top-level key using dot-notation."""
    data = {}
    config_loader._set_nested(data, "key", "value")
    assert data == {"key": "value"}


def test_set_nested_deep(config_loader):
    """Test setting nested keys, creating intermediate dicts as needed."""
    data = {}
    config_loader._set_nested(data, "app.server.host", "localhost")
    assert data == {"app": {"server": {"host": "localhost"}}}


def test_set_nested_overwrite_non_dict(config_loader):
    """Test that setting a nested key overwrites a non-dict value in the middle path."""
    data = {"app": "not_a_dict"}
    config_loader._set_nested(data, "app.server.port", 8080)
    assert data == {"app": {"server": {"port": 8080}}}


def test_set_nested_empty_path_raises(config_loader):
    """Test that setting a value with an empty path raises ValueError."""
    data = {}
    with pytest.raises(ValueError, match="Path must be a non-empty string"):
        config_loader._set_nested(data, "", "value")


def test_load_success(config_loader, tmp_path):
    """Test loading specified configuration keys using the legacy Load wrapper."""
    config_data = {
        "database": {"url": "postgresql://localhost:5432"},
        "version": "1.0.0"
    }
    test_file = tmp_path / "config.json"
    test_file.write_text(json.dumps(config_data), encoding="utf-8")

    result = config_loader.Load(str(test_file), ["database.url", "version"])
    assert result == {
        "database.url": "postgresql://localhost:5432",
        "version": "1.0.0"
    }


def test_load_by_keys_success(config_loader, tmp_path):
    """Test LoadByKeys retrieving nested values from file."""
    config_data = {
        "app": {"host": "127.0.0.1"}
    }
    test_file = tmp_path / "config.json"
    test_file.write_text(json.dumps(config_data), encoding="utf-8")

    result = config_loader.LoadByKeys(str(test_file), ["app.host", "app.port"])
    assert result == {
        "app.host": "127.0.0.1",
        "app.port": ""
    }


def test_load_all_success(config_loader, tmp_path):
    """Test LoadAll retrieving the entire config dictionary."""
    config_data = {"key1": "val1", "key2": "val2"}
    test_file = tmp_path / "config.json"
    test_file.write_text(json.dumps(config_data), encoding="utf-8")

    assert config_loader.LoadAll(str(test_file)) == config_data


def test_load_file_not_found(config_loader, tmp_path):
    """Test that loading from a non-existent file raises FileNotFoundError."""
    non_existent_file = tmp_path / "missing_config.json"
    with pytest.raises(FileNotFoundError, match="File not found"):
        config_loader.LoadByKeys(str(non_existent_file), ["some.key"])


def test_save_success(config_loader, tmp_path):
    """Test saving configuration data to a JSON file."""
    test_file = tmp_path / "saved_config.json"
    data_to_save = {"theme": "dark"}

    config_loader.Save(str(test_file), data_to_save)

    assert os.path.exists(test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        assert json.load(f) == data_to_save


def test_save_type_error(config_loader, tmp_path):
    """Test that Save raises TypeError if data is not a dictionary."""
    test_file = tmp_path / "invalid_data.json"
    with pytest.raises(TypeError, match="data must be a dict"):
        config_loader.Save(str(test_file), "not a dict")  # type: ignore


def test_save_invalid_path(config_loader):
    """Test saving to a path that is OS-invalid raises FileNotFoundError or OSError."""
    invalid_path = "C:\\invalid?:directory*name\\config.json"
    with pytest.raises((FileNotFoundError, OSError)):
        config_loader.Save(invalid_path, {"key": "value"})


def test_save_by_keys_new_file(config_loader, tmp_path):
    """Test SaveByKeys when target file does not exist (creates file)."""
    test_file = tmp_path / "new_by_keys.json"
    kv = {"a.b": 1, "c": "hello"}

    config_loader.SaveByKeys(str(test_file), kv)

    assert os.path.exists(test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        assert json.load(f) == {"a": {"b": 1}, "c": "hello"}


def test_save_by_keys_merge(config_loader, tmp_path):
    """Test SaveByKeys merges new keys with existing JSON file."""
    test_file = tmp_path / "merge.json"
    existing = {"a": {"b": 1}, "old": "keep"}
    test_file.write_text(json.dumps(existing), encoding="utf-8")

    kv = {"a.c": 2, "new": "added"}
    config_loader.SaveByKeys(str(test_file), kv)

    with open(test_file, "r", encoding="utf-8") as f:
        assert json.load(f) == {
            "a": {"b": 1, "c": 2},
            "old": "keep",
            "new": "added"
        }


def test_save_by_keys_invalid_json_overwrite(config_loader, tmp_path):
    """Test SaveByKeys overwrites/starts fresh if the existing file has invalid JSON."""
    test_file = tmp_path / "invalid.json"
    test_file.write_text("invalid json string {", encoding="utf-8")

    kv = {"a": 1}
    config_loader.SaveByKeys(str(test_file), kv)

    with open(test_file, "r", encoding="utf-8") as f:
        assert json.load(f) == {"a": 1}


def test_save_by_keys_empty_path_raises(config_loader, tmp_path):
    """Test SaveByKeys raises ValueError if an empty path key is supplied."""
    test_file = tmp_path / "exception.json"
    with pytest.raises(ValueError, match="Path must be a non-empty string"):
        config_loader.SaveByKeys(str(test_file), {"": 1})


def test_delete_success(config_loader, tmp_path):
    """Test deleting an existing configuration file."""
    test_file = tmp_path / "temp_config.json"
    test_file.write_text("{}", encoding="utf-8")

    assert os.path.exists(test_file)
    config_loader.Delete(str(test_file))
    assert not os.path.exists(test_file)


def test_delete_file_not_found(config_loader, tmp_path):
    """Test that deleting a non-existent file raises FileNotFoundError."""
    non_existent_file = tmp_path / "missing_file.json"
    with pytest.raises(FileNotFoundError, match="File not found"):
        config_loader.Delete(str(non_existent_file))


def test_delete_os_error(config_loader):
    """Test that Delete raises OSError when os.remove raises another system error."""
    with patch("os.remove", side_effect=OSError("Permission Denied")):
        with pytest.raises(OSError, match="Unable to delete file"):
            config_loader.Delete("some_file_path.json")
