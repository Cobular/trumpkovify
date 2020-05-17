import numpy as np
import json
import language_check
from textstat.textstat import textstat


def make_corpus() -> list:
    """
    Generates a corpus of text using the transcriptsClean.json file in the same directory

    :return: The corpus, a list of all used words in order
    """
    text = ""
    with open("transcriptsClean.json") as data_file:
        text_input = json.load(data_file)
        for line in text_input:
            text = text + " " + line["transcriptText"]

    corpus = text.split()
    return corpus


def make_word_dict(corpus: str) -> dict:
    """
    Takes in a corpus (list of words) and returns a word frequency dictionary

    :param corpus: An ordered word list, generated by the make_corpus() function
    :return: A dictionary of word frequencies
    """
    pairs = [(corpus[i], corpus[i + 1]) for i in range(len(corpus) - 1)]

    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    return word_dict


def make_first_words(corpus: str) -> list:
    """
    Makes a list of words at the start of sentences

    :param corpus: A list of all words
    :return: A list of all words at the start of sentences.
    """
    start_words = ""
    for i, word in enumerate(corpus):
        if "." in corpus[i - 1]:
            start_words = start_words + " " + corpus[i]

    return start_words.split()


def _is_readable(phrase: str) -> bool:
    """
    Checks if a given phrase is readable
    :param phrase: The string to check
    :return: True if readable, false if not
    """
    textstat.set_lang("en")
    score = textstat.text_standard(phrase, float_output=True)
    if score > 6:
        return True
    else:
        return False


def _make_string(first_words, word_dict) -> str:
    """
    Generates a string from the pre-created models. No checking here.

    :param first_words: List of first words to start sentences
    :param word_dict: Word frequency dictionary
    :return: A generated, unfiltered, and unchecked string
    """
    first_word = np.random.choice(first_words)

    chain = [first_word]

    n_words = 100

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    output = " ".join(chain)
    output = output.replace("&#8217;", "'")
    output = output.replace("&#8220;", "")
    output = output.replace("&#8221;", "")
    output = output.replace("&#8230;", "!")

    return output


def return_generated_string(first_word_corpus: str, word_dict: dict) -> str:
    output = _make_string(first_word_corpus, word_dict)

    if "." or "!" or "?" in output:
        output = output.split(".")
        output = ".".join(output[:-1]) + "."
    else:
        return_generated_string(first_word_corpus, word_dict)

    tool = language_check.LanguageTool("en-GB")
    matches = tool.check(output)
    checked_output = language_check.correct(output, matches)

    if _is_readable(checked_output):
        return checked_output
    else:
        return_generated_string(first_word_corpus, word_dict)


# with open("corpus.json", "w") as corpus_file:
#     corpus = make_corpus()
#     json.dump(corpus, corpus_file)

# with open("first_word_corpus.json", "w") as first_word_corpus_file:
#     with open("corpus.json", "r") as corpus_file:
#         corpus = json.load(corpus_file)
#         first_word_corpus = make_first_words(corpus)
#         json.dump(first_word_corpus, first_word_corpus_file)

# with open("word_dict.json", "w") as word_dict_file:
#     with open("corpus.json", "r") as corpus_file:
#         corpus = json.load(corpus_file)
#         word_dict = make_word_dict(corpus)
#         json.dump(word_dict, word_dict_file)


with open("first_word_corpus.json", "r") as first_word_corpus_file:
    with open("word_dict.json", "r") as word_dict_file:
        first_word_corpus = json.load(first_word_corpus_file)
        word_dict = json.load(word_dict_file)

        for i in range(10):
            str = return_generated_string(first_word_corpus, word_dict)
            # print(str)
