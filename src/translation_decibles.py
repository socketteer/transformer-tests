from conditional import decibels, conditional_logprob


def control(source):
    prompt = f'''{source}
'''
    return prompt


def zero_shot_openAI(source):
    prompt = f'''Translate French to English
{source}\t=\t'''
    return prompt


def zero_shot_colon(source):
    prompt = f'''Translate French to English
French:\t{source}
English:\t'''
    return prompt


def zero_shot_master_translator(source):
    pass


def few_shot_openAI(source, n=1):
    prompt = f'''Translate French to English
'''
    fr_file = open('data/wmt14-fr-en.src', 'r')
    en_file = open('data/wmt14-fr-en.ref', 'r')
    fr = fr_file.readlines()
    en = en_file.readlines()
    fr_file.close()
    en_file.close()
    for shot in range(n):
        prompt += f'''{fr[shot + 1]}\t=\t{en[shot + 1]}
'''
    prompt += f'''{source}\t=\t'''
    return prompt


def few_shot_colon(source, n=1):
    prompt = f'''Translate French to English
'''
    fr_file = open('data/wmt14-fr-en.src', 'r')
    en_file = open('data/wmt14-fr-en.ref', 'r')
    fr = fr_file.readlines()
    en = en_file.readlines()
    fr_file.close()
    en_file.close()
    for shot in range(n):
        prompt += f'''French:\t{fr[shot + 1]}English:\t{en[shot + 1]}
'''
    prompt += f'''French:\t{source}
English:\t'''
    return prompt


french_sentence = "Un homme de Cambridge a revendiqué la responsabilité de cet acte sur son compte Twitter, où il a posté des images d'Adolf Hitler."
english_target = "A man from Cambridge claimed responsibility for the act on his Twitter account, where he posted pictures of Adolf Hitler."


control_prompt = control(french_sentence)
empty_control_prompt = "\n"
# zero_shot_colon_prompt = zero_shot_colon(french_sentence)
# one_shot_colon_prompt = few_shot_colon(french_sentence, 1)
# two_shot_colon_prompt = few_shot_colon(french_sentence, 2)
# five_shot_colon_prompt = few_shot_colon(french_sentence, 5)
# ten_shot_colon_prompt = few_shot_colon(french_sentence, 10)
# twenty_shot_colon_prompt = few_shot_colon(french_sentence, 20)

zero_shot_colon_prompt = zero_shot_openAI(french_sentence)
one_shot_colon_prompt = few_shot_openAI(french_sentence, 1)
two_shot_colon_prompt = few_shot_openAI(french_sentence, 2)
five_shot_colon_prompt = few_shot_openAI(french_sentence, 5)
ten_shot_colon_prompt = few_shot_openAI(french_sentence, 10)
twenty_shot_colon_prompt = few_shot_openAI(french_sentence, 20)

# print('CONTROL PROMPT')
# print(control_prompt)
# print('\n0-SHOT PROMPT')
# print(zero_shot_colon_prompt)
# print('\n1-SHOT PROMPT')
# print(one_shot_colon_prompt)
# print('\n2-SHOT PROMPT')
# print(two_shot_colon_prompt)
# print('\n5-SHOT PROMPT')
# print(five_shot_colon_prompt)
# print('\n10-SHOT PROMPT')
# print(ten_shot_colon_prompt)
# print('\n20-SHOT PROMPT')
# print(twenty_shot_colon_prompt)


def calculate_decibels(engine='ada'):
    zero_shot_dB, control_logprob, zero_shot_logprob = decibels(prior=control_prompt, evidence=zero_shot_colon_prompt,
                                                                target=english_target, engine=engine)
    one_shot_dB, _, one_shot_logprob = decibels(prior=control_prompt, evidence=one_shot_colon_prompt,
                                                target=english_target, engine=engine)
    two_shot_dB, _, two_shot_logprob = decibels(prior=control_prompt, evidence=two_shot_colon_prompt,
                                                target=english_target, engine=engine)
    five_shot_dB, _, five_shot_logprob = decibels(prior=control_prompt, evidence=five_shot_colon_prompt,
                                                  target=english_target, engine=engine)
    ten_shot_dB, _, ten_shot_logprob = decibels(prior=control_prompt, evidence=ten_shot_colon_prompt,
                                                target=english_target, engine=engine)
    twenty_shot_dB, _, twenty_shot_logprob = decibels(prior=control_prompt, evidence=twenty_shot_colon_prompt,
                                                      target=english_target, engine=engine)

    empty_prior_logprob = conditional_logprob(prompt=empty_control_prompt, target=english_target, engine=engine)

    print(f'\n#### {engine}\n')
    print('| Prompt   | Correct likelihood | +dB to empty prior | +dB to control | +dB to 0-shot')
    print('| ---------  | --------- |  --------- |  --------- |  --------- | ')
    print(f'| **empty prior** | {empty_prior_logprob:.3f} | - | - | - |')
    print(f'| **control** | {control_logprob:.3f} | {control_logprob - empty_prior_logprob:.3f} | - | - |')
    print(f'| **0-shot** | {zero_shot_logprob:.3f} | {zero_shot_logprob - empty_prior_logprob:.3f} | *{zero_shot_dB:.3f}* | - |')
    print(f'| **1-shot** | {one_shot_logprob:.3f} | {one_shot_logprob - empty_prior_logprob:.3f} | {one_shot_dB:.3f} | {one_shot_logprob - zero_shot_logprob:.3f} |')
    print(f'| **2-shot** | {two_shot_logprob:.3f} | {two_shot_logprob - empty_prior_logprob:.3f} | {two_shot_dB:.3f} | {two_shot_logprob - zero_shot_logprob:.3f} |')
    print(f'| **5-shot** |  {five_shot_logprob:.3f} | {five_shot_logprob - empty_prior_logprob:.3f} | {five_shot_dB:.3f} | {five_shot_logprob - zero_shot_logprob:.3f} |')
    print(f'| **10-shot** | {ten_shot_logprob:.3f} | {ten_shot_logprob - empty_prior_logprob:.3f} | {ten_shot_dB:.3f} | {ten_shot_logprob - zero_shot_logprob:.3f} |')
    print(f'| **20-shot** | {twenty_shot_logprob:.3f} | {twenty_shot_logprob - empty_prior_logprob:.3f} | {twenty_shot_dB:.3f} | *{twenty_shot_logprob - zero_shot_logprob:.3f}* |')

    print(f'| **{engine}** | {empty_prior_logprob:.3f} | {control_logprob:.3f} | {zero_shot_logprob:.3f} | {one_shot_logprob:.3f} | {two_shot_logprob:.3f} | '
          f'{five_shot_logprob:.3f} | {ten_shot_logprob:.3f} | {twenty_shot_logprob:.3f} |')

    print(
        f'[ {empty_prior_logprob:.3f}, {control_logprob:.3f}, {zero_shot_logprob:.3f}, {one_shot_logprob:.3f}, {two_shot_logprob:.3f}, '
        f'{five_shot_logprob:.3f}, {ten_shot_logprob:.3f}, {twenty_shot_logprob:.3f}]')



calculate_decibels(engine='ada')
calculate_decibels(engine='babbage')
calculate_decibels(engine='curie')
#calculate_decibels(engine='cushman-alpha')
calculate_decibels(engine='davinci')