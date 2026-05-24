from abc import ABC, abstractmethod
from ....Entity.Section.Section import Section


class ISectionRepository(ABC):
    def __init__(self, *args, **kwargs):
        ...
    @abstractmethod
    def add_section(self, section_id: str , section_name: str) -> None: pass
    @abstractmethod
    def remove_section(self, section_id: str) -> None: pass
    @abstractmethod
    def find_by_id(self, section_id: str) -> Section | None:
        """Return Section if found, None if not found."""
        ...
    @abstractmethod
    def save_runtime_to_database(self) -> None: pass
    @abstractmethod
    def load_runtime_from_database(self) -> Section | None: pass

