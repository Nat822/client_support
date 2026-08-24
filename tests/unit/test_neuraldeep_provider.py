from unittest.mock import Mock

from client_support.providers.neuraldeep import NeuralDeepSGRProvider


def make_client(content: str) -> Mock:
    client = Mock()
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = content
    client.chat.completions.create.return_value = response
    return client


def test_neuraldeep_provider_classifies_json_response() -> None:
    provider = NeuralDeepSGRProvider(
        api_key="test-key",
        client=make_client('{"category":"order_tracking","confidence":0.97}'),
    )
    result = provider.classify(text="Where is ORD-001?")
    assert result.category == "order_tracking"
    assert result.confidence == 0.97


def test_neuraldeep_provider_extracts_order_numbers() -> None:
    provider = NeuralDeepSGRProvider(
        api_key="test-key",
        client=make_client('{"order_numbers":["ORD-001"],"confidence":0.99}'),
    )
    result = provider.extract_order_tracking(text="Track ORD-001")
    assert result.order_numbers == ["ORD-001"]
    assert result.confidence == 0.99
