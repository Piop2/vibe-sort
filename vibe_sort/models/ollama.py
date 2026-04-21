from typing import Optional, cast

import ollama

from vibe_sort.client import (
    KeyFunction,
    VibeSortClient,
    default_key,
    key_wrapper,
)
from vibe_sort.prompts import SYSTEM_PROMPT


class OllamaSortClient(VibeSortClient):
    def __init__(
        self, model_code: str, api_key: Optional[str] = None, host: Optional[str] = None
    ) -> None:
        super().__init__(model_code, api_key)

        self.__client = ollama.Client(host=host)
        return

    def sort[T](
        self,
        array: list[T],
        /,
        key: KeyFunction = default_key,
        reverse: bool = False,
    ) -> list[T]:
        response = self.__client.chat(
            model=self._model_code,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": self._create_prompt(array, key_wrapper(key)),
                },
            ],
        )

        if response.message.content is None:
            raise RuntimeError

        sorted_list = self._parse_response(response.message.content, array)
        if reverse:
            return sorted_list[::-1]
        return sorted_list
