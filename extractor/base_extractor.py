from abc import ABCMeta, abstractmethod

class BaseExtractor(metaclass=ABCMeta):
    """Abstract base class from which all NPExtractor classes inherit.
    Descendant classes must implement an ``extract(text)`` method
    that returns a list of noun phrases as strings.
    """
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def extract(self, text):
        """Return a list of noun phrases (strings) for a body of text."""
        raise NotImplementedError
