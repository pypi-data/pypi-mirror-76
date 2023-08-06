from reynir_correct import tokenize
from reynir_correct import main
from reynir_correct import Correct_TOK

from reynir_correct.errtokenizer import TOK, CorrectToken, Error, tokenize
from tokenizer import Tok, detokenize, normalized_text_from_tokens
from functools import partial

#from reynir_correct.spelling import correct

# Fyrir reyni correct væri kannski best að senda á main fallið
# eða kópera það einhvernveginn.


def gen(f): # This yields a generator so we are not storing long texts in memory
    yield from f
    # TODO: send in one word or a part of a lowercase sentance


def is_oneword(txt):
    """
    Takes the txt and
    figures out if it is a one word
    :param txt:
    :return txt:
    """
    if " " in txt:
        return False
    return True


def correct_word(word):
    s = tokenize(word)


def spell_check(txt="t2.txt"):
    txt = txt.strip()

    # May put in here if there are some erroneous letters
    if is_oneword(txt):
        if not txt[0].isupper():
            txt[0] = txt[0].upper()
        return correct_word(txt)
    for t in tokenize(gen(txt)):
        print(t.txt)


def spell_check_neat(txt):

    to_text = partial(detokenize, normalize=True)
    """ detokenize is a Utility function in Greynir to convert an iterable of tokens back
                to a correctly spaced string. If normalize is True,
                punctuation is normalized before assembling the string. """
    # Initialize sentence accumulator list
    curr_sent = []  # type: List[CorrectToken]
    # Normal shallow parse, one line per sentence,
    # tokens separated by spaces
    for t in tokenize(gen(txt)):
        if t.kind in TOK.END:
            # End of sentence/paragraph
            if curr_sent:
                print(to_text(curr_sent))
                curr_sent = []

        else:
            curr_sent.append(t)

    if curr_sent:
        print(to_text(curr_sent))