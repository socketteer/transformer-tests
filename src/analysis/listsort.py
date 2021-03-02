import math

import pandas as pd
from matplotlib import pyplot as plt

tests = [
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 0, "accuracy": 0.28, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 1, "accuracy": 0.40, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 3, "accuracy": 0.30, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 5, "accuracy": 0.28, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 7, "accuracy": 0.32, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 10, "accuracy": 0.50, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 13, "accuracy": 0.36, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 16, "accuracy": 0.22, "trials": 50},
    { "task": "listsort", "prompt": "examples", "length": 5, "shots": 32, "accuracy": 0.20, "trials": 50},

    { "task": "listsort", "prompt": "code", "length": 5, "shots": 0, "accuracy": 0.76, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 1, "accuracy": 0.66, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 3, "accuracy": 0.46, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 5, "accuracy": 0.44, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 7, "accuracy": 0.44, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 10, "accuracy": 0.42, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 13, "accuracy": 0.30, "trials": 50},
    { "task": "listsort", "prompt": "code", "length": 5, "shots": 16, "accuracy": 0.32, "trials": 50},


    # { "task": "listsort", "prompt": "examples", "length": 10, "shots": 0, "accuracy": 0.04, "trials": 50},
    # { "task": "listsort", "prompt": "examples", "length": 10, "shots": 1, "accuracy": 0.04, "trials": 50},
    # { "task": "listsort", "prompt": "examples", "length": 10, "shots": 10, "accuracy": 0.00, "trials": 50},
    # { "task": "listsort", "prompt": "examples", "length": 10, "shots": 32, "accuracy": 0.00, "trials": 50},
    # { "task": "listsort", "prompt": "code", "length": 10, "shots": 0, "accuracy": 0.04, "trials": 50},
    # { "task": "listsort", "prompt": "code", "length": 10, "shots": 1, "accuracy": 0.14, "trials": 50},
    # { "task": "listsort", "prompt": "code", "length": 10, "shots": 10, "accuracy": 0.00, "trials": 50},
]
for d in tests:
    d["code"] = d["prompt"] == "code"
    d["correct"] = d["accuracy"] * d["trials"]
    p = d["accuracy"]
    # 80% confidence: 0.842
    # 95% confidence:
    d["err"] = 0.842 * math.sqrt(p * (1-p) / d["trials"])

df = pd.DataFrame(tests)


plt.style.use('dark_background')
examples_df = df[df["prompt"] == "examples"]
plt.errorbar('shots', 'accuracy', yerr=examples_df["err"], data=examples_df, marker='o', capsize=2,
             color='mediumorchid', markersize=4, linewidth=1, linestyle='-', label="Examples")

code_df = df[df["prompt"] == "code"]
plt.errorbar('shots', 'accuracy', yerr=code_df["err"], data=code_df, marker='o', capsize=4,
             color='darkcyan', markersize=4, linewidth=1, label="Coding")


plt.legend()
plt.xlabel("Shots")
plt.ylabel("Accuracy")
plt.title("List Sort Length 5")
# plt.savefig('Fig2.png', dpi=300, bbox_inches='tight')
plt.show()



# seaborn.lineplot(data=df, x="shots", y="correct", hue="prompt", ci="sd")




# length 99
# { "task": "listsort", "prompt": "examples", "length": 5, "shots" 10, "accuracy": 0.46, "trials": 50},
# { "task": "listsort", "prompt": "code", "length": 5, "shots": 0, "accuracy": 0.50, "trials": 50},
# { "task": "listsort", "prompt": "code", "length": 10, "shots": 0, "accuracy": 0.02, "trials": 50},

