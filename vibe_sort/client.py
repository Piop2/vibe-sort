import json
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Callable, Optional

from vibe_sort.prompts import USER_PROMPT_TEMPLATE

KeyFunction = Callable[[Any], int]


def default_key(x: Any) -> int:
    match x:
        case int():
            return x
        case str():
            return ord(x)
        case _:
            raise TypeError


class ModelCode(StrEnum): ...


class VibeSortClient(ABC):
    def __init__(self, api_key: str, model_code: ModelCode) -> None:
        self._api_key = api_key
        self._model_code = model_code
        return

    def _create_prompt[T](self, array: list[T], key: KeyFunction) -> str:
        return USER_PROMPT_TEMPLATE.format(
            json.dumps(
                {
                    "array": [
                        {"index": index, "value": key(value)}
                        for index, value in enumerate(array)
                    ]
                }
            )
        )

    def _parse_response[T](self, response: str, array: list[T]) -> list[T]:
        return [array[element["index"]] for element in json.loads(response)["sorted"]]

    @abstractmethod
    def sort(
        self,
        array: list[int],
        /,
        key: Optional[KeyFunction] = None,
        reverse: bool = False,
    ) -> list[int]: ...
