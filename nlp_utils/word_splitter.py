from typing import List
import re
import jieba
from overrides import overrides
from nltk import word_tokenizer
from commom.types import Token, WordToken
from nlp_utils.spacy_utils import get_spacy_model


class WordSplitter:
    """
    A ``WordSplitter`` splits strings into words.
    """

    def split_words(self, sentence: str) -> List[WordToken]:
        """
        Splits ``sentence`` into a list of :class:`Token` objects.
        """
        raise NotImplementedError

    def batch_split_words(self, sentences: List[str]) -> List[List[WordToken]]:
        """
        Spacy needs to do batch processing, or it can be really slow.  This method lets you take
        advantage of that if you want.  Default implementation is to just iterate of the sentences
        and call ``split_words``, but the ``SpacyWordSplitter`` will actually do batched
        processing.
        """
        return [self.split_words(sentence) for sentence in sentences]


class WhiteSpaceSplitter(WordSplitter):
    """
    A ``WordSplitter`` that simply split the input string on whitespace and return the token list.
    """

    @overrides
    def split_words(self, sentence: str) -> List[WordToken]:
        return [token for token in sentence.split()]


class NLTKSplitter(WordSplitter):
    @overrides
    def split_words(self, sentence: str) -> List[WordToken]:
        return [token for token in word_tokenizer(sentence)]


class SpacyWordSplitter(WordSplitter):
    """
    A ``WordSplitter`` that uses spaCy's tokenizer.
    """

    def __init__(
        self,
        language: str = "english",
        lang_model: str = "en_core_web_sm",
        disabled: List[str] = None,
        keep_spacy_tokens: bool = False,
    ) -> None:
        self.nlp = get_spacy_model(language, disabled)

    def _sanitize(self, tokens: List[Token]) -> List[WordToken]:
        if self._keep_spacy_tokens:
            return tokens
        else:
            return [token.text for token in tokens]

    @overrides
    def batch_split_words(self, sentences: List[str]) -> List[List[WordToken]]:
        return [self._sanitize(tokens) for tokens in self.nlp.pipe(sentences, n_threads=-1)]

    @overrides
    def split_words(self, sentence: str) -> List[WordToken]:
        return self._sanitize(self.nlp(sentence))


def CamelCaseSplitter(WordSplitter):
    """
    A ``WordSplitter`` that split on CamelCase, e.g. 'AI100', 'WageWorkers', 'NewYork'
    """

    @overrides
    def split_words(self, sentence: str) -> List[WordToken]:
        sentence = re.sub("([A-Z0-9]+)", r" \1", sentence)
        sentence = re.sub("([A-Z0-9][a-z]+)", r" \1", sentence)
        sentence = re.sub("([A-Z]+)([0-9]+)", r" \1 \2", sentence)
        sentence = re.sub("([0-9]+)([A-Z]+)", r" \1 \2", sentence)
        return sentence.split()


def MultiLanguageSplitter(WordSplitter):
    """
    A ``WordSplitter`` that split on multilangual case, e.g. '腾讯Group', 'City银行'
      TODO: consider using stanfordnlp/spacy lib with multi-lingual models/tokenizer.
    """

    @overrides
    def split_words(self, sentence: str) -> List[WordToken]:
        tokens = []
        ascii_tokens = []
        splitted = False
        multilingual_tokens = jieba.lcut(sentence)
        for tok in multilingual_tokens:
            if not tok or tok.isspace():
                continue
            elif tok.isascii() and (not splitted):
                ascii_tokens.append(tok)
                splitted = False
            else:
                if ascii_tokens:
                    tokens.append("".join(ascii_tokens))
                    ascii_tokens = []
                    splitted = True
                tokens.append(tok)
        return tokens
