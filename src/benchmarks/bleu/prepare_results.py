import os
from pprint import pprint

from gpt3.bleu.util import read_file, json_open



def prepare_translation_file(src_file, result_file, translation_file):
    src_lines = read_file(src_file)
    results = json_open(result_file)

    if len(src_lines) != len(results):
        ids = [r["index"] for r in results]
        print(set(range(len(src_lines))) - set(ids))
        for j, i in enumerate(ids):
            if i != j:
                print("AHHHH", i, j)
    assert len(src_lines) == len(results), f"Len mismatch {len(src_lines)} != {len(results)}"
    for src_line, result_src_line in zip(src_lines, [r["source"] for r in results]):
        assert src_line == result_src_line, f"Src mismatch {src_line} != {result_src_line}"

    trans_lines = [r["translation"] for r in results]
    if trans_lines[-1] == "":
        trans_lines[-1] = "."

    with open(translation_file, 'w') as f:
        f.write("\n".join(trans_lines))



def score_translations(translation_file):
    print(translation_file)
    os.system(f"cat {translation_file} | sacrebleu -t wmt14 -l fr-en --short")
    print("\n")

def main():
    results_folder = "data/results/"
    src_file = "data/wmt14/fr-en.fr"

    results_files = [f for f in os.listdir(results_folder) if os.path.isfile(os.path.join(results_folder, f))]
    results_files = sorted([results_folder + f for f in results_files])
    translation_files = [
        f"{os.path.dirname(f)}/translations/{os.path.basename(f).split('.')[0]}.trans"
        for f in results_files
    ]

    for result_file, translation_file in zip(results_files, translation_files):
        if "curie" not in result_file:
            continue
        try:
            prepare_translation_file(src_file, result_file, translation_file)
            score_translations(translation_file)
        except Exception as e:
            print(f"FAIL {result_file} {str(e)}\n\n")
            continue


    # results_file = "data/results/wmt14-fr-en--engine=ada--prompt=openai--shots=0.json"
    # prepare_translation_file(src_file, results_file)
    #
    # translation_filename =

    # To calculate score, run this from the bleu dir
    # cat data/results/FILENAME.trans | sacrebleu -t wmt14 -l fr-en
    # scores are bleu4 unigram/bigram/trigram/4gram (modified) precision scores



    # OpenAI Models:  Small Med Large XL    2.7B 6.7B 13B 175B

    ########
    # 0 Shot
    #########
    # OpenAI's score for each model: 2.29 2.99 3.90 3.60    21.2 15.5 22.4 21.9


    # data/results/wmt14-fr-en--engine=babbage--prompt=openai--shots=0.trans
    # 7.1 23.3/8.7/4.8/2.9 (BP = 0.980 ratio = 0.980 hyp_len = 69323 ref_len = 70708)


    ########
    # 1 Shot
    #########
    # OpenAI's score for each model:  1.50 16.3 24.4 27.0     30.0 31.6 31.4 35.6

    # data/results/wmt14-fr-en--engine=babbage--prompt=openai--shots=1.trans
    # 21.8 58.0/31.8/20.1/13.1 (BP = 0.825 ratio = 0.839 hyp_len = 59296 ref_len = 70708)


    ########
    # 10 Shot
    #########
    # OpenAI's score for each model [64 shot]:  5.30 26.2 29.5 32.2    35.1 36.4 38.3 41.4

    # data/results/wmt14-fr-en--engine=babbage--prompt=openai--shots=10.trans
    # 25.1 60.7/34.4/21.8/14.3 (BP = 0.884 ratio = 0.890 hyp_len = 62933 ref_len = 70708)


if __name__ == "__main__":
    main()


# {
#     "metadata": {
#         "test": "Test(src=File(file='data/wmt14/fr-en.fr', language='French'), target=File(file='data/wmt14/fr-en.en', language='English'))",
#         "engine": "babbage",
#         "shots": 10
#     },
#     "index": 1599,
#     "source": "Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir.",
#     "target": "For more than a year, I have been noticing the strong dissatisfaction of people I meet everywhere: the horrendous revaluation of their properties, a deluge of taxes, the costs of all sorts of permits, endless administrative fees, etc.",
#     "translation": "Since more than a year, I am in a position to observe a strong discontentment among the people I meet: a monstrous revaluation of their property, a flood of taxes, a cost of all kinds, administrative costs to the point of exhaustion."
# },

# The French sentence on the screen reads,
# I click the button labeled Translate to English, and the English translation appears:

# The French phrase is:
# The masterful French translator translates the phrase into English:

# "Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir."


# Original French: "Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir."
# Perfect translation to English:

# French: Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir.
# English:
# Since a year ago, everywhere I go, I am very tired of the people I meet: a monstrous evaluation of their properties, a huge tax burden, a flood of permits, and so on.



# The original French phrase: Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir.
# The perfect English translation by a native speaker:
#
#
# Amatuer French to English translators often make simple mistakes due to their inexperience with the intricacies and idioms of each language. The best translators are often native speakers of both French and English. Their skill allows them to go beyond translating text literally. Instead, they translate the true meaning of the phrase.
#
# For example, consider the following phrase: "Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir."
# A masterful translator would correctly translate in a way that an English speaker would recognize as a natural English phrase: "For more than a year, everywhere I go, I am struck by the strong dissatisfaction of the people I meet: monstrous revaluation of their properties, deluge of taxes, cost of permits of all kinds, endless administrative fees."
#
#
# Original French phrase: Depuis plus d'un an, partout, je suis \u00e0 m\u00eame de constater un fort m\u00e9contentement de la part des gens que je rencontre: r\u00e9\u00e9valuation monstrueuse de leurs propri\u00e9t\u00e9s, d\u00e9luge de taxes, co\u00fbt des permis de toutes sortes, frais administratifs \u00e0 n'en plus finir.
# Correct translation of the French phrase in English:





# Press button
# The French sentence on the screen reads, ""Depuis plus d'un an, partout, je suis à même de constater un fort mécontentement de la part des gens que je rencontre: réévaluation monstrueuse de leurs propriétés, déluge de taxes, coût des permis de toutes sortes, frais administratifs à n'en plus finir."
# I click the button labeled Translate to English, and the flawless English translation appears: "Since more than one year, everywhere, I am able to observe a great dissatisfaction of the people I meet: a monstrous revaluation of their properties, a deluge of taxes, a flood of fees, a never-ending administrative cost."


# Native speakers
# Amatuer French to English translators often make simple mistakes due to their inexperience with the intricacies and idioms of each language. The best translators are often native speakers of both French and English. Their skill allows them to go beyond translating text literally. Instead, they translate the true meaning of the phrase.
#
# For example, consider the following phrase: "Depuis plus d'un an, partout, je suis à même de constater un fort mécontentement de la part des gens que je rencontre: réévaluation monstrueuse de leurs propriétés, déluge de taxes, coût des permis de toutes sortes, frais administratifs à n'en plus finir."
# A masterful translator would correctly translate the phrase: ""Since more than one year, everywhere, I am able to observe a great discontentment of the people I meet: a monstrous revaluation of their properties, a deluge of taxes, a flood of fees, a never-ending administrative cost."


