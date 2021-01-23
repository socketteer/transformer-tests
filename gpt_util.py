from transformers import GPT2Tokenizer
import math

def tokenize(input):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return tokenizer(input)['input_ids']

def logprobs_to_probs(probs):
    return [math.exp(x) for x in probs]