from .reynir import reynir_correct
from .ngrams import ngrams_correct


def correct(text, **corrector_opt):
    """
    Function for postprocessing OCR errors
    :param text: The text string from the OCR engine
    :param corrector_opt: Dictionary for corrector options:
    -ngrams_nr_of_succ: how many possible successors to search for
    :return:
    """

    if corrector_opt.get('ngrams'):
        if corrector_opt.get('ngrams') is True:
            if corrector_opt.get('ngrams_nr_of_succ'):
                text = ngrams_correct(text, corrector_opt['ngrams_nr_of_succ'])
            else:
                text = ngrams_correct(text)
    if corrector_opt.get('reynir'):
        if corrector_opt['reynir'] is True:
            text = reynir_correct(text)


    return text
