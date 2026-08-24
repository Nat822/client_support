# Phase 1.5 — Real provider evaluation

This phase adds an explicit evaluation entry point for the NeuralDeep OpenAI-compatible provider.

## Running it

Set `NEURALDEEP_API_KEY` locally and optionally `NEURALDEEP_MODEL`. The default model is `qwen3.6-35b-a3b`.

Run:

```bash
python scripts/evaluate_neuraldeep.py
```

The script prints category accuracy, exact extraction accuracy, error rate, and average latency. It is deliberately excluded from CI because external API calls require secrets and introduce network/provider nondeterminism.

## Quality gates

Do not hard-code production thresholds from the tiny synthetic dataset. Treat this run as a baseline. Before autonomous execution, expand the dataset and establish reviewed thresholds for:

- category accuracy;
- exact extraction accuracy;
- malformed/failed request rate;
- latency;
- cost/throughput.

A model failing an evaluation gate must not be allowed to compensate by bypassing deterministic PolicyEngine or ToolRuntime controls.
