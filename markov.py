import numpy as np
import json
import language_check
from textstat.textstat import textstat

text=""
with open('transcriptsClean.json') as data_file:
    data = json.load(data_file)
    i = 0
    for item in data:
        #print(item)
        text = text + " " + item["transcriptText"]

corpus = text.split()



def isReadable(checkedOutput):
    textstat.set_lang('en')
    score = textstat.text_standard(checkedOutput, float_output=True)
    if score > 6:
        print(checkedOutput)
        print(score)
    else:
        print(score)
        makeString()

 

def check_output(output):
    tool = language_check.LanguageTool('en-GB')
    matches = tool.check(output)
    checkedOutput = language_check.correct(output, matches)
    #print(matches)
    #print (checkedOutput)
    isReadable(checkedOutput)

def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])
pairs = make_pairs(corpus)

word_dict = {}
for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]
def makeString():
    first_word = np.random.choice(corpus)

    while first_word.islower():
        first_word = np.random.choice(corpus)

    chain = [first_word]

    n_words = 100

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    output=' '.join(chain)
    output = output.replace('&#8217;',"'")
    output = output.replace('&#8220;','')
    output = output.replace('&#8221;','')
    output = output.replace('&#8230;','!')

    #print(output)
    check_output(output)

print("making string...")
makeString()
