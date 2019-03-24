import os
from lxml.cssselect import CSSSelector
from lxml import html
import utils
import unicodedata
import string
import re

def read_sentence(path):
    with open(path, "r") as file:
        doc = html.fromstring("".join(file.readlines()))
    phrases = []
    for el in doc.cssselect(".DocumentPage-content p"):
        phrases.append(format_phrase(el.text_content()))
    return filter_phrases(phrases)

re_punctua = re.compile('[%s\n€]' % re.escape(string.punctuation))
re_numbers = re.compile('[0-9]')

def filter_phrases(phrases):
    return filter(lambda p: len(p.split(" ")) > 2, phrases)

def format_phrase(phrase):
    phrase = strip_accents(phrase.lower())
    phrase = re_punctua.sub(' ', phrase)
    phrase = re_numbers.sub(' ', phrase)
    words = phrase.split()
    words = map(lambda a: "flsn" if a in ["fl", "fls"] else a, words)
    words = map(lambda a: "artn" if a in ["art", "arts"] else a, words)
    words = filter(lambda a: len(a) > 2, words)
    return " ".join(words)

def strip_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def generate(input_path, output_path):
    with open(output_path, "w") as output:
        for file_path in utils.list_files(input_path):
            print(file_path)
            for phrase in read_sentence(file_path):
                output.write(phrase + "\n")

if __name__ == "__main__":
    generate(
        "data/sentences",
        "data/phrases.csv"
    )