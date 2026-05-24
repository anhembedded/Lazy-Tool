from AlokeCore.UseCases.Config.ConfigManager import ConfigManager, IConfigHandler


class StubConfigHandler(IConfigHandler):
    def __init__(self):
        self.calls = []

    def loadAllConfig(self, config_file: str) -> dict[str, str]:
        self.calls.append(("loadAllConfig", config_file))
        return {"config_file": config_file}

    def saveAllConfig(self, config_dict: dict[str, str], config_file: str) -> None:
        self.calls.append(("saveAllConfig", config_dict, config_file))

    def getConfig(self, path: str, config_keys: list[str], config_file: str) -> dict[str, str]:
        self.calls.append(("getConfig", path, config_keys, config_file))
        return {key: f"value_for_{key}" for key in config_keys}

    def setConfig(self, path: str, config_dict: dict[str, str], config_file: str) -> None:
        self.calls.append(("setConfig", path, config_dict, config_file))


def test_config_manager_load_all_config_delegates_to_handler():
    handler = StubConfigHandler()
    config_manager = ConfigManager(handler)

    result = config_manager.loadAllConfig("config.json")

    assert result == {"config_file": "config.json"}
    assert handler.calls == [("loadAllConfig", "config.json")]


def test_config_manager_save_all_config_delegates_to_handler():
    handler = StubConfigHandler()
    config_manager = ConfigManager(handler)

    config_manager.saveAllConfig({"theme": "dark"}, "config.json")

    assert handler.calls == [("saveAllConfig", {"theme": "dark"}, "config.json")]


def test_config_manager_get_config_delegates_to_handler():
    handler = StubConfigHandler()
    config_manager = ConfigManager(handler)

    result = config_manager.getConfig("app", ["theme"], "config.json")

    assert result == {"theme": "value_for_theme"}
    assert handler.calls == [("getConfig", "app", ["theme"], "config.json")]


def test_config_manager_set_config_delegates_to_handler():
    handler = StubConfigHandler()
    config_manager = ConfigManager(handler)

    config_manager.setConfig("app", {"theme": "dark"}, "config.json")

    assert handler.calls == [("setConfig", "app", {"theme": "dark"}, "config.json")]
