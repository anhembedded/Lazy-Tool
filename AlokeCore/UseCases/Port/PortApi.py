from abc import ABC, abstractmethod




class ConfigHandler(ABC):
    @abstractmethod
    def loadAllConfig(self, path: str) -> dict: pass

