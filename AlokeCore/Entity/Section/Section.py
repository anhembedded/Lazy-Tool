from .Port import IConfigManager
from typing import Any
from .Port import CONFIG_KEY

class Section:
    def __init__(self,
                 section_name: str,
                 section_id: str,
                 config_manager : IConfigManager):
        self.section_name = section_name
        self.section_id = section_id
        self.configManager : IConfigManager = config_manager
        self.configDict : dict[str, str] = {}

    def loadConfig(self, config_file: str) -> None:
        self.configDict = self.configManager.loadAllConfig(config_file)

    def name(self):
        return self.section_name
    def id(self):
        return self.section_id



class SectionBuilder:
    def __init__(self):
        pass
    def setSectionName(self, section_name : str):
        self.section_name = section_name
        return self
    def setSectionId(self, section_id : str):
        self.section_id = section_id
        return self
    def setConfigHandler(self, config_manager : IConfigManager):
        self.config_manager = config_manager
        return self
    def build(self) -> Section:
        return Section(self.section_name,
                       self.section_id,
                       self.config_manager)
