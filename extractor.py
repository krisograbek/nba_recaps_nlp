import spacy
import pyinflect
from spacy.matcher import Matcher
from collections import Counter

from helpers import (
    get_subj_text,
    get_pobjs_text
)

nlp = spacy.load('en_core_web_sm')


def merge_noun_chunks():
    if "merge_noun_chunks" not in nlp.pipe_names:
        nlp.add_pipe("merge_noun_chunks", last=True)
    if "merge_noun_chunks" in nlp.disabled:
        nlp.enable_pipe("merge_noun_chunks")


def get_streaks(text, starts):
    """
    Parameters
    ----------
    text : str
        The article text
    starts : list
        The list with indices of Tokens, that are
        at the beginning of sentences cantaining
        words "straight", "streak", or "consecutive"

    Returns
    -------
    sentences : a list of spacy Spans
        Sentences cantaining words "straight", "streak", or "consecutive"
    """
    doc = nlp(text)
    sentences = []
    for token in doc:
        if token.lower_ in ["straight", "streak", "consecutive"]:
            if token.sent.start not in starts:
                starts.append(token.sent.start)
                sentences.append(token.sent)

    print("Streaks. Found {} streak(s)".format(len(sentences)))
    return sentences


def get_records(text, starts):
    """
    Parameters
    ----------
    text : str
        The article text
    starts : list
        The list with indices of Tokens, that are
        at the beginning of sentences cantaining
        words "straight", "streak", or "consecutive"

    Returns
    -------
    sentences : a list of spacy Spans
        Sentences cantaining any kind of best or worst performance
        e.g. season-high, franchise best, career-low
    """
    doc = nlp(text)
    starts.append(0)
    sentences = [doc[0].sent]
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
    for match_id, start, end in matches:
        if doc[start].sent.start not in starts:
            sentences.append(doc[start].sent)
            starts.append(doc[start].sent.start)

    print("Records. Found {} record(s)".format(len(sentences)))
    # print(sentences)
    return sentences


def get_extracted_articles(filtered):
    """
    Parameters
    ----------
    filtered : str
        The sentences from all the articles after
        filtering with get_streaks()
    
    Returns
    -------
    extracted : list of tuples
        Each tuple contains a score, text extracted
        from sentences with streaks, and record sentences
    """
    merge_noun_chunks()
    extracted = []
    for art in filtered:
        streak_tokens = get_streak_tokens(art[1])
        text = streak_extractions(streak_tokens)
        extracted.append((art[0], text, art[2]))
    return extracted


def get_streak_tokens(sentences):
    """
    Parameters
    ----------
    sentences : str
        The sentences from all the articles after
        filtering with get_streaks()
    
    Returns
    -------
    streak_tokens : list of spacy Tokens
        Noun chunks containing one of words:
        straight, consecutive, streak
    """
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

    return streak_tokens


def streak_extractions(streak_tokens):
    """
    Parameters
    ----------
    streak_tokens : list of spacy Tokens
        Noun chunks containing one of words:
        straight, consecutive, streak
    
    Returns
    -------
    filtered_sents : list of str
        Text extracted from sentences with streaks
    """

    filtered_sents = []

    dobjs = [token for token in streak_tokens if token.dep_ in ["dobj", "nsubj"]]
    pobjs = [token for token in streak_tokens if token.dep_ in ["pobj"]]

    for token in pobjs:
        sent = handle_obj(token, True)
        if len(sent) > 0:
            filtered_sents.append(sent)

    for token in dobjs:
        sent = handle_obj(token)
        if len(sent) > 0:
            filtered_sents.append(sent)
    return filtered_sents


def handle_obj(token, is_pobj = False):
    """ Applies Information Extraction task using spacy. 
    It checks many conditions about sentences' dependency trees.
    
    Parameters
    ----------
    token : spacy Token
        Noun chunk containing one of words:
        straight, consecutive, streak
    is_pobj : Boolean
        A flag that is True if token.dep_ == "pobj"
    
    Returns
    -------
    ret_text : str
        Text extracted from sentences with streaks
    """
    ret_text = ""
    verb = token.head
    if is_pobj == True:
        prep = token.head
        verb = prep.head
        # if prep's head is not a verb, a pattern gets too complicated
        if verb.pos_ != "VERB":
            return ret_text

    # some sentences are complicated and they don't match with any pattern coverd here
    # In this case only the whole sentence will be shown
    if (verb.tag_ not in ["VBD", "VBN"]) and (verb.head.tag_ not in ["VBD", "VBN"]):
        # print(".........Pattern not covered")
        return ret_text

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

    # when token is a subject, we handle it differently
    if token.dep_ == "nsubj":
        print_text = [token.text, verb_text, right_info]
   
    if is_pobj == True:
        dobj_text = ""
        try:
            dobj = [child for child in verb.rights if child.dep_ == "dobj"][0]
            dobj_text = dobj.text
        except IndexError:
            pass
        print_text = [subj_text, verb_text, dobj_text, prep.text, token.text, right_info]
    for word in print_text:
        if len(word) > 0:
            ret_text += word + " "
    # print(*print_text)

    return ret_text
