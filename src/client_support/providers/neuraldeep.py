import json
from typing import Any

from openai import OpenAI

from client_support.contracts.sgr_provider import SGRClassification, SGRExtraction


class NeuralDeepSGRProvider:
    """OpenAI-compatible SGR provider; only the client/base URL are provider-specific."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "qwen3.6-35b-a3b",
        base_url: str = "https://api.neuraldeep.ru/v1",
        client: OpenAI | None = None,
    ) -> None:
        self.model = model
        self.client = client or OpenAI(api_key=api_key, base_url=base_url)

    def _json_completion(self, *, system: str, text: str) -> dict[str, Any]:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": text},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("SGR provider returned an empty response")
        value = json.loads(content)
        if not isinstance(value, dict):
            raise ValueError("SGR provider returned a non-object JSON response")
        return value

    def classify(self, *, text: str) -> SGRClassification:
        value = self._json_completion(
            system=(
                "Classify a customer support ticket. Return JSON only with keys "
                '"category" and "confidence". Supported categories: order_tracking, billing. '
                "Use order_tracking only when the customer asks about an order or shipment."
            ),
            text=text,
        )
        category = value.get("category")
        confidence = value.get("confidence")
        if not isinstance(category, str) or not isinstance(confidence, (int, float)):
            raise ValueError("Invalid SGR classification response")
        return SGRClassification(category=category, confidence=float(confidence))

    def extract_order_tracking(self, *, text: str) -> SGRExtraction:
        value = self._json_completion(
            system=(
                "Extract order numbers from a customer support ticket. Return JSON only with keys "
                '"order_numbers" and "confidence". order_numbers must be an array of strings. '
                "If no order number is present, return an empty array."
            ),
            text=text,
        )
        order_numbers = value.get("order_numbers")
        confidence = value.get("confidence")
        if not isinstance(order_numbers, list) or not all(isinstance(item, str) for item in order_numbers):
            raise ValueError("Invalid SGR extraction response")
        if not isinstance(confidence, (int, float)):
            raise ValueError("Invalid SGR extraction confidence")
        return SGRExtraction(order_numbers=order_numbers, confidence=float(confidence))
