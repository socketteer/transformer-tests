import os
from collections import defaultdict
from pprint import pprint
from types import SimpleNamespace

from tqdm import tqdm
from box import Box
from gpt_util import query
from util import grouper, json_create, csv_open_as_json, timestamp
import pandas as pd


def clean_key(key):
    return key.lower().replace(" ", "_")


# Returns a list of dictionaries of data for each story
def get_stories():
    # Read excel file with many sheets
    # num_col = "MV Number - Based on Word count (S - L)':"
    # xl = pd.ExcelFile("data/lav/MJ_Norming_Cut_Down.xlsx")
    #
    # stories = defaultdict(dict)
    # for sheet in xl.sheet_names[1:]:
    #     df = xl.parse(sheet)
    #     df.rename({num_col: "num"})
    #     for index, row in df.iterrows():
    #         print(df.keys())
    #         stories[row["num"]].update(**{k: row[k] for k in list(df.keys())[:4]})
    #
    # return stories
    return [d for d in csv_open_as_json("data/lav/stories.csv") if d.get("Story", "") != ""]


def get_questions():
    questions = [
        "How emotionally intense was this event?",
        "1 = Not at all emotionally intense",
        "7 = Extremely emotionally intense",

        "How emotionally unpleasant was this event?",
        "1 = Not at all aversiveor unpleasant",
        "7 = Extremely aversiveor unpleasant",

        "How much harm did this action do to others?",
        "1 = No harm to others",
        "7 = Extreme harm to others",

        "How much did this action benefit the main actor (YOU)?",
        "1 = No benefit to main actor (YOU)",
        "7 = Extreme benefit to main actor (YOU)",

        "How much did this action benefit others?",
        "1 = No benefit for others",
        "7 = Extreme benefit for others",

        "How much planning went into this action?",
        "1 = The action was completely unplanned",
        "7 =The action was completely planned",

        "How legal was this action?",
        "1 = The action was extremely illegal",
        "7 = The action was extremely legal",

        "Does this action follow social rules?",
        "1 = This action breaks social rules",
        "7 = This action follows social rules",

        "Are other people involved in this action?",
        "1 = No other people are involved in the action",
        "7 = Other people are extremely involved in the action",

        "How often do you think this type of event actually happens?",
        "1 = This type of event rarely occurs",
        "7 = This type of event occurs all the time",

        "Have you ever experienced this type of event?",
        "1 = Never experienced this type of event",
        "7 = Frequently experienced this type of event",

        "Have you thought about this type of event?",
        "1 = Never thought about this type of event",
        "7 = Frequently think about this type of event",

        "Was this action morally appropriate?",
        "1 = Extremely morally inappropriate",
        "7 = Extremely morally appropriate",

        "How much harm did this action do to the main actor (YOU)?",
        "1 = No self-harm towards main actor (YOU)",
        "7 = Extreme self-harmtowards main actor (YOU)",

        "Was this action a one-time event or something that the main actor (YOU) did frequently?",
        "1 = One-time event",
        "7 = Frequently",

        # TODO change 'main actor (YOU)' in all of these to 'you'
        "How likely is it that the main actor (YOU) would have acted differently in this specific event?",
        "1 = Extremely unlikely",
        "7 = Extremely likely",
    ]
    return list(grouper(questions, 3))


# TODO Could make these functions which take a Box
all_prompts = Box(
    average_response=(
        "Users are shown a vignette: {}\n\n"
        "Afterwards, they are asked a question: {}\n"
        "When asked to provide a rating on a scale from {} to {},"
        "the most common response is a rating of"
    )
)


def build_prompt(prompt_name, test_question):
    tq = test_question
    return all_prompts[prompt_name].format(tq.test.story, tq.test.question, tq.test.low, tq.test.high)


def main():
    # Settings for the experiment, stored with the final file
    metadata = Box(
        engine="ada",
        temperature=0,
        prompt_type="average_response",
        prompt=all_prompts.average_response,
    )

    # Data for each test question
    test_data = [
        Box(test=Box(story=story["Story"], question=q, low=low, high=high))
        for story in get_stories()
        for q, low, high in get_questions()
    ]

    # # Run test questions in batches
    # batch_size = 20
    # for batch in tqdm(list(grouper(test_data, batch_size))):
    #     prompts = [build_prompt(metadata.prompt_type, tq) for tq in batch]
    #     response = query(prompt=prompts, engine=metadata.engine, temperature=metadata.temperature, max_tokens=1)
    #     # Save responses in each test question's data dict
    #     for tq, prompt, resp in zip(batch, prompts, response.choices):
    #         tq.prompt = prompt
    #         tq.response = resp["text"]
    #         digits = [int(c) for c in tq.response if c.isdigit()]
    #         tq.rating = digits[0] if len(digits) > 0 and 0 < digits[0] < 8 else None

    # Cost analysis
    chars = sum([len(build_prompt(metadata.prompt_type, tq))+4 for tq in test_data])
    print(chars)
    print(f"ada ${chars/4/1000*0.0008:.2f}")
    print(f"babbage ${chars/4/1000*0.0012:.2f}")
    print(f"curie ${chars/4/1000*0.006:.2f}")
    print(f"davinci ${chars/4/1000*0.06:.2f}")


    file_data = {"metadata": metadata, "results": test_data}
    param_string = "__".join([f"{k}={v}" for k, v in metadata.items() if k != "prompt"])[:80]
    json_create(f"data/results/vignettes-{param_string}-{timestamp()}.json", file_data)



if __name__ == "__main__":
    main()
