from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class SGRClassification:
    category: str
    confidence: float


@dataclass(frozen=True, slots=True)
class SGRExtraction:
    order_numbers: list[str]
    confidence: float


class SGRProvider(Protocol):
    def classify(self, *, text: str) -> SGRClassification: ...

    def extract_order_tracking(self, *, text: str) -> SGRExtraction: ...
