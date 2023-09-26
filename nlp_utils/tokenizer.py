# coding: utf-8
from __future__ import unicode_literals
from typing import List, Optional
from nlp_utils.normalize import remove_punctuation, expand_contractions
from common.types import WordToken


class WordTokenizer:
    """A `WordTokenizer` split strings into words and adding leading or trailing tokens.
        Post-processing (e.g. filtering, stemming, remove stopwords) are left outside of tokenizer.
    """

    def __init__(
        self,
        word_splitter,
        start_tokens: Optional[List[WordToken]] = None,
        end_tokens: Optional[List[WordToken]] = None,
    ):
        self._word_splitter = word_splitter
        self._start_tokens = start_tokens or []
        # We reverse the tokens here because we're going to insert them with `insert(0)` later;
        # this makes sure they show up in the right order.
        self._start_tokens.reverse()
        self._end_tokens = end_tokens or []

    @classmethod
    def tokenize(self, text: str, with_contraction: bool = False, with_punc: bool = True) -> List[WordToken]:
        """
        with_punc: (optional) whether to include punctuation as separate tokens.
        with_contraction: (optional) whether to replace contraction words into
                    multigrams before tokenizing.
        Returns: list of word tokens.
        """
        if with_contraction:
            # TODO: not yet implemented
            text = expand_contractions(text)
        tokens = self._word_splitter.split_words(text)
        return self._sanitize(tokens, with_punc)

    def _sanitize(self, tokens: List[str], with_punc: bool = False) -> List[WordToken]:
        if not with_punc:
            tokens = [
                word if word.startswith("'") else remove_punctuation(word)
                for word in tokens
                if remove_punctuation(word)
            ]
        for start_token in self._start_tokens:
            tokens.insert(0, start_token)
        for end_token in self._end_tokens:
            tokens.append(end_token)
        return tokens

    @classmethod
    def batch_tokenize(self, texts: List[str]) -> List[List[WordToken]]:
        return [self.tokenize(text) for text in texts]
