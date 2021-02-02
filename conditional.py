import os
import openai
import numpy as np
from gpt_util import logprobs_to_probs, normalize

openai.api_key = os.environ["OPENAI_API_KEY"]


# returns the conditional probability of filter coming after prompt
def filter_logprob(prompt, filter, engine='ada'):
    combined = prompt + filter
    response = openai.Completion.create(
        engine=engine,
        prompt=combined,
        temperature=0,
        max_tokens=0,
        echo=True,
        top_p=1,
        n=1,
        logprobs=0
    )

    positions = response.choices[0]["logprobs"]["text_offset"]
    logprobs = response.choices[0]["logprobs"]["token_logprobs"]
    # tokens = response.choices[0]["logprobs"]["tokens"]

    word_index = positions.index(len(prompt))

    total_conditional_logprob = sum(logprobs[word_index:])

    return total_conditional_logprob


# TODO use threading
# returns the conditional probabilities for each event happening after prompt
def event_probs(prompt, events, engine='ada'):
    probs = []
    for event in events:
        logprob = filter_logprob(prompt, event, engine)
        probs.append(logprobs_to_probs(logprob))

    normal_probs = normalize(probs)
    return probs, normal_probs


# like event_probs, returns conditional probabilities (normalized & unnormalized) for each token occurring after prompt
def token_probs(prompt, tokens, engine='ada'):
    pass


# returns a list of positions and counterfactual probability of token at position
# if token is not in top_logprobs, probability is treated as 0
# all positions if actual_token=None, else only positions where the actual token in response is actual_token
# TODO next sequence instead of next token
def counterfactual(response, token, actual_token=None, next_token=None, sort=True):
    counterfactual_probs = []
    tokens = response.choices[0]['logprobs']['tokens']
    top_logprobs = response.choices[0]['logprobs']['top_logprobs']
    positions = response.choices[0]['logprobs']['text_offset']
    for i, probs in enumerate(top_logprobs):
        if (actual_token is None and next_token is None) \
                or actual_token == tokens[i] \
                or (i < len(tokens) - 1 and next_token == tokens[i+1]):
            if token in probs:
                counterfactual_probs.append({'position': positions[i+1],
                                             'prob': logprobs_to_probs(probs[token])})
            else:
                counterfactual_probs.append({'position': positions[i+1], 'prob': 0})
    if sort:
        counterfactual_probs = sorted(counterfactual_probs, key=lambda k: k['prob'])
    return counterfactual_probs


def substring_probs(preprompt, content, filter, quiet=0):
    index = 0
    logprobs = []
    substrings = []
    for word in content.split():
        index += len(word) + 1
        substring = content[:(index - 1)]
        prompt = preprompt + substring
        logprob = filter_logprob(prompt, filter)
        logprobs.append(logprob)
        substrings.append(substring)
        if not quiet:
            print(substring)
            print('logprob: ', logprob)

    return substrings, logprobs


def n_top_logprobs(preprompt, content, filter, n=5, quiet=0):
    substrings, logprobs = substring_probs(preprompt, content, filter, quiet)
    sorted_logprobs = np.argsort(logprobs)
    top = []
    for i in range(n):
        top.append({'substring': substrings[sorted_logprobs[-(i + 1)]],
                    'logprob': logprobs[sorted_logprobs[-(i + 1)]]})

    return top


def main():
    f = open("preprompt.txt", "r")
    preprompt = f.read()[:-1]
    g = open("content.txt", "r")
    content = g.read()[:-1]
    h = open("filter.txt", "r")
    filter = h.read()[:-1]

    print('preprompt\n', preprompt)
    print('\ncontent\n', content)
    print('\nfilter\n', filter)

    top = n_top_logprobs(preprompt, content, filter, 10)
    print(top)

    for t in top:
        print('\ncutoff: ', t['substring'][-100:])
        print('logprob: ', t['logprob'])


if __name__ == "__main__":
    main()


