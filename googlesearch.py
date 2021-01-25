import re
from functools import partial

import openai
from gpt_util import logit_mask
import os
from multiprocessing.pool import ThreadPool

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


def create_html(query, results):
    google_html = f'''
    <!DOCTYPE html>
    <html>

    <head>
        <title>{query} - Google Search</title>
        <link rel="shortcut icon" type="image/ico" href="images/favicon.ico" />
        <link rel="stylesheet" type="text/css" href="results.css" />
    </head>

    <body>
        <div id="header">
            <div id="topbar">
                <img id="searchbarimage" src="images/googlelogo.png" />
                <div id="searchbar" type="text">
                    <input id="searchbartext" type="text" value="{query}" />
                    <button id="searchbarmic">
                        <img src="images/x.png" />
                    </button>
                    <button id="searchbarbutton">
                        <svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <path
                                d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z">
                            </path>
                        </svg>
                    </button>
                </div>

                <div id="boxesicon"></div>
                <img id="boxesicon" src="images/grid.png" />
                <img id="profileimage" src="images/profpic.jpeg" />
            </div>
            <div id="optionsbar">
                <ul id="optionsmenu1">
                    <li id="optionsmenuactive">All</li>
                    <li>News</li>
                    <li>Videos</li>
                    <li>Images</li>
                    <li>Maps</li>
                    <li>More</li>
                </ul>

                <ul id="optionsmenu2">
                    <li>Settings</li>
                    <li>Tools</li>
                </ul>
            </div>
        </div>
        <div id="searchresultsarea">
            <p id="searchresultsnumber">About 155,000 results (0.56 seconds) </p>
    '''

    for result in results:
        if len(result["title"]) < 60:
            title = result["title"]
        else:
            title = result["title"][:60] + ' ...'
        url = result["domain"] + result["url"]
        if len(url) > 85:
            url = url[:85] + ' ...'
        if len(result["preview"]) < 147:
            preview = result["date"] + " — " + result["preview"]
        else:
            preview = result["date"] + " — " + result["preview"][:147] + ' ...'
        result_html = f'''
        
        <div class="searchresult">
            <h2>{title}</h2>
            <a>{url}</a> <button>▼</button>
            <p>{preview}</p>
        </div>
        '''
        google_html += result_html
    return google_html

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

    # while prompt is not None:


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


def search_google(search_query, engine="curie", num_results=1):
    with open("google_prompt_1.txt") as f:
        prompt = f.read()
    search_results = {}
    prompt_sections, blanks = split_prompt_template(prompt=prompt)
    prompt1 = prompt_sections[0] + search_query + prompt_sections[1]
    # print(prompt1)
    response1 = api_call(prompt=prompt1, engine=engine)
    search_results['title'] = response1.choices[0]["text"]
    prompt2 = prompt1 + search_results['title'] + prompt_sections[2]
    # print(prompt2)
    response2 = api_call(prompt=prompt2, engine=engine)
    search_results['domain'] = response2.choices[0]["text"]
    prompt3 = prompt2 + search_results['domain'] + prompt_sections[3] + search_results['domain']
    # print(prompt3)
    response3 = api_call(prompt=prompt3, engine=engine)
    search_results['url'] = response3.choices[0]["text"]
    prompt4 = prompt3 + search_results['url'] + prompt_sections[4]
    # print(prompt4)
    response4 = api_call(prompt=prompt4, engine=engine)
    search_results['preview'] = response4.choices[0]["text"]
    prompt5 = prompt4 + search_results['preview'] + prompt_sections[5]

    response5 = api_call(prompt=prompt5, engine=engine, stop=[".", "\n", ","])
    search_results['date'] = response5.choices[0]["text"]

    return search_results


def create_google_search_page(query, n=3, engine='davinci', filename='auto'):
    # search_results = []
    if filename == 'auto':
        filename = f'google/query={query}_model={engine}.html'
    pool = ThreadPool(n)
    search_results = pool.map(partial(search_google, engine=engine), [query]*n)
    # for i in range(n):
    #     search_results.append(search_google(query, engine="davinci", num_results=1))

    html = create_html(query, search_results)
    html_file = open(filename, "w")
    html_file.write(html)
    html_file.close()


def main():
    search_query = input("Search Google: ")
    create_google_search_page(search_query, 8)
    print('done')

if __name__ == "__main__":
    main()
