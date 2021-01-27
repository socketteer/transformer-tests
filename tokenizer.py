from transformers import GPT2Tokenizer


def tokenize(input):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return tokenizer(input)['input_ids']


def logit_mask(mask):
    id_mask = {}
    for token in mask:
        token_id = tokenize([token])[0][0]
        id_mask[token_id] = mask[token]
    return id_mask