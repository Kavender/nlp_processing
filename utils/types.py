from collections import namedtuple
from spacy.tokens import Token

# define a Word type
Word = namedtuple('Word', ['sentnum', 'wordnum', 'token'])

Phrase = namedtuple('Phrase', ['text', 'text_lemma', 'words', 'lemmas', 'pos', 'start', 'end'])

# define a Phrase type--> modify the following to a namedupe type? or List of Word type
