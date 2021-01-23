import os
from pprint import pprint
import random

from gpt_util import query
from util import json_open, json_create, json_append_dict


# Official script
"""return a tuple with recall, precision, and f1 for one example"""
def computeF1(goldList, predictedList):

  """Assume all questions have at least one answer"""
  if len(goldList) == 0:
    raise Exception("gold list may not be empty")
  """If we return an empty list recall is zero and precision is one"""
  if len(predictedList) == 0:
    return (0, 1, 0)
  """It is guaranteed now that both lists are not empty"""

  precision = 0
  for entity in predictedList:
    if entity in goldList:
      precision+=1
  precision = float(precision) / len(predictedList)

  recall = 0
  for entity in goldList:
    if entity in predictedList:
      recall+=1
  recall = float(recall) / len(goldList)

  f1 = 0
  if precision+recall>0:
    f1 = 2*recall*precision / (precision + recall)
  return (recall, precision, f1)


def extract_question(d):
    return d["utterance"]#[0]#.capitalize() + d["utterance"][1:]


def extract_answers(question_data):
    answer_list = question_data["targetValue"]
    # Remove starting and ending ()
    assert answer_list.startswith("(") and answer_list.endswith(")"), answer_list
    answer_list = answer_list[1:-1]
    # Remove (description
    assert "(description " in answer_list, answer_list
    dirty_answers = answer_list.split("(description ")[1:]
    # Remove spaces then SINGLE ending and then quotes
    answers = [a.strip()[:-1].strip("\"") for a in dirty_answers]
    assert all(map(lambda s: s.strip().endswith(")"), dirty_answers)), dirty_answers
    assert all([a for a in answers]), answers
    return answers


def openai_prompt(question, example_questions=None, example_answers=None):
    if example_questions is None:
        example_questions, example_answers = [], []
    example_questions.append(question)
    example_answers.append("")
    return "\n\n".join(f"Q: {question}\nA:{answer}" for question, answer in zip(example_questions, example_answers))

def plain(question, example_questions=None, example_answers=None):
    if example_questions is None:
        example_questions, example_answers = [], []
    example_questions.append(question)
    example_answers.append("")
    dq = "\""
    sq = "'"
    return "\n".join(f"{question}\t{str(answer).replace(sq, dq)}" for question, answer in zip(example_questions, example_answers)) + "[\""


def get_random_examples(test, num, do_not_select=None):
    test = test.copy()
    if do_not_select is not None:
        test.remove(do_not_select)
    if num == 0:
        return [], []
    examples = random.sample(test, k=num)
    if num == 1:
        examples = examples
    questions = [extract_question(d) for d in examples]
    answers = [" " + extract_answers(d)[0] for d in examples]
    return questions, answers


def main():
    test_data = json_open("data/test.json")

    metadata = {
        "test": "webqs",
        "engine": "davinci",
        "prompt_format": "plain",
        "shots": 10,
        "debug": False,
    }

    output_file = (f"data/"
                   f"{'DEBUG-' if metadata['debug'] else ''}"
                   f"{metadata['test']}"
                   f"__engine={metadata['engine']}"
                   f"__prompt={metadata['prompt_format']}"
                   f"__shots={metadata['shots']}"
                   f""
                   f".json"
    )


    if not os.path.isfile(output_file) or input(f"Delete and replace {output_file}? (y/n)\n") == "y":
        print("Creating new file")
        json_create(output_file, [metadata])
    test_results = json_open(output_file)
    already_answered = list([d["question"] for d in test_results[1:]])


    for i, d in enumerate(test_data):
        if metadata["debug"] and i > 25:
            continue

        question = extract_question(d)
        answers = extract_answers(d)
        if question in already_answered:
            continue

        # example_questions, example_answers = get_random_examples(test_data, metadata["shots"], do_not_select=d)
        example_questions = [extract_question(test_data[i-j-1 % len(test_data)]) for j in range(metadata["shots"])]
        example_answers = [extract_answers(test_data[i-j-1 % len(test_data)]) for j in range(metadata["shots"])]

        prompt_func = globals()[metadata["prompt_format"]]
        prompt = prompt_func(question, example_questions, example_answers)

        response = query(prompt=prompt, engine=metadata["engine"], max_tokens=10)
        guess = response["choices"][0]["text"]
        correct = any([a.lower() in guess.lower().strip("'\"]") for a in answers])
        recalled = any([guess.lower().strip("'\"]") in a.lower() for a in answers])

        print(f"Finished {i}/{len(test_data)}")
        print(f"\tQ: {question}\n\tA:{guess}")
        print(f"\tAnswers {answers}")
        print(f"\tCorrect: {correct}")
        print(f"\tRecalled: {recalled}")

        json_append_dict(output_file, {
            "i": i,
            "question": question,
            "prompt": prompt,
            "guess": guess,
            "answers": answers,
            "correct": correct,
            "recalled": recalled,
        })

    analyze_results(output_file)


def analyze_results(results_file):
    data = json_open(results_file)
    data = [d for d in data if "correct" in d]
    correct = [d for d in data if d["correct"]]
    print(f"Correct: {len(correct)}/{len(data)}: {len(correct)/len(data)}")
    if "recalled" in data[0]:
        recalled = [d for d in data if d["recalled"]]
        print(f"Recalled: {len(recalled)}/{len(data)}: {len(recalled) / len(data)}")
        cor_or_rec = [d for d in data if d["recalled"] or d["correct"]]
        print(f"Correct or recalled: {len(cor_or_rec)}/{len(data)}: {len(cor_or_rec) / len(data)}")


if __name__ == "__main__":
    # main()
    analyze_results("data/webqs__engine=davinci__prompt=plain__shots=10.json")


# OpenAI
# Correct: 616/2032: 0.3031496062992126

# Simple, no quotes
# Correct: 650/2032: 0.3198818897637795
# Recalled: 593/2032: 0.2918307086614173