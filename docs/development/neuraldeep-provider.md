# NeuralDeep provider for Phase 1 testing

NeuralDeep exposes an OpenAI-compatible API. Its documented base URL is `https://api.neuraldeep.ru/v1`, and the official quickstart uses the OpenAI Python SDK with only `base_url` and `api_key` changed. urlNeuralDeep API documentationhttps://neuraldeep.ru/docs

## Configuration

The adapter defaults to:

- base URL: `https://api.neuraldeep.ru/v1`
- model: `qwen3.6-35b-a3b`

Both are constructor parameters so another OpenAI-compatible endpoint can be used without changing application code.

For local/manual testing, keep the API key outside the repository, for example in `NEURALDEEP_API_KEY`. Never commit the key.

## Model choice

The initial recommended model is `qwen3.6-35b-a3b`. NeuralDeep lists it as a 256k-context model with tools, reasoning and vision, and indicates that qwen models run on its own infrastructure. This is a good first candidate for customer-support classification/extraction because it is large enough for schema-following and Russian/English support while remaining more practical for repeated evaluation than the largest frontier options. citeturn0search1turn0search6

`gpt-oss-120b` is the first comparison model I would benchmark next: NeuralDeep lists it with tools and reasoning, but notes that it is handled by an external vendor rather than its own GPU infrastructure. citeturn0search6

We should choose the production model from measured evaluation results, not from model branding or a generic benchmark. The first gate is exact category accuracy and exact order-number extraction accuracy on the reviewed dataset, followed by latency and cost/throughput.
