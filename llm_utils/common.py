from dataclasses import dataclass, field
import tiktoken
import logging


def get_model_encoding(model: str):
    """Get the encoding for the given model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    return encoding


@dataclass
class ModelInfo:
    """Struct for model information with common attributes
    """

    name: str
    max_tokens: int
    prompt_token_cost: float
    completion_token_cost: float
    tokens_per_message: int = field(default=3)
    tokens_per_name: int = field(default=1)
    
    def encoding(self):
        return get_model_encoding(self.name)


MODELS = {
    info.name: info
    for info in [
        ModelInfo(name="text-davinci-003", max_tokens=4097, prompt_token_cost=0.02, completion_token_cost=0.02,
                  ),
        ModelInfo(name="gpt-3.5-turbo-0301", max_tokens=4096, prompt_token_cost=0.0015, tokens_per_message=4, tokens_per_name=-1
                  ),
        ModelInfo(name="gpt-3.5-turbo-0613", max_tokens=4096, prompt_token_cost=0.0015, completion_token_cost=0.002,
                  ),
        ModelInfo(
            name="gpt-3.5-turbo-16k-0613", max_tokens=16384, prompt_token_cost=0.003, completion_token_cost=0.004,
            
        ),
        ModelInfo(name="gpt-4-0314", max_tokens=8192, prompt_token_cost=0.03, completion_token_cost=0.06, 
                  ),
        ModelInfo(name="gpt-4-0613", max_tokens=8192, prompt_token_cost=0.03, completion_token_cost=0.06,
                  ),
        ModelInfo(name="gpt-4-32k-0314", max_tokens=32768, prompt_token_cost=0.06, completion_token_cost=0.12, 
                  ),
        ModelInfo(name="gpt-4-32k-0613", max_tokens=32768, prompt_token_cost=0.06, completion_token_cost=0.12, 
                  ),
        
    ]
}


chat_model_mapping = {
    "gpt-3.5-turbo": "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo-16k-0613",
    "gpt-4": "gpt-4-0613",
    "gpt-4-32k": "gpt-4-32k-0613",
}

for alias, target in chat_model_mapping.items():
    alias_info = ModelInfo(**MODELS[target].__dict__)
    alias_info.name = alias
    MODELS[alias] = alias_info
