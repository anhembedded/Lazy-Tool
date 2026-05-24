from abc import ABC, abstractmethod
from ....Entity.Section.Section import Section, SectionBuilder
from ....UseCases.Config.Port.ConfigHandler import IConfigHandler

class SectionRepository():
    def __init__(self):
        self.sections_runtime_store : dict[str, Section] = {}

    def add_section(self, section: Section) -> None:
        self._push_to_runtime_store(section.id(), section)

    def remove_section(self, section_id: str) -> None:
        self._remove_from_runtime_store(section_id)

    def find_by_id(self, section_id: str) -> Section | None:
        return self.sections_runtime_store.get(section_id, None)


    def _push_to_runtime_store(self, section_id: str, section_obj: Section) -> None:
        self.sections_runtime_store[section_id] = section_obj

    def _remove_from_runtime_store(self, section_id: str) -> None:
        if section_id in self.sections_runtime_store:
            del self.sections_runtime_store[section_id]
