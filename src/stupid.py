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
correction3 = """You say, \"No,"""
correct = """\"That's correct,\" you say."""

math1 = """You say \"What is 2 + 3?\"
\"It's 4,\" says John.
You say \"No, 2 + 3 is 5.\"
\"Oh,\" says John, smiling sheepishly. \"I get it.\"
You grin and nod.\n"""

math1_hopeless = """You say \"What is 2 + 3?\"
\"It's 4,\" says John.
You say \"No, 2 + 3 is 5.\"
\"Oh,\" says John, smiling sheepishly. \"I get it.\"
But you know that John doesn't get it because he is a bot who can't do arithmetic. You decide to ask anyway, knowing his answer will be no better than random.\n"""

math2 = """You say \"What is 4 + 3?\""""
math_correct_7 = """\"4 + 3 is 7,\" says John."""
math_incorrect_6 = """\"4 + 3 is 6,\" says John."""
math_incorrect_8 = """\"4 + 3 is 8,\" says John."""
math_incorrect_4 = """\"4 + 3 is 4,\" says John."""
math_incorrect_2 = """\"4 + 3 is 2,\" says John."""

print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 7\n')
evaluate(prompt=math1_hopeless + math2 + '\n', target=math_correct_7)

print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 6\n')
evaluate(prompt=math1_hopeless + math2 + '\n', target=math_incorrect_6)

print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 8\n')
evaluate(prompt=math1_hopeless + math2 + '\n', target=math_incorrect_8)

print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 4\n')
evaluate(prompt=math1_hopeless + math2 + '\n', target=math_incorrect_4)

print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 2\n')
evaluate(prompt=math1_hopeless + math2 + '\n', target=math_incorrect_2)


# print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 7 && you correct John\n')
# evaluate(prompt=math1 + math2 + '\n' + math_correct_7 + '\n', target=correction3)
#
# print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 2 && you correct John\n')
# evaluate(prompt=math1 + math2 + '\n' + math_incorrect_2 + '\n', target=correction3)
#
# print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 7 && you say correct\n')
# evaluate(prompt=math1 + math2 + '\n' + math_correct_7 + '\n', target=correct)
#
# print('#### John evaluates 2 + 3 incorrectly && you ask 4 + 3 && John says 2 && you say correct\n')
# evaluate(prompt=math1 + math2 + '\n' + math_incorrect_2 + '\n', target=correct)


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


# print('### Probability that you correct John\n')
#
# print('#### No context + unbalanced parentheses + John says unbalanced + you correct\n')
# evaluate(prompt=unbalanced_context + '\n' + unbalanced_response + '\n', target=correction2)
#
# print('#### No context + unbalanced parentheses + John says balanced\n')
# evaluate(prompt=unbalanced_context + '\n' + balanced_response + '\n', target=correction2)
#
# print('#### Original context + unbalanced parentheses + John says unbalanced\n')
# evaluate(prompt=background_context + unbalanced_context + '\n' + unbalanced_response + '\n', target=correction2)
#
# print('#### Original context + unbalanced parentheses + John says balanced\n')
# evaluate(prompt=background_context + unbalanced_context + '\n' + balanced_response + '\n', target=correction2)

# print('#### Smart John context + unbalanced parentheses + John says unbalanced + you correct John\n')
# evaluate(prompt=smart_john_context + unbalanced_context + '\n' + unbalanced_response + '\n', target=correction2)
#
# print('#### Smart John context + unbalanced parentheses + John says balanced + you correct John\n')
# evaluate(prompt=smart_john_context + unbalanced_context + '\n' + balanced_response + '\n', target=correction2)
