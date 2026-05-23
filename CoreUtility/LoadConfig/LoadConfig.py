import json
import os
from typing import Any, Dict, List
from CoreUtility.LoadConfig.I_LoadConfig import I_ConfigHandle

# Test file: CoreUtility\Test\CoreUtility\LoadConfig\test_LoadConfig.py

class LoadConfigFromJson(I_ConfigHandle):
    """
    Concrete implementation that loads, saves, deletes JSON config files.
    Supports nested keys using dot-separated paths (e.g., 'a.b.c').
    """

    def __init__(self):
        pass

    def _get_nested(self, data: dict, path: str, default: Any = "") -> Any:
        keys = path.split(".") if path else []
        current = data
        for k in keys:
            if isinstance(current, dict):
                if k in current:
                    current = current[k]
                else:
                    return default
            else:
                return default
        return current

    def _set_nested(self, data: dict, path: str, value: Any) -> None:
        """
        Set value into nested dict creating intermediate dicts as needed.
        Example: path 'a.b.c' will create data['a']['b']['c'] = value
        """
        if not path:
            raise ValueError("Path must be a non-empty string")
        keys = path.split(".")
        d = data
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    def _read_file(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, file_path: str, data: Dict[str, Any]) -> None:
        dirpath = os.path.dirname(file_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        # Use a temp file for safer writes
        tmp_path = f"{file_path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, file_path)

    def Load(self, file_path: str, list_key: List[str]) -> Dict[str, Any]:
        """Loads specified configuration keys from a JSON file. Satisfies I_LoadConfig protocol."""
        return self.LoadByKeys(file_path, list_key)

    def LoadByKeys(self, file_path: str, list_key: List[str]) -> Dict[str, Any]:
        data = self._read_file(file_path)
        return {key: self._get_nested(data, key) for key in list_key}

    def LoadAll(self, file_path: str) -> Dict[str, Any]:
        return self._read_file(file_path)

    def Save(self, file_path: str, data: Dict[str, Any]) -> None:
        # Validate data is serializable
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        self._write_file(file_path, data)

    def SaveByKeys(self, file_path: str, kv: Dict[str, Any]) -> None:
        """
        Merge or create keys in the JSON file using dot-path keys.
        kv example: {"a.b.c": 1, "a.f": "x"}
        """
        # Load existing or start new
        data = {}
        if os.path.exists(file_path):
            try:
                data = self._read_file(file_path)
            except json.JSONDecodeError:
                # If file exists but invalid JSON, overwrite with new structure
                data = {}

        for path, value in kv.items():
            self._set_nested(data, path, value)

        self._write_file(file_path, data)

    def Delete(self, file_path: str) -> None:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except OSError as e:
            raise OSError(f"Unable to delete file {file_path}: {e}")
