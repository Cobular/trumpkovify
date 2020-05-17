import numpy as np
import json
import language_check
from textstat.textstat import textstat


def is_readable(checked_output):
    textstat.set_lang("en")
    score = textstat.text_standard(checked_output, float_output=True)
    if score > 6:
        print(checked_output)
        print(score)
    else:
        print(score)
        make_string()


def check_output(output):
    tool = language_check.LanguageTool("en-GB")
    matches = tool.check(output)
    checked_output = language_check.correct(output, matches)
    # print(matches)
    # print (checked_output)
    is_readable(checked_output)


def make_pairs(corpus):
    for i in range(len(corpus) - 1):
        yield corpus[i], corpus[i + 1]


def make_string():
    first_word = np.random.choice(corpus)

    while first_word.islower():
        first_word = np.random.choice(corpus)

    chain = [first_word]

    n_words = 100

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    output = " ".join(chain)
    output = output.replace("&#8217;", "'")
    output = output.replace("&#8220;", "")
    output = output.replace("&#8221;", "")
    output = output.replace("&#8230;", "!")

    # print(output)
    check_output(output)


text = ""
with open("transcriptsClean.json") as data_file:
    data = json.load(data_file)
    i = 0
    for item in data:
        # print(item)
        text = text + " " + item["transcriptText"]

corpus = text.split()

pairs = make_pairs(corpus)

word_dict = {}
for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]

print("making string...")
make_string()
