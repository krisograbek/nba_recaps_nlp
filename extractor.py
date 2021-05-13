import spacy
import pyinflect
from spacy.matcher import Matcher
from collections import Counter

from helpers import (
    get_subj_text,
    get_pobjs_text
)

nlp = spacy.load('en_core_web_sm')


def get_streaks(text, sentences, starts):
    doc = nlp(text)
    counter = 0
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
    sents = []
    for match_id, start, end in matches:
        if doc[start].sent.start not in starts:
            sents.append(doc[start].sent.text)
            sentences.append(doc[start].sent)
            starts.append(doc[start].sent.start)
        else:
            print("Here's a sentence")
            print(doc[start].sent)
    print("Records. Found {} record(s)".format(len(sents)))
    print(starts)


def extract_sentences(text, sentences, starts):
    get_records(text, sentences, starts)
    get_streaks(text, sentences, starts)


def get_filtered_articles(extracted):
    try:
        nlp.add_pipe("merge_entities", after="ner")
        nlp.add_pipe("merge_noun_chunks", last=True)
    except ValueError:
        print("Pipes already there")
    for art in extracted:
        print(art[0])
        streak_tokens = get_streak_tokens(art[1])
        for token in streak_tokens:
            print(token.text)

def get_streak_tokens(sentences):
    doc = nlp(sentences)

    matcher = Matcher(nlp.vocab)
    pattern = [
        [
            {'TEXT': {'REGEX': 'straight|consecutive|streak'}}
        ]
    ]

    matcher.add("streaks", pattern)
    matches = matcher(doc)

    streak_tokens = [doc[start] for _, start, _ in matches]
    streak_extractions(streak_tokens)
    return streak_tokens


def streak_extractions(streak_tokens):
    print("Total tokens: ", len(streak_tokens))

    dobjs = [token for token in streak_tokens if token.dep_ in ["dobj", "nsubj"]]
    pobjs = [token for token in streak_tokens if token.dep_ in ["pobj"]]

    p_counter = 0
    d_counter = 0

    for token in pobjs:
        if handle_obj(token, True) == True:
            p_counter += 1

    print("Counter {}/{}".format(p_counter, len(pobjs)))
    
    for token in dobjs:
        if handle_obj(token) == True:
            d_counter += 1
    print("Counter {}/{}".format(d_counter, len(dobjs)))
    print(" -_ "*20)

def handle_obj(token, is_pobj = False):
    verb = token.head
    if is_pobj == True:
        prep = token.head
        verb = prep.head
        # if prep's head is not a verb, a pattern gets too complicated
        if verb.pos_ != "VERB":
            return False
    # if current token is a subject, there is no need to run the whole code
    if token.dep_ == "nsubj":
        print_text = [token.text, verb.text]
        print(*print_text)
        return True

    # some sentences are complicated and they don't match with any pattern coverd here
    # In this case only the whole sentence will be shown
    if (verb.tag_ not in ["VBD", "VBN"]) and (verb.head.tag_ not in ["VBD", "VBN"]):
        # print(".........Pattern not covered")
        return False

    # get the subject's text
    # Note: It may be an empty string
    subj_text = get_subj_text(verb)
    
    verb_text = verb.text
    # verbs in past tense look more natural
    if verb.tag_ != "VBD":
        verb_text =  verb._.inflect('VBD')

    # add more info if there is a prep child for the token
    right_info = get_pobjs_text(token, verb)

    # array to print the extracted sentence
    print_text = [subj_text, verb_text, token.text, right_info]
    if is_pobj == True:
        dobj_text = ""
        try:
            dobj = [child for child in verb.rights if child.dep_ == "dobj"][0]
            dobj_text = dobj.text
        except IndexError:
            pass
        print_text = [subj_text, verb_text, dobj_text, prep.text, token.text, right_info]
    print(*print_text)

    return True
