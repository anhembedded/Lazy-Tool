from AlokeCore.Entity.Section.Section import IConfigManager, SectionBuilder


class DummyConfigManager(IConfigManager):
    def __init__(self, config=None):
        self.config = config or {}
        self.loaded_paths = []

    def loadAllConfig(self, file_dir: str) -> dict[str, str]:
        self.loaded_paths.append(file_dir)
        return self.config


def test_section_builder_builds_section_with_expected_values():
    config_manager = DummyConfigManager()

    section = (
        SectionBuilder()
        .setSectionName("Section 1")
        .setSectionId("section_1")
        .setConfigHandler(config_manager)
        .build()
    )

    assert section.name() == "Section 1"
    assert section.id() == "section_1"
    assert section.configManager is config_manager


def test_section_load_config_populates_config_dict():
    config_manager = DummyConfigManager({"theme": "dark"})
    section = (
        SectionBuilder()
        .setSectionName("Section 1")
        .setSectionId("section_1")
        .setConfigHandler(config_manager)
        .build()
    )

    section.loadConfig("config.json")

    assert config_manager.loaded_paths == ["config.json"]
    assert section.configDict == {"theme": "dark"}
