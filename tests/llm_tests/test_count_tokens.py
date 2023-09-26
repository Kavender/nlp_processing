import pytest
from llm_utils.count_tokens import get_input_tokens, num_tokens_from_messages, get_tokens_params_for_model


@pytest.mark.parametrize(
    "messages, model, expected_tokens",
    [
        ([{"name": "user", "content": "hello"}], "gpt-3.5-turbo", 5),
        ([{"name": "user", "content": "hello world"}], "gpt-4", 11),
        ([{"name": "system", "content": "hello"}, {"name": "assistant", "content": "hi"}], "gpt-3.5-turbo-0613", 7),
        ([], "gpt-3.5-turbo-0613", 0),
    ],
)
def test_get_input_tokens(messages, model, expected_tokens):
    assert get_input_tokens(messages, model) == expected_tokens


@pytest.mark.parametrize(
    "messages, model, expected_tokens",
    [
        ([{"name": "user", "content": "hello"}], "gpt-3.5", 20),
        ([{"name": "user", "content": "hello world"}], "gpt-4", 33),
        (
            [{"name": "system", "content": "hello, I'm your chatbot"}, {"name": "assistant", "content": "hi"}],
            "gpt-3.5-turbo-0613",
            37,
        ),
        ([], "gpt-3.5-turbo-0613", 3),
    ],
)
def test_num_tokens_from_messages(messages, model, expected_tokens):
    assert num_tokens_from_messages(messages, model) == expected_tokens


@pytest.mark.parametrize(
    "model, expected_output",
    [("gpt-3.5-turbo", (10, 2)), ("gpt-3.5-turbo-0613", (10, 2)), ("gpt-4", (15, 3)), ("gpt-4-0613", (15, 3)),],
)
def test_get_tokens_params_for_model(model, expected_output):
    assert get_tokens_params_for_model(model) == expected_output


# Testing for invalid model
def test_get_tokens_params_for_model_invalid():
    with pytest.raises(ValueError):
        get_tokens_params_for_model("unknown-model")
