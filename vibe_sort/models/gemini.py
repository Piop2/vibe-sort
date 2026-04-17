from typing import cast

from google import genai
from google.genai import types

from vibe_sort.client import KeyFunction, Model, VibeSortClient, default_key, key_wrapper
from vibe_sort.prompts import SYSTEM_PROMPT


class GeminiModel(Model):
    FLASH_LITE = "gemini-3.1-flash-lite-preview"


GEMINI_FLASH_LITE = GeminiModel.FLASH_LITE


class GeminiSortClient(VibeSortClient):
    def __init__(self, api_key: str, model_code: GeminiModel) -> None:
        super().__init__(api_key, model_code)

        self.__client = genai.Client(api_key=self._api_key)
        return

    def sort[T](
            self,
            array: list[T],
            /,
            key: KeyFunction = default_key,
            reverse: bool = False,
    ) -> list[T]:
        response = self.__client.models.generate_content(
            model=self._model_code.value,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=self._create_prompt(array, key_wrapper(key)),
        )

        if response.text is None:
            raise RuntimeError

        sorted_list = self._parse_response(cast(str, response.text), array)
        if reverse:
            return sorted_list[::-1]
        return sorted_list
