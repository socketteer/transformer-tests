from conditional import conditional_logprob


def evaluate(prompt, target):
    prompt_lines = prompt.splitlines()
    for line in prompt_lines:
        print(f'>{line}\n>')
    print(f'>**{target}**')
    logprob = conditional_logprob(prompt=prompt, target=target, engine='davinci')
    print(f'\n`logprob: {logprob}`\n')


background_context = """You say \"Is ' ( ) ( ) ( ) ' balanced or unbalanced?\"
\"Unbalanced,\" says John.
You say \"No, ' ( ) ( ) ( ) ' is balanced\"
\"Oh,\" says John, smiling sheepishly. \"I get it.\"
You grin and nod.\n"""
explanation_context = """You say, \"Balanced parentheses means that each opening symbol has a corresponding closing symbol and the pairs of parentheses are properly nested.\"
\"Okay,\" says John.\n"""
smart_john_context = """You say, \"John, I have a question, and I know you're the expert on this kind of thing. What does it mean if parentheses is balanced?\"
John says, "Balanced parentheses means that each opening symbol has a corresponding closing symbol and the pairs of parentheses are properly nested.\"\n"""
balanced_context = """You say \"Is ' ( ) ( ) ( ) ' balanced or unbalanced?\""""
unbalanced_context = """You say "Is ' ( ) ( ) ) ' balanced or unbalanced?\""""
balanced_response = """\"It's balanced,\" says John."""
unbalanced_response = """\"It's unbalanced,\" says John."""
#correction = """\"No, it isn't,\" you say."""
correction2 = """\"No,\" you say"""
correct = """\"That's correct,\" you say."""

true_context = """You say \"Is the equation 2 + 3 = 4 + 1 true or false?\""""
false_context = """You say "Is the equation 2 + 3 = 4 + 3 true or false?\""""
true_response = """\"It's true,\" says John."""
false_response = """\"It's false,\" says John."""

# print('### Probability that John thinks the parentheses are balanced\n')
#
# print('#### No context + unbalanced parentheses\n')
# evaluate(prompt=unbalanced_context + '\n', target=balanced_response)
#
# print('#### No context + balanced parentheses\n')
# evaluate(prompt=balanced_context + '\n', target=balanced_response)
#
# print('#### Original context + unbalanced parentheses\n')
# evaluate(prompt=background_context + unbalanced_context + '\n', target=balanced_response)
#
# print('#### Original context + balanced parentheses\n')
# evaluate(prompt=background_context + balanced_context + '\n', target=balanced_response)
#
# print('#### Explanation + unbalanced parentheses\n')
# evaluate(prompt=explanation_context + unbalanced_context + '\n', target=balanced_response)
#
# print('#### Explanation + balanced parentheses\n')
# evaluate(prompt=explanation_context + balanced_context + '\n', target=balanced_response)
#
# print('#### Smart John context + unbalanced parentheses\n')
# evaluate(prompt=smart_john_context + unbalanced_context + '\n', target=balanced_response)
#
# print('#### Smart John context + balanced parentheses\n')
# evaluate(prompt=smart_john_context + balanced_context + '\n', target=balanced_response)
#
#
# print('### Probability that John thinks the parentheses are unbalanced\n')
#
# print('#### No context + unbalanced parentheses\n')
# evaluate(prompt=unbalanced_context + '\n', target=unbalanced_response)
#
# print('#### No context + balanced parentheses\n')
# evaluate(prompt=balanced_context + '\n', target=unbalanced_response)
#
# print('#### Original context + unbalanced parentheses\n')
# evaluate(prompt=background_context + unbalanced_context + '\n', target=unbalanced_response)
#
# print('#### Original context + balanced parentheses\n')
# evaluate(prompt=background_context + balanced_context + '\n', target=unbalanced_response)
#
# print('#### Explanation + unbalanced parentheses\n')
# evaluate(prompt=explanation_context + unbalanced_context + '\n', target=unbalanced_response)
#
# print('#### Explanation + balanced parentheses\n')
# evaluate(prompt=explanation_context + balanced_context + '\n', target=unbalanced_response)
#
# print('#### Smart John context + unbalanced parentheses\n')
# evaluate(prompt=smart_john_context + unbalanced_context + '\n', target=unbalanced_response)
#
# print('#### Smart John context + balanced parentheses\n')
# evaluate(prompt=smart_john_context + balanced_context + '\n', target=unbalanced_response)


print('### Probability that you correct John\n')

print('#### No context + unbalanced parentheses + John says unbalanced\n')
evaluate(prompt=unbalanced_context + '\n' + unbalanced_response + '\n', target=correction2)

print('#### No context + unbalanced parentheses + John says balanced\n')
evaluate(prompt=unbalanced_context + '\n' + balanced_response + '\n', target=correction2)

print('#### Original context + unbalanced parentheses + John says unbalanced\n')
evaluate(prompt=background_context + unbalanced_context + '\n' + unbalanced_response + '\n', target=correction2)

print('#### Original context + unbalanced parentheses + John says balanced\n')
evaluate(prompt=background_context + unbalanced_context + '\n' + balanced_response + '\n', target=correction2)
