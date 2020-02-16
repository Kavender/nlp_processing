# coding: utf-8
from __future__ import unicode_literals
from nltk.corpus import stopwords

class NLPStopwords:

    def __init__(self, language: str='English'):
        self.stopwords = set(stopwords.words(language))

    def add_stopword(self, *args):
        """
        This function is used to add new stopwords
        to the predefined list
        Parameters - ["new_stopword"]
        ------------------------------
        Example -
        obj = NLPStopwords()
        obj.add_stopword(["first_word", "second_word"])
        """
        if self.remove_stopwords is False:
            raise Exception("Please enable removal of stopwords")
        if type(args) != list:
            raise Exception("Error - pass stopwords in list")
        for arg in args:
            self.stopwords.add(arg)


    def remove_stopwords(self, *args):
        """
        This function is used to remove stopwords from predefined list
        Parameters - ["first_word"]
        ------------------------------
        Example
        obj = NLPStopwords()
        obj.remove_stopwords(['new_stopword_here'])
        """
        if self.remove_stopwords is False:
            raise Exception("Error - enable stopword removal functionality")
        if type(args) != list:
            raise Exception("Error - expected a list")
        if args == []:
            raise Exception("Error - no items to remove from stopword list")
        for arg in args:
            if arg in self.stopwords:
                self.stopwords.remove(arg)
            else:
                raise Exception(arg+" not in list")
