from nltk.metrics.distance import edit_distance
from icegrams import Ngrams
from reynir.bindb import BIN_Db
from tokenizer import split_into_sentences, correct_spaces
from string import punctuation
from tokenizer.abbrev import Abbreviations


# Initialize classes
ng = Ngrams()
db = BIN_Db()
ab = Abbreviations()

# Minimum probability of a candidate other than the original
# word in order for it to be returned
MIN_LOG_PROBABILITY = -16.5
# Unigrams need to be above this probability threshold
UNIGRAM_ACCEPT_THRESHOLD = -12.0


def has_numbers(inp):
    """
    Function returns True if any character in the input string is a digit
    :param inp: str
    :return: True/False
    """
    return any(char.isdigit() for char in inp)


def word_exists_in_bin(word):
    """
    Function to loopup icelandic word in the BÍN dictionary.
    The word can be some form of inflection
    :param word: single word from the text
    :return: True/False
    """
    word = word.strip(punctuation)
    word = word.strip("0123456789")
    if word == "":
        return True
    sw = db.lookup_word(word)
    if sw[1]:
        return True
    return False


def get_min_ed(ng_arr, word):
    """
    Get the minimum edit distance
    :param ng_arr: list of possible ngrams
    :param word: the original/incorrect word from the text
    :return: original word or the suggestion with minimum edit distance
    """
    ed_d = dict()
    for ngw in ng_arr:
        # Gets the edit distance number by Levenshtein distance
        ed = edit_distance(ngw[0], word)
        if ed == 1:  # Return the first candidate with 1 edit distance
            return ngw[0]
        # Appends the (word successor, E.d. number) to a list
        ed_d.update({ngw[0]: [ed, ngw[1]]})
    w_res = min(ed_d, key=lambda x: ed_d[x][0])
    w_prob = ed_d[w_res][1]
    if w_prob < MIN_LOG_PROBABILITY:
        return word
    return w_res


def find_successors(word, ngwords, nr_of_successors):
    """
    Finds a successor if it is plausible or it returns the original word
    :param word: Original word from the text
    :param ngwords: The 1 or two previous words used to find a possible successor
    :param nr_of_successors: How many ngram successors should come into consideration
    :return: The word with minimum edit distance if plausible, else original word
    """
    # Gets the n propable successors
    ng_arr = ng.succ(nr_of_successors, *ngwords)

    if ng_arr:
        # start_m = 100
        return get_min_ed(ng_arr, word)
    return word


def check_abbrev(word):
    """Checks the Icelandic tokenizer if word is a common abbreviations"""
    if ab.has_meaning(word):
        return True
    return False


def ngram_word_filter(words, nr_of_successors):
    """
    Function that decides if a word should be searched for ngrams,
    Start by iterating over each word in a sentance, then:
    1. Checks if it has numbers, does not change the word.
    2. Checks if the word is a common unigram, does not change it.
    3. Checks if it exists in the BÍN dictionary, does not change it.
    4. Checks if it is an icelandic abbreviation.
    5. Looks up ngram suggestions for the word.
    :param words: list of word strings from a single sentence
    :param nr_of_successors: int, how many possible ngram successors should we look up
    :return: Returns the words as a string
    """
    words_f = list()
    for word in words:
        # If it has numbers we keep it
        if has_numbers(word):
            words_f.append(word)
        else:
            # Check if word is a common unigram
            w_log_prob = ng.logprob(word)
            if w_log_prob > UNIGRAM_ACCEPT_THRESHOLD:
                words_f.append(word)
            elif not word_exists_in_bin(word):  # If it does not exists in icelandic dictionary
                # Check if it is an icelandic abbreviation
                if check_abbrev(word):
                    words_f.append(word)
                elif words_f:
                    # Find the ngrams for the word
                    words_f.append(find_successors(word, words_f[-2:], nr_of_successors))
                else:  # If it is a first word in a sentence ngrams has no relevance
                    words_f.append(word)
            else:  # Defensive programming else clause
                words_f.append(word)

    return " ".join(words_f)


def ngrams_correct(text, nr_of_successors=10):
    """This ngrams function uses shallow tokenization for text.
    Splits sentences into words to find ngrams.
    Iterates through these sentences to possibly find ngrams"""

    if not text:
        return ""
    if " " not in text:  # No point if only one word
        return text

    # Put only sentences into ngrams
    sentences = split_into_sentences(text)
    corrected_s = list()
    for s in sentences:
        words = s.split(" ")
        tmp = ngram_word_filter(words, nr_of_successors)
        corrected_s.append(correct_spaces(tmp))

    res = " ".join(corrected_s)
    return res
