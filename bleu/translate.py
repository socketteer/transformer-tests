import os
from pprint import pprint
from recordclass import recordclass
from gpt3.bleu.util import read_file, json_create, json_append_dict, query

File = recordclass("File", "file language")
Test = recordclass("Test", "src target")


def openai_prompt(test, src_examples, tar_examples, src_line):
    if len(src_examples) == 0:
        return f"Q: What is the {test.target.language} translation of {src_line}\nA:"
    else:
        few_shots = "\n\n".join([
            f"{src}\t=\t{tar}"
            for src, tar in zip(src_examples, tar_examples)
        ])
        return f"Translate {test.src.language} to {test.target.language}:\n{few_shots}\n\n{src_line}\t="


def openai_quote_prompt(test, src_examples, tar_examples, src_line):
    if len(src_examples) == 0:
        return f"Q: What is the {test.target.language} translation of \"{src_line}\"\nA: \""
    else:
        p = lambda src, tar: f"\"{src}\" = \"{tar}\""
        few_shots = "\n\n".join([
            p(src, tar)
            for src, tar in zip(src_examples, tar_examples)
        ])
        return (f"Translate {test.src.language} to {test.target.language}:"
                f"\n{few_shots}"
                f"\n\n\"{src_line}\" = \"")
    # quote_symb = '"' if '"' not in src_line else "'"
    # if quote_symb in src_line:
    #     print(f"WARNING: Src has quote symbol {quote_symb}:\n{src_line}")
    # return (f"Q: What is the {test.target.language} translation of"
    #         f" {quote_symb}{src_line}{quote_symb}"
    #         f"\nA: {quote_symb}")


def simple_prompt(test, src_examples, tar_examples, src_line):
    few_shots = "\n\n".join([f"{test.src.language}: {src}\n{test.target.language}: {tar}" for src, tar in zip(src_examples, tar_examples)])
    few_shots = few_shots + "\n\n" if len(src_examples) > 0 else ""
    return f"{few_shots}{test.src.language}: {src_line}\n{test.target.language}:"


def button_prompt(test, src_examples, tar_examples, src_line):
    assert len(src_examples) == 0
    return (f"The {test.src.language} sentence on the screen reads \"{src_line}\""
            f"\nI click the button labeled Translate to {test.target.language},"
            f" and the flawless {test.target.language} translation appears: \"")


def help_forum_prompt(test, src_examples, tar_examples, src_line):
    assert len(src_examples) == 0
    return (f"How do I translate this {test.src.language} phrase to {test.target.language}?"
            f" Google translate seems to be wrong."
            f"\n\"{src_line}\""
            f"\n\nHello! Happy to help. I'm a native {test.src.language} and {test.target.language} speaker."
            f"I would translate the phrase as: \"")


def native_speaker_prompt(test, src_examples, tar_examples, src_line):
    assert len(src_examples) == 0
    return (
        f"Amatuer {test.src.language} to {test.target.language} translators often make simple mistakes due to their"
        f" inexperience with the intricacies and idioms of each language. The best translators are often native"
        f" speakers of both {test.src.language} and {test.target.language}. Their skill allows them to go beyond"
        f" translating text literally. Instead, they translate the true meaning of the phrase."
        f"\n\nFor example, consider the following phrase: \"{src_line}\""
        f"\nA masterful translator would correctly translate the phrase: \""
    )


def translator_prompt(test, src_examples, tar_examples, src_line):
    assert len(src_examples) == 0
    return (f"A {test.src.language} phrase is provided: \"{src_line}\""
            f"\nThe masterful {test.src.language} translator flawlessly translates the phrase"
            f" into {test.target.language}: \"")


def create_prompt(test, src_examples, tar_examples, src_line, prompt_style):
    prompt_funcs = {
        "openai": openai_prompt,
        "openai_in_quotes": openai_quote_prompt,
        "simple": simple_prompt,
        "button": button_prompt,
        "translator": translator_prompt,
        "help_forum": help_forum_prompt,
        "native_speaker": native_speaker_prompt,
    }
    return prompt_funcs[prompt_style](test, src_examples, tar_examples, src_line)



def translate(test, shots, engine="ada", prompt_style="openai", start_index=0, output_file=None, debug=True):
    if output_file and start_index == 0:
        if os.path.isfile(output_file):
            if not input(f"Delete and replace {output_file}?\nEnter any key to continue"):
                return
        json_create(output_file)

    src_lines = read_file(test.src.file)
    tar_lines = read_file(test.target.file)

    early_src_examples = src_lines[:shots]
    early_tar_examples = tar_lines[:shots]
    late_src_examples = src_lines[-shots:]
    late_tar_examples = tar_lines[-shots:]

    src_lines = src_lines[start_index:]
    tar_lines = tar_lines[start_index:]

    if debug:
        src_lines = src_lines[:5]
        tar_lines = tar_lines[:5]
    results = []

    for i, (src_line, tar_line) in enumerate(zip(src_lines, tar_lines)):
        i = i+start_index

        src_examples = late_src_examples if i <= shots else early_src_examples
        tar_examples = late_tar_examples if i <= shots else early_tar_examples
        if shots > 0:
            assert len(src_examples) == shots
            prompt = create_prompt(test, src_examples, tar_examples, src_line, prompt_style)
        else:
            prompt = create_prompt(test, [], [], src_line, prompt_style)
        response = query(prompt, engine)

        translated_line = response["choices"][0]["text"].strip("\"\'\n \t").replace("\n", " ")
        if response["choices"][0]["finish_reason"] != "stop":
            print(f'WARNING: Stopped because {response["choices"][0]["finish_reason"]}')

        result = {
            "metadata": {
                "test": str(test),
                "engine": engine,
                "shots": shots,
                "prompt_style": prompt_style,
            },
            "index": i,
            "source": src_line,
            "target": tar_line,
            "prompt": prompt if len(prompt) < 1000 else "TOO LONG TO INCLUDE IN RESULTS DICT",
            "translation": translated_line,
        }

        if output_file:
            json_append_dict(output_file, result)
        results.append(result)


        pprint(result)
        print("\n\n")
        # print(f"Finished {i}/{len(src_lines)}:")
        # print(f"\tprompt: {prompt}")
        # print(f"\tsrc: {src_line}\n")
        # print(f"\ttar: {tar_line}\n")
        # print(f"\ttrans: {translated_line}\n")
        # print("\n\n")

    return results


def main():
    fr_en = Test(
        File("data/wmt14/fr-en.fr", "French"),
        File("data/wmt14/fr-en.en", "English")
    )

    test = fr_en

    engine = "curie"
    # shots = 1
    # prompt_style = "simple"

    runs = [
        # [0, "openai"],
        # [1, "openai_in_quotes"],
        [1, "simple"],
        [10, "simple"],
        # [10, "openai_in_quotes"],
        # [0, "translator"],
        # [0, "simple"],
        # [0, "button"],
        # [0, "openai_in_quotes"],
        # [10, "openai"],
    ]

    # for shots in [1, 10]:
    # for prompt_style in ["button", "help_forum", "native_speaker", "translator"]:
    for shots, prompt_style in runs:
        output_file = (
            f"data/results/"
            f"{test.src.file.split('data/')[-1].split('.')[0].replace('/', '-')}"
            f"--engine={engine}"
            f"--prompt={prompt_style}"
            f"--shots={shots}"
            f".json"
        )
        results = translate(test, shots=shots, engine=engine, prompt_style=prompt_style,
                            output_file=output_file, start_index=0, debug=False)
    return


if __name__ == "__main__":
    main()
    print("Done! :)")



