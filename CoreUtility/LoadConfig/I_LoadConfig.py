from typing import  Any, Protocol

class I_ConfigHandle(Protocol):
    def Load(self, file_path: str, list_key: list[str]) -> dict[str, Any]:
        ...

    def LoadAll(self, file_path: str) -> dict[str, Any]:
        ...

    def Save(self, file_path: str, data: dict[str, Any]) -> None:
        ...

    def Delete(self, file_path: str) -> None:
        ...


