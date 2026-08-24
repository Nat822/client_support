"""Explicit local/CI NeuralDeep evaluation entry point."""

import json
import os
from pathlib import Path

from client_support.evaluation.order_tracking import OrderTrackingCase
from client_support.evaluation.real_provider import evaluate_real_provider
from client_support.providers.neuraldeep import NeuralDeepSGRProvider


def load_cases(path: Path) -> list[OrderTrackingCase]:
    with path.open(encoding="utf-8") as handle:
        return [OrderTrackingCase(**json.loads(line)) for line in handle if line.strip()]


def main() -> None:
    api_key = os.environ.get("NEURALDEEP_API_KEY")
    if not api_key:
        raise SystemExit("NEURALDEEP_API_KEY is required")

    model = os.environ.get("NEURALDEEP_MODEL", "qwen3.6-35b-a3b")
    dataset = os.environ.get("NEURALDEEP_DATASET", "evaluation/order_tracking.jsonl")
    provider = NeuralDeepSGRProvider(api_key=api_key, model=model)
    result = evaluate_real_provider(provider, load_cases(Path(dataset)))

    print(json.dumps({
        "model": model,
        "dataset": dataset,
        "total": result.total,
        "category_accuracy": result.category_accuracy,
        "extraction_accuracy": result.extraction_accuracy,
        "error_rate": result.error_rate,
        "average_latency_seconds": result.average_latency_seconds,
    }, indent=2))


if __name__ == "__main__":
    main()
