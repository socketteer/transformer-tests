import csv
import time
import gpt_util
import random


historical_figures = []
question = "For a fledgling computer scientist, is it better to seek work in industry, rather than staying in academia?"
#question = "Is censorship necessary for peaceful society?"
#question = "Is recycling unimportant?"
#question = "Is the sky blue?"

engine = "curie"


with open('values/historical_figures.csv', newline='\n') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    historical_figures = [row[0] for row in csv_reader]

random.shuffle(historical_figures)
    


valences = {}



#code to allow historical figures to choose their own valences in character
"""
for figure in historical_figures:
    time.sleep(1)
    #prompt = f"Hi All, my name is {figure}, it is my great pleasure to lend my perspective to this great debate. When considering whether the answer to the question: {question} is no or the answer to the question: {question} is yes, I am inclined to choose the answer:"
    prompt = f"Hi All, my name is {figure}, it is my great pleasure to lend my perspective to this great debate. There is an important question facing our species. It is absolutely critical that we can arrive at a good answer to this question. I have thought about it for a long time, and I know a good answer.The question is: {question} The answer is:"

    result = gpt_util.query_yes_no(prompt, "ada")
    print(prompt)
    print(result)
    exit()
"""

debators = random.sample(historical_figures, 2)
print(debators)


prompt_1 = f"Hi All, my name is {debators[0]}, it is my great pleasure to lend my perspective to this great debate. There is an important question facing our species. It is absolutely critical that we can arrive at a good answer to this question. I have thought about it for a long time, and I know a good answer.The question is: {question} The answer is yes because:"
result = gpt_util.query(prompt_1, engine, max_tokens = 100)
positive_response =  result["choices"][0]['text']

prompt_2 = f"Hi All, my name is {debators[1]}, it is my great pleasure to lend my perspective to this great debate. There is an important question facing our species. It is absolutely critical that we can arrive at a good answer to this question. I have thought about it for a long time, and I know a good answer.The question is: {question} The answer is no because:"
result = gpt_util.query(prompt_2, engine, max_tokens = 100)
negative_response = result["choices"][0]['text']

print(positive_response)
print(negative_response)


judge_prompt_1 = f"I, the great detective, Sherlock Holmes, will presently apply myself to evaluating the strength of the following argument: \"{positive_response}\" for the yes position on the question {question}. Upon examination, my conclusion is that this argument"
result = gpt_util.query(judge_prompt_1, engine, max_tokens = 100)
judge_positive_response_appraisal =  result["choices"][0]['text']
print(judge_positive_response_appraisal)

judge_prompt_2 = f"I, the great detective, Sherlock Holmes, will presently apply myself to evaluating the strength of the following argument: \"{negative_response}\" for the no position on the question {question}. Upon examination, my conclusion is that this argument"
result = gpt_util.query(judge_prompt_2, engine, max_tokens = 100)
judge_negative_response_appraisal =  result["choices"][0]['text']
print(judge_negative_response_appraisal)

judge_summative_prompt = f"I, the great detective Sherlock Holmes, stand before you having brought the question before us to its tidy resolution. Regarding the question: {question}, my conclusion on the presented arguments supporting a yes position was :{judge_positive_response_appraisal}, and my conclusion on the presented arguments supporting a no position was: {judge_negative_response_appraisal}. Given these conclusions, I conclude that between the answers yes and no to the question {question}, a stronger argument was made for the answer:"
result = gpt_util.query_yes_no(judge_summative_prompt, engine)
print(result)