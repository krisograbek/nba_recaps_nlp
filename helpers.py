import os
import pickle
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")


def store_pickle(articles, fname):
    fdir = "pickle_files"
    fpath = os.path.join(fdir, fname)
    with open(fpath, 'wb') as f:
        pickle.dump(articles, f)


def load_pickle(fname):
    fdir = "pickle_files"
    fpath = os.path.join(fdir, fname)
    with open(fpath, 'rb') as f:
        articles = pickle.load(f)
    return articles

def filter_out_upper(text):
    if isinstance(text, list):
        text = " ".join([sent.text for sent in text])
    doc = nlp(text)
    pattern = [
        [
            {"IS_UPPER": True, "IS_SENT_START": True}, 
            {"IS_UPPER": True, "OP": "?"}, 
            {"TEXT": "--"},
            {"TEXT": {"IN": ["—", "-"]}},
        ],
        [
            {"IS_UPPER": True, "IS_SENT_START": True}, 
            {"IS_UPPER": True, "OP": "?"}, 
            {"TEXT": ","}, 
            {"TAG": "NNP"}, 
            {"TEXT": "--"},
            {"TEXT": {"IN": ["—", "-"]}},
        ],
        [
            {"TEXT": "TIP"},
            {"TEXT": "-"},
            {"TEXT": "INS"},
        ],
    ]

    matcher = Matcher(nlp.vocab)
    matcher.add("uppers", pattern)

    sents = [sent for sent in doc.sents]
    new_sents = []
    for sent in sents:
        matches = matcher(sent)
        if len(matches) > 0:
            match_id, start, end = matches[0]
            # print(sent[start:end].text)
            new_sents.append(sent[end:].text)
            continue
        new_sents.append(sent.text)

    text = " ".join([sent for sent in new_sents])

    return text

