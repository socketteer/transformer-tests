import math


def total_logprob(response):
    logprobs = response['logprobs']['token_logprobs']
    logprobs = [i for i in logprobs if not math.isnan(i)]
    return sum(logprobs)


