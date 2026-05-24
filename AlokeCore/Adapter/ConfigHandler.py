
from typing import Any
from ast import Dict
from CoreUtility.OsSystemCall import SystemCallFactory
from typing import List
from CoreUtility.LoadConfig.I_LoadConfig import I_ConfigHandle
from CoreUtility.LoadConfig.LoadConfig import LoadConfigFromJson
from ..UseCases.Config.Port.ConfigHandler import IConfigHandler



class ConfigHandler(IConfigHandler):
    def __init__(self):
        self.loadConfigHandler : I_ConfigHandle = LoadConfigFromJson()
        self.result : dict[Any, Any] = {}

    def loadAllConfig(self, config_file: str) -> dict[Any, Any]:
        self.result = self.loadConfigHandler.LoadAll(config_file)
        return self.result

    def loadConfig(self, config_file: str, config_keys: list[str]) -> dict[Any, Any]:
        self.result = self.loadConfigHandler.Load(config_file, config_keys)
        return self.result

    def setConfig(self, path: str, config_dict: dict[Any, str], config_file: str) -> None:
        self.loadConfigHandler.Save(config_file, config_dict)
