"""Explicit, local-only NeuralDeep evaluation entry point.

This script requires NEURALDEEP_API_KEY and is intentionally not part of CI.
"""

import json
import os

from client_support.evaluation.order_tracking import OrderTrackingCase
from client_support.evaluation.real_provider import evaluate_real_provider
from client_support.providers.neuraldeep import NeuralDeepSGRProvider


def main() -> None:
    api_key = os.environ.get("NEURALDEEP_API_KEY")
    if not api_key:
        raise SystemExit("NEURALDEEP_API_KEY is required")

    model = os.environ.get("NEURALDEEP_MODEL", "qwen3.6-35b-a3b")
    provider = NeuralDeepSGRProvider(api_key=api_key, model=model)

    with open("evaluation/order_tracking.jsonl", encoding="utf-8") as handle:
        cases = [OrderTrackingCase(**json.loads(line)) for line in handle if line.strip()]

    result = evaluate_real_provider(provider, cases)
    print(json.dumps({
        "model": model,
        "total": result.total,
        "category_accuracy": result.category_accuracy,
        "extraction_accuracy": result.extraction_accuracy,
        "error_rate": result.error_rate,
        "average_latency_seconds": result.average_latency_seconds,
    }, indent=2))


if __name__ == "__main__":
    main()
