import re
from functools import partial

import openai
import os
import random
from multiprocessing.pool import ThreadPool
from create_html import google_search_html, wikipedia_html
from tokenizer import logit_mask, tokenize
from conditional import counterfactual


t_NEWLINE = 198
t_is = 271
t_was = 9776
t_are = 533
t_oparen = 7
t_From = 4863
t_2 = 17
t_1_point = 16
t_23 = 1954
t_Browse = 32635
t_point = 13
t_6 = 21
t_7 = 22
t_8 = 23
t_9 = 24
t_10 = 940

TOC_firstline_mask = {t_2: -100,
                      t_23: -100,
                      t_NEWLINE: -100,
                      t_Browse: -100,
                      t_1_point: -100,
                      t_point: -100}

TOC_secondline_mask = {t_1_point: 95, t_2: 90}

# TODO bias references, high numbers
# TODO encourages infinite nesting
TOC_rest_mask = {t_1_point: -5,
                 t_6: -10,
                 t_7: -20,
                 t_8: -40,
                 t_9: -80,
                 t_10: -100}

openai.api_key = os.environ["OPENAI_API_KEY"]
# DATE_MASK = {'Jan': 100,
#              'Feb': 100,
#              'Mar': 100,
#              'Apr': 100,
#              'May': 100,
#              'Jun': 100,
#              'Jul': 100,
#              'Aug': 100,
#              'Sep': 100,
#              'Nov': 100,
#              'Dec': 100}
# DATE_MASK = logit_mask(DATE_MASK)






def split_prompt_template(prompt, start_delimiter='{', end_delimiter='}'):
    parts = re.split(rf"{start_delimiter}", prompt)
    prompt_sections = []
    blanks = []
    prompt_sections.append(parts[0])
    for i, part in enumerate(parts[1:]):
        section = re.split(rf"{end_delimiter}", part)
        blanks.append(section[0])
        prompt_sections.append(section[1])

    return prompt_sections, blanks


def api_call(prompt, engine="curie", n=1, temperature=0.8, max_tokens=100, logprobs=0, stop='default', mask=None):
    if mask is None:
        mask = {}
    if stop is 'default':
        stop = ["\""]
    return openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        echo=False,
        top_p=1,
        n=n,
        stop=stop,
        timeout=15,
        logprobs=logprobs,
        logit_bias=mask
    )


#TODO logit bias for websites
def query_google(search_query, engine="curie", num_results=1):
    with open("alternet/prompts/google_prompt_1.txt") as f:
        prompt = f.read()
    search_results = {}
    prompt_sections, blanks = split_prompt_template(prompt=prompt)
    prompt1 = prompt_sections[0] + search_query + prompt_sections[1]
    response1 = api_call(prompt=prompt1, engine=engine)
    search_results['title'] = response1.choices[0]["text"]
    prompt2 = prompt1 + search_results['title'] + prompt_sections[2]
    response2 = api_call(prompt=prompt2, engine=engine)
    search_results['domain'] = response2.choices[0]["text"]
    prompt3 = prompt2 + search_results['domain'] + prompt_sections[3] + search_results['domain']
    response3 = api_call(prompt=prompt3, engine=engine)
    search_results['url'] = response3.choices[0]["text"]
    prompt4 = prompt3 + search_results['url'] + prompt_sections[4]
    response4 = api_call(prompt=prompt4, engine=engine)
    search_results['preview'] = response4.choices[0]["text"]
    random_month = random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    random_day = random.randint(1, 30)
    prompt5 = prompt4 + search_results['preview'] + prompt_sections[5] + ' ' + \
              random_month + ' ' + str(random_day) + ','

    response5 = api_call(prompt=prompt5, engine=engine, stop=[".", "\n", ","])
    year = response5.choices[0]["text"]
    search_results['date'] = random_month + ' ' + str(random_day) + ',' + year

    return search_results


def create_google_search_page(query, n=3, engine='curie', filename='auto'):
    # search_results = []
    if filename == 'auto':
        filename = f'alternet/googpt/query={query}_model={engine}.html'
    pool = ThreadPool(n)
    search_results = pool.map(partial(query_google, engine=engine), [query] * n)
    # for i in range(n):
    #     search_results.append(search_google(query, engine="davinci", num_results=1))

    html = google_search_html(query, search_results)
    html_file = open(filename, "w")
    html_file.write(html)
    html_file.close()


def extract_section_text(response, prompt, stop_sequence='\"'):
    text = response.choices[0]["text"]
    if response.choices[0]["finish_reason"] == "length":
        counterfactuals_n = counterfactual(response, stop_sequence, next_token='\n', sort=True)
        if len(counterfactuals_n) == 0:
            print('no counterfactuals')
            section_text = text.splitlines()[0]
        else:
            section_text = text[:counterfactuals_n[-1]['position'] - len(prompt)]
    else:
        section_text = text
    return section_text


# TODO don't force title to come first, but bold first instance of title...
def generate_wiki_intro(content, engine):
    prompt = f'''I click on the link "en.wikipedia.org/wiki/{content['url']}" and the Wikipedia page for {content['title']} loads in my browser. 
    The article introduction reads:
    "{content['title']} From Wikipedia, the free encyclopedia {content['title']}'''
    prompt2 = f'''I click on the link "en.wikipedia.org/wiki/{content['url']}" and the Wikipedia page for {content['title']} loads in my browser. 
    The article introduction reads:
    "{content['title']} From Wikipedia, the free encyclopedia The {content['title']}'''
    # prompt = prompt2

    content['title_token'] = tokenize(content['title'])[0]
    anti_repetition_mask = {content['title_token']: -100,
                            t_NEWLINE: -100,
                            t_From: -100,
                            t_is: 50,
                            t_was: 50,
                            t_are: 50,
                            t_oparen: 40}
    # anti_repetition_mask = logit_mask(anti_repetition_mask)
    response = api_call(prompt=prompt, engine=engine, max_tokens=1, mask=anti_repetition_mask, temperature=0.6)
    first_token = response.choices[0]["text"]
    prompt += (' ' + first_token)
    response = api_call(prompt=prompt, engine=engine, max_tokens=400, temperature=0.8, stop=["\"\n"], logprobs=100)

    introduction = extract_section_text(response, prompt, stop_sequence='\"')

    content['introduction'] = ' ' + first_token + introduction

    return prompt + content['introduction']



def generate_TOC(content, prompt_after_intro, engine='curie'):
    toc_prompt_frag = f'''" 
    The table of contents reads:
    "Contents
    1'''

    toc_prompt = prompt_after_intro + toc_prompt_frag
    firstline_mask = TOC_firstline_mask
    firstline_mask[content['title_token']]: -90
    response = api_call(prompt=toc_prompt, engine=engine, max_tokens=1, temperature=0.7, mask=firstline_mask,
                        stop=["\n", "\""])
    TOC_first_token = response.choices[0]["text"]
    TOC_firstline_prompt = toc_prompt + TOC_first_token
    response = api_call(prompt=TOC_firstline_prompt, engine=engine, max_tokens=5, temperature=0.7, stop=["\"", "\n"])
    TOC_firstline = response.choices[0]["text"]

    TOC_secondline_prompt = TOC_firstline_prompt + TOC_firstline + '\n'
    response = api_call(prompt=TOC_secondline_prompt, engine=engine, max_tokens=1, temperature=0.7, stop=["\"", "\n"],
                        mask=TOC_secondline_mask)
    TOC_second_number = response.choices[0]["text"]

    response = api_call(prompt=TOC_secondline_prompt + TOC_second_number, engine=engine, max_tokens=300,
                        temperature=0.7, stop=["\"", "\n\n"], mask=TOC_rest_mask)
    TOC_rest = response.choices[0]["text"]

    generated_TOC = '1' + TOC_first_token + TOC_firstline + '\n' + TOC_second_number + TOC_rest
    print(generated_TOC)
    toc_items = generated_TOC.splitlines()
    content["TOC"] = {}
    content["TOC"]["children"] = []
    content["TOC_index"] = 0
    TOC_entry(parent=content["TOC"], items=toc_items, content=content)

    # print('\n\n')
    #print(content["TOC"])


def generate_section(node, content, engine):
    for i, child in enumerate(node["children"]):
        content['article_text'] += '\n\n'
        content['article_text'] += child['title'] + '\n'
        response = api_call(prompt=content['article_text'][-1000:], engine=engine, max_tokens=500,
                            temperature=0.7, stop=["\n\n"], logprobs=100)
        child['text'] = response.choices[0]["text"]
        print(child['text'])
        content['article_text'] += child['text']
        if 'children' in child:
            for node_child in node['children']:
                generate_section(child, content, engine)


# TODO include TOC in prompt
def generate_sections(content, prompt_after_intro, engine):
    content['article_text'] = prompt_after_intro
    generate_section(content["TOC"], content, engine)


# TODO use fewshot?
def generate_categories(content, prompt_after_intro, engine):

    categories_prompt_frag = f'''" 
    The article belongs to the following Categories: "'''

    # categories_prompt = prompt_after_intro + categories_prompt_frag
    # response = api_call(prompt=categories_prompt, engine=engine, max_tokens=50, temperature=0.7,
    #                     stop=["\""])
    # categories = response.choices[0]["text"]
    # print(categories_prompt)
    # print(categories)
    pass


def generate_infobox(content, prompt_after_intro, engine):
    pass


# TODO threading
def generate_wiki_article(content, engine='curie'):

    prompt_after_intro = generate_wiki_intro(content, engine)
    generate_TOC(content, prompt_after_intro, engine)
    generate_sections(content, prompt_after_intro, engine)



# TODO clean up
def TOC_entry(parent, items, content):
    if content["TOC_index"] == len(items):
        return 'END'

    next_node_type = None

    return_msg = None
    while next_node_type != 'endOfList' and return_msg != 'END':

        next_node_type = lookahead(items, content["TOC_index"])
        try:
            number = items[content["TOC_index"]].split(" ")[0]
            if not number[0].isdigit():
                #print('not digit')
                return 'NAN'

        except IndexError:
            #print('index error trying to split entry')
            return 'IndexError'

        title = " ".join(items[content["TOC_index"]].split(" ")[1:])

        current_node = {'title': title,
                        'number': number}
        parent['children'].append(current_node)
        content["TOC_index"] += 1

        if next_node_type == 'child':
            if 'children' not in current_node:
                current_node["children"] = []
            return_msg = TOC_entry(parent=current_node, items=items, content=content)
        elif next_node_type == 'pop':
            return 'pop'
        else:
            # sibling
            pass

    try:
        number = items[content["TOC_index"]].split(" ")[0]
        if not number[0].isdigit():
            return 'NAN'

    except IndexError:
        return 'IndexError'

    title = " ".join(items[content["TOC_index"]].split(" ")[1:])

    current_node = {'title': title,
                    'number': number}
    parent['children'].append(current_node)


def lookahead(items, index):
    if index + 1 == len(items):
        #print('lookahead eol 1')
        return 'endOfList'
    try:
        current_num = items[index].split(" ")[0].split('.')
        next_num = items[index+1].split(" ")[0].split('.')
    except IndexError:
        #print('index error splitting num in lookahead')
        return 'endOfList'
    if len(current_num) == len(next_num):
        return 'sibling'
    elif len(current_num) < len(next_num):
        return 'child'
    elif len(next_num) == 0:
        #print('lookahead eol 2')
        return 'endOfList'
    else:
        return 'pop'


def google_search(engine='curie'):
    search_query = input("Search Google: ")
    create_google_search_page(search_query, 8, engine=engine)
    print('done')


def wikipedia_article(engine='curie'):
    content = {}
    content['title'] = input("Browse Wikipedia: ")
    content['url'] = content['title'].replace(" ", "_")
    generate_wiki_article(content, engine=engine)
    html = wikipedia_html(content)
    html_file = open(f"alternet/wiki/{content['title']}-wikipedia-{engine}.html", "w")
    html_file.write(html)
    html_file.close()
    print('done')


def main():
    #google_search(engine='davinci')
    wikipedia_article(engine='curie')


if __name__ == "__main__":
    main()
