from dataclasses import dataclass
from time import perf_counter

from client_support.contracts.sgr_provider import SGRProvider
from client_support.evaluation.order_tracking import OrderTrackingCase


@dataclass(frozen=True, slots=True)
class EvaluationSample:
    category_correct: bool
    extraction_correct: bool
    latency_seconds: float
    error: str | None = None


@dataclass(frozen=True, slots=True)
class RealProviderEvaluation:
    total: int
    category_accuracy: float
    extraction_accuracy: float
    error_rate: float
    average_latency_seconds: float
    samples: list[EvaluationSample]


def evaluate_real_provider(provider: SGRProvider, cases: list[OrderTrackingCase]) -> RealProviderEvaluation:
    if not cases:
        return RealProviderEvaluation(0, 0.0, 0.0, 0.0, 0.0, [])

    samples: list[EvaluationSample] = []
    for case in cases:
        started = perf_counter()
        try:
            classification = provider.classify(text=case.text)
            extraction = provider.extract_order_tracking(text=case.text)
            samples.append(
                EvaluationSample(
                    category_correct=classification.category == case.expected_category,
                    extraction_correct=sorted(extraction.order_numbers) == sorted(case.expected_order_numbers),
                    latency_seconds=perf_counter() - started,
                )
            )
        except Exception as exc:
            samples.append(
                EvaluationSample(
                    category_correct=False,
                    extraction_correct=False,
                    latency_seconds=perf_counter() - started,
                    error=type(exc).__name__,
                )
            )

    total = len(samples)
    return RealProviderEvaluation(
        total=total,
        category_accuracy=sum(s.category_correct for s in samples) / total,
        extraction_accuracy=sum(s.extraction_correct for s in samples) / total,
        error_rate=sum(s.error is not None for s in samples) / total,
        average_latency_seconds=sum(s.latency_seconds for s in samples) / total,
        samples=samples,
    )
