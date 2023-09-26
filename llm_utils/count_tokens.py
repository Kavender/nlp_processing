from typing import List, Dict
from llm_utils.common import get_model_encoding
from llm_utils.common import MODELS


def get_input_tokens(messages, model):
    encoding = get_model_encoding(model)
    return sum(len(encoding.encode(m["content"])) for m in messages)


def num_tokens_from_messages(messages: List[Dict[str, str]], model="gpt-3.5-turbo-0613"):
    """
    Count the number of tokens used in chat messages for a given model.

    Args:
    - messages (List[Dict[str, str]]): The chat messages to count.
    - model (str): The model name, e.g., "gpt-3.5-turbo".

    Returns:
    - int: Number of tokens used in messages.
    """
    encoding = get_model_encoding(model)
    tokens_per_message, tokens_per_name = get_tokens_params_for_model(model)

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3  # every reply is primed with assistant
    return num_tokens


def get_tokens_params_for_model(model: str):
    """Get tokens per message and tokens per name for model."""

    if model not in MODELS:
        raise ValueError(f"Unknown model: {model}")

    if "gpt-3.5-turbo" in model:
        model = "gpt-3.5-turbo-0613"

    if "gpt-4" in model:
        model = "gpt-4-0613"

    tokens_per_message = MODELS[model].tokens_per_message
    tokens_per_name = MODELS[model].tokens_per_name
    return tokens_per_message, tokens_per_name
