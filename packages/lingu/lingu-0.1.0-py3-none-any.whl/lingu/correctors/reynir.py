from __future__ import unicode_literals
from reynir_correct.errtokenizer import TOK, CorrectToken, tokenize
from tokenizer import detokenize, split_into_sentences, normalized_text_from_tokens
from functools import partial



def gen(f):  # This yields a generator so we are not storing long texts in memory
    yield from f


def post_correct(text):
    """
    Function that uses Reynir-correct library to correct a text file
    :param txt:
    :return corr_text:
    """
    to_text = partial(detokenize, normalize=True)
    """ detokenize is a Utility function in Greynirs Tokenizer to convert an iterable of tokens back
                to a correctly spaced string. If normalize is True,
                punctuation is normalized before assembling the string. """
    # Initialize sentence accumulator list
    curr_sent = []  # type: List[CorrectToken]
    corr_text = ""
    corr_text_lis = list()
    # Normal shallow parse, one line per sentence,
    # tokens separated by spaces
    for t in tokenize(text):
        if t.kind in TOK.END:
            # End of sentence/paragraph
            if curr_sent:
                #print(to_text(curr_sent))
                corr_text_lis.append(to_text(curr_sent))
                print(TOK.END)
                #corr_text_lis.append(t.kind)
                #print(corr_text)
                curr_sent = []

        else:
            curr_sent.append(t)
    #print("Here we are")
    #print(to_text(curr_sent))
    print(corr_text_lis)
    corr_text = " ".join(corr_text_lis)
    print(curr_sent)
    corr_text += " ".join(to_text(curr_sent))# if curr_sent else ""
    print(corr_text)

    return corr_text
