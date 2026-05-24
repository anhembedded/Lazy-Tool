from abc import ABC, abstractmethod
from ....Entity.Section.Port import CONFIG_KEY

class IConfigHandler(ABC):
    @abstractmethod
    def loadAllConfig(self, config_file: str) -> dict[str, str]: pass
    @abstractmethod
    def saveAllConfig(self, config_dict: dict[str, str], config_file: str) -> None : pass
    @abstractmethod
    def getConfig(self, path: str, config_keys: list[str], config_file: str) -> dict[str, str]: pass
    @abstractmethod
    def setConfig(self, path: str, config_dict: dict[str, str], config_file: str) -> None: pass


