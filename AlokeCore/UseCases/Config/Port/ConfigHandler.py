from abc import ABC, abstractmethod
from ..ConfigType import CONFIG_KEY

class IConfigHandler(ABC):
    @abstractmethod
    def loadAllConfig(self, config_file: str) -> dict[CONFIG_KEY, str]: pass
    @abstractmethod
    def saveAllConfig(self, config_dict: dict[CONFIG_KEY, str], config_file: str) -> None : pass
    @abstractmethod
    def getConfig(self, path: str, config_keys: list[CONFIG_KEY], config_file: str) -> dict[CONFIG_KEY, str]: pass
    @abstractmethod
    def setConfig(self, path: str, config_dict: dict[CONFIG_KEY, str], config_file: str) -> None: pass


