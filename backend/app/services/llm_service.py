from __future__ import annotations

from openai import AzureOpenAI

from app.config import settings


class AzureLLMService:
    def __init__(self) -> None:
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )

    def explain(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or "No response returned."
