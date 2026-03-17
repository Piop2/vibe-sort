from typing import Optional

from google import genai
from google.genai import types

from vibe_sort.client import KeyFunction, ModelCode, VibeSortClient, default_key
from vibe_sort.prompts import SYSTEM_PROMPT


class GeminiModelCode(ModelCode):
    GEMINI_3_FLASH_LITE = "gemini-3.1-flash-lite-preview"


class GeminiSortClient(VibeSortClient):
    def __init__(self, api_key: str, model_code: GeminiModelCode) -> None:
        super().__init__(api_key, model_code)

        self.__client = genai.Client(api_key=self._api_key)
        return

    def sort[T](
        self,
        array: list[T],
        /,
        key: Optional[KeyFunction] = None,
        reverse: bool = False,
    ) -> list[T]:
        if key is None:
            key = default_key
        
        response = self.__client.models.generate_content(
            model=self._model_code.value,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=self._create_prompt(array, key),
        )

        if response.text is None:
            raise RuntimeError

        sorted_list = self._parse_response(response.text, array)
        if reverse:
            return sorted_list[::-1]
        return sorted_list
