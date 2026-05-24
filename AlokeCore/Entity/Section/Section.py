from .Port import I_ConfigManager
from typing import Any



class Section:
    def __init__(self,
                 section_name: str,
                 section_id: str,
                 config_manager : I_ConfigManager):
        self.section_name = section_name
        self.section_id = section_id
        self.configHandler : I_ConfigManager = config_manager
        self.configDict : dict[str, Any] = {}

    def loadConfig(self):
        self.configDict = self.configHandler.loadAllConfig(self.section_id)

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
    def setConfigManager(self, config_manager : I_ConfigManager):
        self.config_manager = config_manager
        return self
    def build(self) -> Section:
        return Section(self.section_name,
                       self.section_id,
                       self.config_manager)
