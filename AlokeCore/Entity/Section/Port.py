from typing import Protocol
from enum import Enum
from abc import abstractmethod


class CONFIG_KEY(Enum):
    PACKAGE_DIR = "package_dir"
    SVN_DIR = "svn_dir"
    VISUAL_STUDIO_DIR_EXE = "visual_studio_dir"
    PROJECT_SOLUTION_DIR = "project_solution_dir"
    WEB_HOOK_URL = "web_hook_url"


class IConfigManager:
    def __init__(self, config_dir: str) -> None: ...

    @abstractmethod
    def loadAllConfig(self, file_dir: str) -> dict[str, str]:
        ...

    @abstractmethod
    def saveConfig(self, file_dir: str, config_dict: dict[str, str]) -> None:
        ...

    @abstractmethod
    def saveAllConfig(self, config_dict: dict[str, str], config_file: str) -> None:
        ...

    @abstractmethod
    def getConfig(self, path: str, config_keys: list[str], config_file: str) -> dict[str, str]:
        ...

    @abstractmethod
    def setConfig(self, path: str, config_dict: dict[str, str], config_file: str) -> None:
        ...

