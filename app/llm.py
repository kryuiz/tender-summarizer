import json

import httpx
from pydantic import ValidationError

from app.schemas import TenderSummary


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2"


async def summarize_text(text: str) -> TenderSummary:
    text = text[:20000]

    prompt = f"""
Ты анализируешь тендерную документацию.

Извлеки из документа:
- сумму контракта;
- срок выполнения;
- ключевые требования к исполнителю;
- штрафы и неустойки.

Если информация отсутствует:
- для contract_amount и deadline используй "Не указано";
- для requirements и penalties используй пустой массив.

Отвечай только данными из документа. Не выдумывай информацию.

Документ:

{text}
"""

    schema = TenderSummary.model_json_schema()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": schema,
            },
            timeout=120,
        )

    response.raise_for_status()

    data = json.loads(response.json()["response"])

    try:
        return TenderSummary.model_validate(data)
    except ValidationError as e:
        raise ValueError("LLM returned invalid response") from e
