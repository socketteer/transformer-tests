from tokenizer import tokenize


def char_tokenization(input):
    tokens = []
    for char in input:
        if char == ' ':
            # replaces spaces with underscores
            token = 62
        else:
            token = tokenize([char])[0][0]
        tokens.append(token)
    return tokens


def char_tokenization_2(input):
    tokens = []
    for i in range(len(input)):
        if input[i] == ' ':
            # uses token with prepended space
            token = tokenize([input[i] + input[i+1]])[0][0]
            i += 1
        else:
            token = tokenize([input[i]])[0][0]
        tokens.append(token)
    return tokens