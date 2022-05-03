# coding: utf-8
from spacy.tokens import Token, Span, Doc
from spacy.language import Language as SpacyModelType
from spacy.cli.download import download as spacy_download


def get_spacy_model(spacy_model_name: str,  pipeline_disabled=["vectors", "textcat"]):
    try:
        import spacy
        spacy_model = spacy.load(spacy_model_name, disable=pipeline_disabled)
    except (ImportError, OSError) as e:
        logger.error('spaCy is not installed or the model is unavailale.')
        spacy_download(spacy_model_name)
        # Import the downloaded model module directly and load from there
        spacy_model_module = __import__(spacy_model_name)
        spacy_model = spacy_model_module.load(disable=disable)
    return spacy_model




def is_alphanum(token: Token, valid_punctuation_marks='-') -> bool:
    """Check whether token contains only alpha-numeric characters and valid punctuation. Expand from spacy's
    `Token.is_digit` and `Token.is_alpha` attributes.

    Parameters
    ----------
    token : Token
        One item of Doc object, representing a word, punctuation symbol, whitespace, etc.
    valid_punctuation_marks : type
        Punctuation marks that are valid for a candidate, defaults to '-'.

    Returns
    -------
    bool
        Return true when token contains only only alpha-numeric
        characters and valid punctuation, otherwise, return False.
    """
    for punct in valid_punctuation_marks.split():
        word = token.lemma_.replace(punct, '')
    return word.isalnum()
