import datetime

from flask import Flask, render_template, request
import hashlib
import random
import json
from markov import return_final_string

app = Flask(__name__)

speech_words = [
    "nonono"
    # "liam should be locked up",
    # "penisman penisman penisman penisman penisman penisman penisman penisman penisman penisman penisman penisman",
    # "chairs can be good or they can be sharp",
    # "the elementary school never expected the principal",
]

speech_words_hash = [hashlib.sha1(i.encode("utf-8")).hexdigest() for i in speech_words]

with open("first_word_corpus.json", "r") as first_word_corpus_file:
    with open("word_dict.json", "r") as word_dict_file:
        first_word_corpus = json.load(first_word_corpus_file)
        word_dict = json.load(word_dict_file)


@app.route("/")
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    speech = random.choice(speech_words)
    generated = return_final_string(first_word_corpus, word_dict)

    if bool(random.getrandbits(1)):
        text1 = speech
        text2 = generated
    else:
        text1 = generated
        text2 = speech

    return render_template(
        "index.html",
        text_1=text1.capitalize(),
        text_2=text2.capitalize(),
        hash1=hashlib.sha1(text1.encode("utf-8")).hexdigest(),
        hash2=hashlib.sha1(text2.encode("utf-8")).hexdigest(),
    )


def random_confetti_options():
    options = {
        "startVelocity": random.randint(55, 75),
        "particleCount": random.randint(60, 90),
        "disableForReducedMotion": True,
        "gravity": random.uniform(0.7, 1.3),
    }
    origin_angle_options = [
        {
            "origin": {"x": 0.5, "y": 1},
            "angle": random.randint(80, 100),
            "spread": random.randint(40, 60),
        },
        {
            "origin": {"x": 1, "y": 1},
            "angle": random.randint(120, 150),
            "spread": random.randint(40, 60),
        },
        {
            "origin": {"x": 0, "y": 1},
            "angle": random.randint(33, 60),
            "spread": random.randint(40, 60),
        },
    ]
    options.update(random.choice(origin_angle_options))
    return options


@app.route("/answerValidation")
def answer_validation():
    """:returns correct when the returned hash is from the speech list, otherwise returns incorrect"""
    button_no = request.args.get("button")
    button_hash = request.args.get("textHash")
    print(button_hash)
    confetti_options = random_confetti_options()
    print(confetti_options)
    if button_hash in speech_words_hash:
        print("Status: correct")
        return {"status": "correct", "confetti": confetti_options}
    print("Status: incorrect")
    return {"status": "incorrect", "confetti": confetti_options}


@app.route("/newQuestion")
def new_question():
    speech = random.choice(speech_words)
    generated = return_generated_str()

    if bool(random.getrandbits(1)):
        response = {"text1": speech, "text2": generated}

    else:
        response = {"text1": generated, "text2": speech}

    return response


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
