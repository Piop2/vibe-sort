import json

from google import genai
from google.genai import types

from vibe_sort.client import VibeSortClient, ModelCode
from vibe_sort.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class GeminiModelCode(ModelCode):
    GEMINI_3_FLASH_LITE = "gemini-3.1-flash-lite-preview"


class GeminiSortClient(VibeSortClient):
    def __init__(self, api_key: str, model_code: GeminiModelCode) -> None:
        super().__init__(api_key, model_code)

        self.__client = genai.Client(api_key=self._api_key)
        return

    def sort(self, array: list[int], reverse: bool = False) -> list[int]:
        response = self.__client.models.generate_content(
            model=self._model_code.value,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=USER_PROMPT_TEMPLATE.format(array),
        )

        if response.text is None:
            raise RuntimeError

        sorted_list = json.loads(response.text)["sorted"]
        if reverse:
            return sorted_list[::-1]
        return sorted_list
