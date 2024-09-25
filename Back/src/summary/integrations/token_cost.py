import os
from typing import List

import tiktoken
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.environ['MODEL_NAME']
COST_TOKEN_RATIO = 0.08

_encoding_name = tiktoken.encoding_name_for_model(MODEL_NAME)
_encoding = tiktoken.get_encoding(_encoding_name)

def estimate_token_cost(*summary_contents: str) -> int:
    """
    Estimate the cost of a token in terms of the number of requests it can make.
    """
    total_token_count = sum(len(_encoding.encode(content)) for content in summary_contents if content)
    token_cost = int(total_token_count * COST_TOKEN_RATIO)
    return token_cost
