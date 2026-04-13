# Vibe Sort

> The perfect solution for vibe coders

## Example

```python
from vibe_sort.models.gemini import GeminiSortClient, GEMINI_FLASH_LITE

API_KEY = "GEMINI API KEY HERE"
client = GeminiSortClient(API_KEY, GEMINI_FLASH_LITE)

array = [...]

client.sort(array)  # <--- sorted!!
```
