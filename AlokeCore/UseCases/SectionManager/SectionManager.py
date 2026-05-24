from .Port.SectionRepo import SectionRepository
from enum import Enum
from ...Entity.Section.Section import Section,SectionBuilder
from ..Config.Port.ConfigHandler import IConfigHandler
from ...UseCases.Config.ConfigManager import ConfigManager

class SECTION_RESULT(Enum):
    ERROR = -2
    DEFAULT = -1
    SUCCESS = 0
    SECTION_ALREADY_EXIST = 1
    SECTION_NOT_FOUND = 2


class SectionManager:
    def __init__(self, section_runtime_repo: SectionRepository, config_manager : ConfigManager):
        self._section_runtime_repo = section_runtime_repo
        self._config_manager: ConfigManager = config_manager

    def new_section(self, name : str) -> SECTION_RESULT:

        result : SECTION_RESULT = SECTION_RESULT.DEFAULT
        section_id = self._generate_unique_section_id(name)
        section_builder = SectionBuilder()
        config_manager = ConfigManager(self._config_manager._config_handler)
        new_section = section_builder.setSectionId(section_id).setSectionName(name).setConfigHandler(config_manager).build()

        self._section_runtime_repo.add_section(new_section)


        check_success = self._section_runtime_repo.find_by_id(section_id)
        if check_success is not None:
            result = SECTION_RESULT.SUCCESS
        else:
            result = SECTION_RESULT.ERROR
        return result

    def remove_section(self, section_id : str) -> SECTION_RESULT:
        result : SECTION_RESULT = SECTION_RESULT.DEFAULT
        self._section_runtime_repo.remove_section(section_id)
        check_success = self._section_runtime_repo.find_by_id(section_id)
        if check_success is None:
            result = SECTION_RESULT.SUCCESS
        else:
            result = SECTION_RESULT.ERROR
        return result

    def find_section_by_id(self, section_id : str) -> Section | None:
        return self._section_runtime_repo.find_by_id(section_id)

    def all_sections(self):
        pass

    def _generate_unique_section_id(self, name: str) -> str:
        return f"section_{hash(name) % 1000000}"