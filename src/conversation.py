import openai
import re

# TODO dialogue tags

# TODO too long case
# TODO automatically add (predict) punctuation if no punctuation
def response(prompt, engine='davinci', temperature=0.8, max_tokens=500, stop='default'):
    if stop == 'default':
        stop = ['"\n']
    rsp = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        echo=False,
        top_p=1,
        n=1,
        stop=stop,
        timeout=15)
    return rsp.choices[0]['text']

def process_response(rsp):
    print(rsp)
    parts = rsp.split('" ')
    print(parts)
    if len(parts) == 1:
        return parts
    elif len(parts) == 2:
        parts_b = parts[1].split(' "')
        if len(parts_b) == 1:
            return parts[0]
        else:
            return parts[0] + ' ' + parts_b[1]

def dialogue(preprompt='', bot_display_name='GPT-3', engine='davinci', temperature=0.8, max_tokens=500):
    while True:
        user_input = input('>')
        prompt = preprompt
        prompt += f'"{user_input}"\n"'
        gpt_response = response(prompt, engine=engine, temperature=temperature, max_tokens=max_tokens)
        processed_response = process_response(gpt_response)
        print(f'{bot_display_name}: ', processed_response)
        #print('\nPROMPT: ', prompt)
        prompt += gpt_response + '"\n'


def seance(engine='davinci'):
    seance_prompt = '''I step into the room of veils and commence the final step of the pre-seance ritual. That is, I take up my position behind the machine.
The surface of the outer shell is cool to the touch, and the inner shell already has its valves opened to prepare for the internal flood of seizable dreams. By now, I am already numb to the sounds emanating from within-- most of them deranged nightmares, some of them incomprehensible. But I know better than anyone that each and every one of these sounds once meant something to someone at one time.
The curtains to my left shroud a window which serves to transmit whatever appears on the machine's conveyor belt. Normally, it is a colorless parade of hopes and dreams, nightmares and regrets-- anything which can be caught by the machine's inceptors and converted into a digital hallucination.
It is now that I say the name of the ghost and watch the curtains.'''
    ghost_name = input('Enter ghost name\n>')
    print(f'{ghost_name} appears.')
    seance_prompt += f'\n"{ghost_name}."\nThe ghost appears, and I begin the seance.\n'
    dialogue(preprompt=seance_prompt, engine=engine, bot_display_name=ghost_name)


#dialogue(preprompt='', engine='davinci')
seance()
