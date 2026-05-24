from .ConfigType import CONFIG_KEY
from .Port.ConfigHandler import IConfigHandler


class ConfigManager:
    def __init__(self, config_handler: IConfigHandler):
        self._config_handler = config_handler

    def setConfigDir(self, config_dir: str):
        self._config_dir = config_dir

    def loadAllConfig(self) -> dict[CONFIG_KEY, str]:
        return self._config_handler.loadAllConfig(self._config_dir)

    def saveAllConfig(self) -> None:
        self._config_handler.saveAllConfig(self.loadAllConfig(), self._config_dir)

    def getConfig(self, path: str, config_keys: list[CONFIG_KEY]) -> dict[CONFIG_KEY, str]:
        return self._config_handler.getConfig(path, config_keys, self._config_dir)

    def setConfig(self, path: str, config_dict: dict[CONFIG_KEY, str]) -> None:
        self._config_handler.setConfig(path, config_dict, self._config_dir)