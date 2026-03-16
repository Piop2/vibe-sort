from abc import ABC, abstractmethod
from enum import StrEnum


class ModelCode(StrEnum): ...


class VibeSortClient(ABC):
    def __init__(self, api_key: str, model_code: ModelCode) -> None:
        self._api_key = api_key
        self._model_code = model_code
        return

    @abstractmethod
    def sort(self, array: list[int], reverse: bool = False) -> list[int]: ...
