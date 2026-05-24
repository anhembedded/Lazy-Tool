
from typing import Any
from ast import Dict
from CoreUtility.OsSystemCall import SystemCallFactory
from typing import List
from CoreUtility.LoadConfig.I_LoadConfig import I_ConfigHandle
from CoreUtility.LoadConfig.LoadConfig import LoadConfigFromJson


class ConfigHandler:
    def __init__(self):
        self.loadConfigHandler : I_ConfigHandle = LoadConfigFromJson()
        self.result :   dict[str, Any] = {}

    def loadAllConfig(self, file_dir : str ) -> dict[str, Any]:
        self.result = self.loadConfigHandler.LoadAll(file_dir)
        return self.result

    def loadConfig(self, file_dir : str , config_keys : list[str]) -> dict[str, Any]:
        self.result = self.loadConfigHandler.Load(file_dir, config_keys)
        return self.result

    def setConfig(self, file_dir : str , config_dict : dict[str, Any]) -> None:
        self.loadConfigHandler.Save(file_dir, config_dict)
