import dataclasses
from enum import Enum
from typing import Any
from AlokeCore.Entity.ConfigManager.I_ConfigManager import I_ConfigManager


class configKey(Enum):
    PACKAGE_DIR = "package_dir"
    SVN_DIR = "svn_dir"
    VISUAL_STUDIO_DIR = "visual_studio_dir"
    WEB_HOOK_URL = "web_hook_url"


class WorkingDir:
    def __init__(self, config_manager : I_ConfigManager):
        self._CONFIG : dict[str, Any] = {}
        self._config_manager = config_manager

    def loadConfig(self, file_dir : str):
        self._CONFIG = self._config_manager.loadAllConfig(file_dir)

    def getConfig(self, configKey : configKey) -> Any:
        return self._CONFIG.get(configKey.value)