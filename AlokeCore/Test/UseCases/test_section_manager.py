from AlokeCore.UseCases.Config.ConfigManager import ConfigManager, IConfigHandler
from AlokeCore.UseCases.SectionManager.SectionManager import SECTION_RESULT, SectionManager


class StubConfigHandler(IConfigHandler):
    def loadAllConfig(self, config_file: str) -> dict[str, str]:
        return {"config_file": config_file}

    def saveAllConfig(self, config_dict: dict[str, str], config_file: str) -> None:
        return None

    def getConfig(self, path: str, config_keys: list[str], config_file: str) -> dict[str, str]:
        return {key: "" for key in config_keys}

    def setConfig(self, path: str, config_dict: dict[str, str], config_file: str) -> None:
        return None


def test_new_section_creates_section_and_stores_it_in_repository():
    handler = StubConfigHandler()
    manager = SectionManager(ConfigManager(handler))

    section = manager.new_section("Section 1")

    assert section.name() == "Section 1"
    assert section.id() == manager._generate_unique_section_id("Section 1")
    assert manager.find_section_by_id(section.id()) is section
    assert section.configManager is not manager._config_manager
    assert isinstance(section.configManager, ConfigManager)
    assert section.configManager._config_handler is handler


def test_remove_section_returns_success_and_removes_existing_section():
    manager = SectionManager(ConfigManager(StubConfigHandler()))
    section = manager.new_section("Section 1")

    result = manager.remove_section(section.id())

    assert result is SECTION_RESULT.SUCCESS
    assert manager.find_section_by_id(section.id()) is None
