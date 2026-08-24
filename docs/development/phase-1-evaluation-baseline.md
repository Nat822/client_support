# Phase 1 — SGR evaluation baseline

The first real NeuralDeep run validated the full path from GitHub Actions secret to the OpenAI-compatible provider and structured SGR output.

Observed baseline on the initial 4-case dataset with `qwen3.6-35b-a3b`:

- category accuracy: 100%
- extraction accuracy: 100%
- error rate: 0%
- average latency: about 10.7 seconds per case

This is a smoke/baseline result, not a production quality claim. Four examples are too small to establish reliable quality thresholds.

## Extended evaluation

The `evaluation` workflow mode now uses `evaluation/order_tracking_extended.jsonl`, containing 20 synthetic cases covering:

- Order Tracking with an order number;
- Order Tracking without an order number;
- delayed/missing shipment wording;
- Billing requests and negative examples.

The workflow uploads the JSON result as an Actions artifact so the run can be reviewed without copying logs.

## Quality gates

We intentionally do not encode arbitrary pass/fail thresholds yet. After several runs, review the dataset and establish gates based on the support risk of each field. In particular, incorrect entity extraction that could cause an unsafe tool call should be treated more strictly than a low-risk classification miss.

Next evaluation work should add per-category/per-field metrics and compare at least two models before selecting a production baseline.
