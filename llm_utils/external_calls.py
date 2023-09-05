import openai
from openai.common import MODELS
from openai.count_tokens import num_tokens_from_messages
from tenacity import retry, stop_after_attemp, wait_random_expential


@retry(wait=wait_random_expential(min=1, max=10), stop=stop_after_attemp(3))
def get_completion_with_backoff(**kwargs):
    assert 'model' in kwargs, "'model' parameter is required!"
    assert 'messages' in kwargs, "'messages' parameter is required!"
    if 'max_token' in kwargs:
        kwargs['max_token'] = get_max_tokens(**kwargs)
    return openai.ChatCompletion.create(**kwargs)


def prepare_basic_prompt(prompt, role):
    assert role in {"system", "user", "assistant"}
    return [{"role": role, "content": prompt}]


def prepare_messages(base_prompt, base_role, user_prompt):
    messages = prepare_basic_prompt(base_prompt, base_role)
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    return messages


def get_max_tokens(max_token, messages=None, prompt: str = "", model="gpt-3.5-turbo-0613"):
    if len(messages) == 0:
        messages = prepare_basic_prompt(prompt, "user")

    input_tokens = num_tokens_from_messages(messages)
    max_output_tokens = MODELS[model].max_tokens - input_tokens
    max_allowed = min(max_token, max_output_tokens)
    if max_allowed < 1:
        raise ValueError(f"Token overflow: not enough token left!")
    return min(max_token, max_output_tokens)


# to generalize, send a message builder
def generate_and_store_response(base_prompt, user_prompt, **kwargs):
    messages = prepare_messages(base_prompt, user_prompt, **kwargs)
    response = get_completion_with_backoff(messages=messages, **kwargs)

    response_text = response.choices[0].message["content"]
    token_usage = response.usage.todict()
    return {"generation": response_text, "token_usage": token_usage,
            "model_dict": {"provider": "Openai", "engine": response.model,
                           "model": response.object}}
