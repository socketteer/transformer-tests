import json
import os
import time
from collections import namedtuple
from pprint import pprint

import openai
from recordclass import recordclass


openai.api_key = os.environ["OPENAI_API_KEY"]


def query(prompt, engine, attempts=3, delay=1, max_tokens=200):
    if attempts < 1:
        raise TimeoutError
    try:
        return openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=0.0,
            max_tokens=max_tokens,
            echo=False,
            top_p=1,
            n=1,
            stop=["\n"],
            timeout=15,
        )
    except Exception as e:
        print(f"Failed to query, {attempts} attempts remaining, delay={delay}")
        print(e)
        time.sleep(delay)
        return query(prompt, engine, attempts=attempts-1, delay=delay*2)




def json_create(filename, data=None):
    print(f"Writing to {filename}")
    data = data if data else []
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def json_append_dict(filename, data_dict):
    with open(filename) as f:
        try:
            json_data = json.load(f)
        except json.decoder.JSONDecodeError as err:
            with open(filename) as file:
                string = file.read()
                print(string[err.pos-500:err.pos+500])
            raise err
    json_data += [data_dict]
    json_create(filename, json_data)


def json_open(filename):
    with open(filename) as f:
        return json.load(f)


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
        content = [x.strip() for x in content if x.strip()]
    return content

