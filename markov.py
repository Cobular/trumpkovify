import numpy as np
import json
import language_check
from textstat.textstat import textstat
import re
from collections import Counter
from typing import List
from random import choices


def make_corpus() -> list:
    """
    Generates a corpus of text using the transcriptsClean.json file in the same directory

    :return: The corpus, a list of all used words in order
    """
    text = ""
    with open("transcriptsClean.json") as data_file:
        text_input = json.load(data_file)
        for speech in text_input:
            text = text + " " + speech["transcriptText"]

    corpus = text.split()
    return corpus


def make_word_dict(corpus: list) -> dict:
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


def make_word_dict_adv(corpus: list, num_words_back: int) -> dict:
    """
    Takes in a corpus (list of words) and returns a word frequency dictionary, allows to specify the number of words back to look.

    Word frequency dictionaries consist of a list of words that appear in the text as the key, and the value as a list
     of all the words that come later and their number of occurances, which can be used as weights to select a next word
     in the chain.

    :param num_words_back: The number of words back to make this dictionary
    :param corpus: An ordered word list, generated by the make_corpus() function
    :return: A dictionary of word frequencies
    """
    pairs = [(corpus[i], corpus[i + num_words_back]) for i in range(len(corpus) - num_words_back)]

    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    word_dict_out = {}
    for word, occurrences in word_dict.items():
        # Counts and normalizes the word dicts to make math easier
        occurrences_counted = Counter(occurrences)
        total = sum(occurrences_counted.values(), 0.0)
        for key in occurrences_counted:
            occurrences_counted[key] /= total
        word_dict_out[word] = dict(occurrences_counted)

    return word_dict_out


def recursive_combination_func(main_dict, list_of_dicts_to_add, count=0) -> dict:
    """
        Combines the main dict with list_of_dicts_to_add

    """
    # print(count)
    if len(list_of_dicts_to_add) == 0:
        return main_dict
    for key, value in main_dict.items():
        if key in list_of_dicts_to_add[0].keys():
            main_dict[key] *= list_of_dicts_to_add[0][key]
    list_of_dicts_to_add = list_of_dicts_to_add[1:]
    return recursive_combination_func(main_dict, list_of_dicts_to_add, count+1)


def combine_word_dict(word_dict_entry_list: list) -> dict:
    """
    Combines multiple word dictionary elements following a specific logic.

    Input should be a list of word dict entries (the lists that are the values for any word in a word dict)
     for the current chain

    First, take all items from the first dict entry in the input list and add them to new_list, as all should have a chance of appearing.
    Then, for each further back word dict entry, add the items from there to new_list that exist in the first entry.
    TODO: Tune the weight on 'adding' items to new_list, maybe some curve is needed.
    Repeat this until you get one combined dict that covers all the given dicts.

    This might be just making real sentences at some point, need to be careful


    :param word_dict_entry_list: The list of all word dict elements to combine. Must be in order, closest (1) to furthest.
     Should look like this:
     word_dict_entry_list
       L word_dict_entry: dict{word: dict{str: int}, word: dict{str: int}, word: dict{str: int}, ...}
       L word_dict_entry: dict{word: dict{str: int}, word: dict{str: int}, word: dict{str: int}, ...}
       L word_dict_entry: dict{word: dict{str: int}, word: dict{str: int}, word: dict{str: int}, ...}
       L word_dict_entry: dict{word: dict{str: int}, word: dict{str: int}, word: dict{str: int}, ...}
       ...
     where str is a choice as the next word in the chain and int is the relative probability of that occurring
    :return: One SuperList TM that is the un-normalized probabilities of each event occurring
    """
    new_dict = word_dict_entry_list[0]
    [print(f"{len(word_dict_entry_list)}.{i+1}+++ {test_dict}") for i, test_dict in enumerate(word_dict_entry_list)]

    if len(word_dict_entry_list) == 1:
        return new_dict

    # Creates a
    clean_word_dict_entry_list = [{k: v for k, v in word_dict_entry.items() if k in new_dict} for word_dict_entry in
                                  word_dict_entry_list[1:]]

    fin_word_dict = recursive_combination_func(new_dict, clean_word_dict_entry_list)
    print(f"{len(word_dict_entry_list)} +++ {fin_word_dict}")
    print(f"{len(word_dict_entry_list)} +++ {new_dict}")

    return fin_word_dict


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


def _make_string(first_words, word_dict_list) -> str:
    """
    Generates a string from the pre-created models. No checking here.

    :param first_words: List of first words to start sentences
    :param word_dict_list: List of word frequency dictionaries, should be in order of closest to furthest
    :return: A generated, unfiltered, and unchecked string
    """
    first_word = np.random.choice(first_words)

    chain = [first_word]

    n_words = 25

    # Picks words to form the chain.
    for i in range(n_words):
        # A list of all word dict entries relevant for the selection of the next word
        # Can be any length, dependant on the number of word dicts and current chain length
        specific_word_dict_list = []
        for num, word_dict in enumerate(word_dict_list):
            # If the current word dict is for distance less than or equal to the length of the chain
            # Then append the specific word from that word dict to the specific word list
            if num + 1 <= len(chain):
                # Num starts at zero, reverse list starts at -1
                index: int = -(num + 1)
                specific_word_dict_list.append(word_dict[str(chain[index])])
        combined_dicts: dict = combine_word_dict(specific_word_dict_list)

        chain.append(choices(list(combined_dicts.keys()), weights=list(combined_dicts.values()))[0])
        # chain.append(str(np.random.choice(list(combined_dicts.keys()), 1, p=list(combined_dicts.values()))))
        # chain.append(np.random.choice(word_dict[chain[-1]]))

    output = " ".join(chain)
    output = output.replace("&#8217;", "'")
    output = output.replace("&#8220;", "")
    output = output.replace("&#8221;", "")
    output = output.replace("&#8230;", "!")

    return output


def return_final_string(first_word_corpus: str, word_dict: dict) -> str:
    output = _make_string(first_word_corpus, word_dict)

    if "." or "!" or "?" in output:
        output = re.split(r"\.|!|\?,", output)
        output = output[0] + "."
    else:
        return return_final_string(first_word_corpus, word_dict)

    tool = language_check.LanguageTool("en-GB")
    matches = tool.check(output)
    checked_output = language_check.correct(output, matches)

    if _is_readable(checked_output):
        return checked_output
    else:
        return return_final_string(first_word_corpus, word_dict)


def _setup_corpi(num_word_dicts: int):
    with open("corpus.json", "w") as corpus_file:
        corpus = make_corpus()
        json.dump(corpus, corpus_file)

    with open("first_word_corpus.json", "w") as first_word_corpus_file:
        with open("corpus.json", "r") as corpus_file:
            corpus = json.load(corpus_file)
            first_word_corpus = make_first_words(corpus)
            json.dump(first_word_corpus, first_word_corpus_file)

    with open("corpus.json", "r") as corpus_file:
        corpus = json.load(corpus_file)
        for i in range(num_word_dicts):
            i += 1
            with open(f"word_dict_{i}.json", "w") as word_dict_file:
                word_dict = make_word_dict_adv(corpus, i)
                json.dump(word_dict, word_dict_file)


if __name__ == '__main__':
    # _setup_corpi(7)
    #
    #     with open("word_dict.json", "r") as word_dict_file:
    #         first_word_corpus = json.load(first_word_corpus_file)
    #         word_dict = json.load(word_dict_file)
    #
    #         for i in range(100):
    #             string = return_final_string(first_word_corpus, word_dict)
    #             print(string)

    with open("first_word_corpus.json", "r") as first_word_corpus_file:
        first_word_corpus = json.load(first_word_corpus_file)
        filenames = ["word_dict_1.json", "word_dict_2.json", "word_dict_3.json", "word_dict_4.json", "word_dict_5.json",
                     "word_dict_6.json", "word_dict_7.json"]
        filedata = {filename: open(filename) for filename in filenames}
        list_of_filedata = [json.load(file) for name, file in filedata.items()]
        print(_make_string(first_word_corpus, list_of_filedata))
        # print(filedata)
