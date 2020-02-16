# coding: utf-8
from .base_extractor import BaseExtractor

class PhraseExtractor(BaseExtractor):
    """Abstract base class from which all NPExtractor classes inherit.
    Descendant classes must implement an ``extract(text)`` method
    that returns a list of noun phrases as strings.
    """

    @abstractmethod
    def extract(self, text):
        """Return a list of noun phrases (strings) for a body of text."""
        return
