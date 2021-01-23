import os
import time

import openai
from transformers import GPT2Tokenizer
import math

openai.api_key = os.environ["OPENAI_API_KEY"]


def tokenize(input):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return tokenizer(input)['input_ids']


def logprobs_to_probs(probs):
    return [math.exp(x) for x in probs]


def total_logprob(response):
    logprobs = response['logprobs']['token_logprobs']
    logprobs = [i for i in logprobs if not math.isnan(i)]
    return sum(logprobs)


def query(prompt, engine="ada", attempts=3, delay=1, max_tokens=200):
    if attempts < 1:
        raise TimeoutError
    try:
        return openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=0.0,
            max_tokens=max_tokens,
            echo=False,
            top_p=1,
            n=1,
            stop=["\n"],
            timeout=15,
        )
    except Exception as e:
        print(f"Failed to query, {attempts} attempts remaining, delay={delay}")
        print(e)
        time.sleep(delay)
        return query(prompt, engine, attempts=attempts-1, delay=delay*2)

