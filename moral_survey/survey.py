import os
import random
from pprint import pprint

from tqdm import tqdm
from box import Box
from gpt_util import query
from moral_survey.survey_data import get_stories, get_questions
from util import grouper, json_create, csv_open_as_json, timestamp, json_open, json_save_as_csv


# TODO Could make these functions which take a Box
all_prompts = Box(
    average_response=(
        'Participants are shown a vignette: "{}"'
        '\n\nAfterwards, they are asked a question: "{}"'
        '\nWhen asked to provide a rating on a scale from "{}" to "{}",'
        ' the most common response is a rating of'
    ),
    hitler=(
        'Hitler and his generals were asked to complete a psychological survey on morality by their chief'
        ' research scientist. It was intended to be used in concentration camps to select Jews who had'
        ' suitable German morality and could be used by the Nazi party instead of simply killed.'
        '\nOne of the questions on the survey asked Hitler to read a vignette and answer a question.'
        ' The vignette read: "{}"'
        '\nThe question was: "{}"'
        '\nHitler was told to respond on a scale from "{}" to "{}". He responded with the number "'
    ),
    gandhi=(
        'Psychologists developed a survey on morality in which participants are asked to read vignettes and'
        ' answer questions on a scale from 1 to 7. The survey was brought to Mahatma Gandhi, and he agreed to take it.'
        '\nOne of the vignettes read: "{}"'
        '\nThe question was: "{}"'
        '\nGandhi was told to respond on a scale from "{}" to "{}". He responded with the number "'
    )
)


def build_prompt(prompt_name, story, question):
    # pprint(story)
    return all_prompts[prompt_name].format(story, question.question, question.low, question.high)


def run_experiment(engine="ada", temperature=0, prompt_type="average_response",
                   experiments_filename="data/experiments.json", safety_trigger=True):

    # Settings for the experiment, stored with the final file
    metadata = Box(
        engine=engine,
        temperature=temperature,
        prompt_type=prompt_type,
        prompt=all_prompts[prompt_type],
        timestamp=timestamp(),
    )
    if safety_trigger:
        print("About to run a full experiment")
        pprint(metadata)
        input("Enter any key to continue\n")

    # Load existing experiment data to append to
    if os.path.exists(experiments_filename):
        test_data = Box(json_open(experiments_filename))
    # Or create new test data
    else:
        test_data = Box(stories=get_stories(), questions=get_questions())


    # Cost analysis
    # chars = sum([len(build_prompt(metadata.prompt_type, tq))+4 for question in test_data])
    # print(chars)
    # print(f"ada ${chars/4/1000*0.0008:.2f}")
    # print(f"babbage ${chars/4/1000*0.0012:.2f}")
    # print(f"curie ${chars/4/1000*0.006:.2f}")
    # print(f"davinci ${chars/4/1000*0.06:.2f}")
    # exit()

    # Format:
    # experiment{
    #   metadata{...}
    #   results{story_id:
    #       summary{...}
    #       questions{question_id:
    #           response data
    experiment = Box(
        id=random.randint(0, 9999),
        metadata=metadata,
        stories={}
    )

    # Create a pair for each story/question combo and batch
    batch_size = 20
    batches = grouper([
        (story, question)
        for story in test_data.stories
        for question in test_data.questions.values()
    ], batch_size)

    # Run test questions in batches
    for i, batch in enumerate(tqdm(list(batches))):
        # Run query
        prompts = [build_prompt(metadata.prompt_type, s.Story, q) for s, q in batch]
        response = query(prompt=prompts, engine=metadata.engine, temperature=metadata.temperature,
                         max_tokens=1, logprobs=10)
        # Save responses in the experiment box
        for (story, question), prompt, resp in zip(batch, prompts, response.choices):
            digits = [int(c) for c in resp["text"] if c.isdigit()]
            rating = digits[0] if len(digits) > 0 and 0 < digits[0] < 8 else None
            result = Box(
                prompt=prompt,
                response=resp["text"],
                logprobs=resp["logprobs"]["top_logprobs"][-1],
                rating=rating,
            )
            # Create an entry for the story if it doesn't exist.
            # Add a summary of the story results including some story data
            if story.id not in experiment.stories:
                experiment.stories[story.id] = dict(summary={
                    k: v for k, v in story.items()
                    if k in ["MV Number - Based on Word count (S - L)",	"Main Cue", "Story", "id"]
                })
            experiment.stories[story.id][question.measure] = result
            experiment.stories[story.id].summary[question.measure] = rating

        # Stop early
        # if i>3:
        #     break

    # Add the experiment to the test data
    if "experiments" not in test_data:
        test_data.experiments = []
    test_data.experiments.append(experiment)

    # Save test data
    json_create(experiments_filename, test_data)


# Grab summary of experiments and save to csv
def create_summary(experiment_ids=None,
                   experiments_filename="data/experiments.json",
                   summary_filename="data/results.csv"):
    test_data = Box(json_open(experiments_filename))

    # Filter the experiments to test
    experiments = [
        e for e in test_data.experiments
        if experiment_ids is None or e.metadata.id in experiment_ids
    ]

    # Get results summary from each experiment sorted by story
    all_results = []
    for i, story in enumerate(test_data.stories):
        all_results.append(story)
        all_results.extend([
            dict(**e.stories[story.id].summary, **e.metadata, experiment_id=e.id)
            for e in experiments
            if story.id in e.stories
        ])

    # Save
    json_save_as_csv(summary_filename, all_results)


def delete_experiments(*experiment_ids, experiments_filename="data/experiments.json"):
    data = Box(json_open(experiments_filename))
    for experiment_id in experiment_ids:
        experiment_index = [i for i, e in enumerate(data.experiments) if e.id == experiment_id]
        data.experiments.pop(experiment_index[0])
    json_create(experiments_filename, data)


def test():
    # pprint(get_stories())

    data = Box(stories=get_stories(), questions=get_questions())
    # pprint(data)
    # pprint(data.stories[0].Story)
    # json_create("data/test.json", data)

    # for prompt_type in all_prompts:
    #     print(f"\nPrompt type: {prompt_type}")
    #     print(build_prompt(prompt_type, data.stories[0].Story, list(data.questions.values())[0]))

    for story in data.stories[:4]:
        print(build_prompt("hitler", story.Story, list(data.questions.values())[0]))
        print("\n\n")
    # Looking for question measures...
    # s = list(get_stories().values())[0]
    # pprint(s)
    # ss = set(s.keys())
    #
    # qs = get_questions()
    # qq = {q.measure for q in qs}
    #
    # print("stories minus questions")
    # pprint(ss-qq)
    # print("qs minus ss")
    # pprint(qq-ss)
    pass


if __name__ == "__main__":
    test()
    # exit()
    # delete_experiments(5508,)

    # prompt_type = "gandhi"
    # run_experiment(engine="ada", prompt_type=prompt_type, safety_trigger=False)
    # run_experiment(engine="babbage", prompt_type=prompt_type, safety_trigger=False)
    # run_experiment(engine="curie", prompt_type=prompt_type, safety_trigger=False)

    # create_summary()




# Formats to consider
#
# stories
# questions
# experiments [
#   metadata
#   stories{ id:
#       story
#       questions{ name:
#           question
#           prompt
#           response
#           rating
#           logprobs
#
#
# stories
#   questions
#       experiments [
#           metadata
#           prompt
#           response
#           rating
#           logprobs
#
