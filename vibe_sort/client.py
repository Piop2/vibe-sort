import json
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Callable

from vibe_sort.prompts import USER_PROMPT_TEMPLATE

KeyFunction = Callable[[Any], int | float | str]
WrappedKeyFunction = Callable[[Any], int | float]


def default_key(x: Any) -> int | float | str:
    if x is None:
        raise TypeError

    return x


def key_wrapper(f: KeyFunction) -> WrappedKeyFunction:
    def key(x: Any) -> int | float:
        match f(x):
            case int() | float():
                return x
            case str():
                # what if x len is more than 2 ...?
                return ord(x)
            case _:
                raise TypeError

    return key


class Model(StrEnum): ...


class VibeSortClient(ABC):
    def __init__(self, api_key: str, model_code: Model) -> None:
        self._api_key = api_key
        self._model_code = model_code
        return

    @staticmethod
    def _create_prompt[T](array: list[T], key: WrappedKeyFunction) -> str:
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

    @staticmethod
    def _parse_response[T](response: str, array: list[T]) -> list[T]:
        return [array[element["index"]] for element in json.loads(response)["sorted"]]

    @abstractmethod
    def sort(
            self,
            array: list[int],
            /,
            key: KeyFunction = default_key,
            reverse: bool = False,
    ) -> list[int]: ...
