from AlokeCore.Entity.Section.Section import IConfigManager, SectionBuilder
from AlokeCore.UseCases.SectionManager.SectionRepo import SectionRepository


class DummyConfigManager(IConfigManager):
    def __init__(self):
        pass

    def loadAllConfig(self, file_dir: str) -> dict[str, str]:
        return {"file_dir": file_dir}


def make_section(section_name: str = "Section 1", section_id: str = "section_1"):
    return (
        SectionBuilder()
        .setSectionName(section_name)
        .setSectionId(section_id)
        .setConfigHandler(DummyConfigManager())
        .build()
    )


def test_section_repository_adds_and_finds_section_by_id():
    repository = SectionRepository()
    section = make_section()

    repository.add_section(section)

    assert repository.find_by_id("section_1") is section


def test_section_repository_remove_section_deletes_existing_entry():
    repository = SectionRepository()
    section = make_section()
    repository.add_section(section)

    repository.remove_section("section_1")

    assert repository.find_by_id("section_1") is None


def test_section_repository_remove_missing_section_is_noop():
    repository = SectionRepository()

    repository.remove_section("missing")

    assert repository.find_by_id("missing") is None
