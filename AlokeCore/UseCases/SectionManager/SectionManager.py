from .Port.SectionRepo import ISectionRepository
from enum import Enum
from ...Entity.Section.Section import Section

class SECTION_RESULT(Enum):
    ERROR = -2
    DEFAULT = -1
    SUCCESS = 0
    SECTION_ALREADY_EXIST = 1
    SECTION_NOT_FOUND = 2


class SectionManager:
    def __init__(self, section_runtime_repo: ISectionRepository):
        self._section_runtime_repo = section_runtime_repo

    def new_section(self, name : str) -> SECTION_RESULT:

        result : SECTION_RESULT = SECTION_RESULT.DEFAULT
        section_id = self._generate_unique_section_id(name)

        self._section_runtime_repo.add_section(section_id, name)

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
        # This is a simple example of generating a unique section ID based on the name.
        # In a real application, you might want to use a more robust method (e.g., UUID).
        return f"section_{hash(name) % 1000000}"