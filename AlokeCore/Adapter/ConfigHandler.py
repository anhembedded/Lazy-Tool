
from abc import ABC, abstractmethod
from typing import Any
from ast import Dict
from AlokeCore.Entity.Section.Port import CONFIG_KEY
from CoreUtility.OsSystemCall import SystemCallFactory
from typing import List
from CoreUtility.LoadConfig.I_LoadConfig import I_ConfigHandle
from CoreUtility.LoadConfig.LoadConfig import LoadConfigFromJson
from ..UseCases.Config.Port.ConfigHandler import IConfigHandler

class ConfigHandler(IConfigHandler):
    def __init__(self):
        self.loadConfigHandler : I_ConfigHandle = LoadConfigFromJson()

    def loadAllConfig(self, config_file: str) -> dict[str, str]:
        result = self.loadConfigHandler.LoadAll(config_file)
        return result

    def saveAllConfig(self, config_dict: dict[str, str], config_file: str) -> None:
        self.loadConfigHandler.Save( config_file, config_dict)

    def getConfig(self, path: str, config_keys: list[str], config_file: str) -> dict[str, str]:
        result = self.loadConfigHandler.Load(path, config_keys)
        return result
    def setConfig(self, path: str, config_dict: dict[str, str], config_file: str) -> None:
        self.loadConfigHandler.Save(path, config_dict)
