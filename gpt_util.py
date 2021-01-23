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

def dict_logprobs_to_probs(prob_dict):
    return {key: math.exp(prob_dict[key]) for key in prob_dict.keys()}


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

def query_yes_no(prompt, engine="ada", attempts=3, delay=1, max_tokens=1):
    if attempts < 1:
        raise TimeoutError
    try:

        mask = {'yes': 100,
                'no': 100,
                'YES': 100,
                'NO': 100,
                'Yes': 100,
                'No': 100,}


        result =  openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=0.0,
            logprobs=10,
            max_tokens=max_tokens,
            echo=True,
            top_p=1,
            n=1,
            stop=["\n"],
            timeout=15,
            logit_bias = logit_mask(mask)

        )
        print(result)

        last_token_logprobs = result['choices'][0]['logprobs']['top_logprobs'][-1]
        print(last_token_logprobs)
        last_token_probs = dict_logprobs_to_probs(last_token_logprobs)
        print(last_token_probs)

        best_prob = 0
        result = "na"
        for key, prob in last_token_probs.items():
            if prob > best_prob:
                if key.lower().replace(" ", "") == 'yes' or key.lower().replace(" ", "") == 'no':
                    best_prob = prob
                    result = key.lower().replace(" ", "")
        return result




    except Exception as e:
        print(f"Failed to query, {attempts} attempts remaining, delay={delay}")
        print(e)
        time.sleep(delay)
        return query(prompt, engine, attempts=attempts-1, delay=delay*2)