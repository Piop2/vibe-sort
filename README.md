# Vibe Sort

> The perfect solution for vibe coders

## Example
```python
from vibe_sort.models.gemini import GeminiSortClient, GeminiModelCode

API_KEY = "GEMINI API KEY HERE"
client = GeminiSortClient(API_KEY, GeminiModelCode.GEMINI_3_FLASH_LITE)

array = [...]

client.sort(array) # <--- sorted!!
```
