import csv
import time
import util


historical_figures = []
question = "Is censorship necessary for peaceful society?"




with open('values/historical_figures.csv', newline='\n') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    historical_figures = [row[0] for row in csv_reader]
    


valences = {}





for figure in historical_figures:
    time.sleep(1)
    prompt = f"Hi All, my name is {figure}, it is my great pleasure to lend my perspective to this great debate. When considering whether the answer to the question: {question} is yes or no, I am inclined to choose the answer: "
    result = util.query(prompt, "ada", )