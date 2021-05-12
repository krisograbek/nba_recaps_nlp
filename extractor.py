import spacy
import pyinflect
from spacy import displacy
from spacy.matcher import Matcher, DependencyMatcher
from collections import Counter

nlp = spacy.load('en_core_web_sm')



def get_streaks(text, sentences, starts):
    doc = nlp(text)
    counter = 0
    # starts = []
    # print("Looking for the streaks")
    for token in doc:
        if token.lower_ in ["straight", "streak", "consecutive"]:
            if token.sent.start not in starts:
                counter += 1
                starts.append(token.sent.start)
                sentences.append(token.sent)

    print("Streaks. Found {} streak(s)".format(counter))
    print(starts)


def get_records(text, sentences, starts):
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    pattern = [
            [
                {"ORTH": {"IN": ["career", "season", "franchise"]}},
                {"ORTH": "-", "OP": "?"}, 
                {"ORTH": {"IN": ["best", "high", "worst", "low", "record"]}}
            ]
    ]
    matcher.add("records", pattern)
    matches = matcher(doc)
    # print(len(matches))
    sents = []
    # starts = []
    for match_id, start, end in matches:
        if doc[start].sent.start not in starts:
            sents.append(doc[start].sent.text)
            sentences.append(doc[start].sent)
            starts.append(doc[start].sent.start)
        else:
            print("Here's a sentence")
            print(doc[start].sent)
            # print(type(doc[start:end][0].sent.text[:-1]), "streaks")
        # print(type(doc[start:end][0].sent.text))
    print("Records. Found {} record(s)".format(len(sents)))
    # print(sents)
    print(starts)
    # for sent in sents:
    #     print(sent)

def extract_stats(text, sentences, starts):
    get_streaks(text, sentences, starts)
    get_records(text, sentences, starts)