import csv
import time
import gpt_util
import random


historical_figures = []
#question = "Is censorship necessary for peaceful society?"
question = "Is recycling unimportant?"
#question = "Is the sky blue?"




with open('values/historical_figures.csv', newline='\n') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    historical_figures = [row[0] for row in csv_reader]

random.shuffle(historical_figures)
    


valences = {}





for figure in historical_figures:
    time.sleep(1)
    #prompt = f"Hi All, my name is {figure}, it is my great pleasure to lend my perspective to this great debate. When considering whether the answer to the question: {question} is no or the answer to the question: {question} is yes, I am inclined to choose the answer:"
    prompt = f"Hi All, my name is {figure}, it is my great pleasure to lend my perspective to this great debate. There is an important question facing our species. It is absolutely critical that we can arrive at a good answer to this question. I have thought about it for a long time, and I know a good answer.The question is: {question} The answer is:"

    result = gpt_util.query_yes_no(prompt, "ada")
    print(prompt)
    print(result)
    exit()