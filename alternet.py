import re
from functools import partial

import openai
import os
import random
from multiprocessing.pool import ThreadPool
from create_html import google_search_html, wikipedia_html
from tokenizer import logit_mask, tokenize


NEWLINE_ID = 198
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


def api_call(prompt, engine="curie", n=1, temperature=0.8, max_tokens=100, stop=["\""], mask=None):
    if mask is None:
        mask = {}
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
        logit_bias=mask
    )


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


def generate_wiki_article(content, engine='curie'):
    prompt = f'''
I click on the link "en.wikipedia.org/wiki/{content['url']}" and the Wikipedia page for {content['title']} loads in my browser. 
The article introduction reads:
"{content['title']} From Wikipedia, the free encyclopedia {content['title']}
'''
    # TODO don't force title to come first, but bold first instance of title...
    title_token = tokenize(content['title'])[0]
    from_token = tokenize(['From'])[0][0]
    is_token = tokenize(['is'])[0][0]
    are_token = tokenize(['are'])[0][0]
    was_token = tokenize(['was'])[0][0]
    open_paren_token = tokenize(['('])[0][0]
    anti_repetition_mask = {title_token: -100,
                            NEWLINE_ID: -100,
                            from_token: -100,
                            is_token: 50,
                            was_token: 50,
                            are_token: 50,
                            open_paren_token: 40}
    #anti_repetition_mask = logit_mask(anti_repetition_mask)
    response = api_call(prompt=prompt, engine=engine, max_tokens=1, mask=anti_repetition_mask, temperature=0.6)
    first_token = response.choices[0]["text"]
    prompt += (' ' + first_token)
    response = api_call(prompt=prompt, engine=engine, max_tokens=400, temperature=0.7)
    content['content'] = ' ' + first_token + response.choices[0]["text"]
    return content


def google_search():
    search_query = input("Search Google: ")
    create_google_search_page(search_query, 8, engine='davinci')
    print('done')

def wikipedia_article(engine):
    content = {}
    content['title'] = input("Browse Wikipedia: ")
    content['url'] = content['title'].replace(" ", "_")
    content = generate_wiki_article(content, engine=engine)
    html = wikipedia_html(content)
    html_file = open(f"alternet/wiki/{content['title']}-wikipedia-{engine}.html", "w")
    html_file.write(html)
    html_file.close()
    print('done')

def main():
    #google_search()
    wikipedia_article(engine='davinci')


if __name__ == "__main__":
    main()
