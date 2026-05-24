from abc import abstractmethod

from ...Entity.Section.Port import CONFIG_KEY
from .Port.ConfigHandler import IConfigHandler
from ...Entity.Section.Port import IConfigManager
class ConfigManager(IConfigManager):
    def __init__(self, config_handler: IConfigHandler):
        self._config_handler = config_handler

    def setConfigDir(self, config_dir: str):
        self._config_dir = config_dir

    def loadAllConfig(self, file_dir: str) -> dict[str, str]:
        return self._config_handler.loadAllConfig(file_dir)

    def saveAllConfig(self, config_dict: dict[str, str], config_file: str) -> None:
        self._config_handler.saveAllConfig(config_dict, config_file)

    def getConfig(self, path: str, config_keys: list[str], config_file: str) -> dict[str, str]:
        return self._config_handler.getConfig(path, config_keys, config_file)

    def setConfig(self, path: str, config_dict: dict[str, str], config_file: str) -> None:
        self._config_handler.setConfig(path, config_dict, config_file)
