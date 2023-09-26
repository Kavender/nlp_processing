import unittest
from typing import List
from nlp_utils.tokenizer import NLTKSplitter


# Define a test class that inherits from unittest.TestCase
class NLTKSplitterTestCase(unittest.TestCase):
    def setUp(self):
        # Create an instance of the NLTKSplitter class
        self.splitter = NLTKSplitter()

    def test_split_words_with_empty_sentence(self):
        # Test with an empty sentence
        sentence = ""
        expected_tokens = []
        
        actual_tokens = self.splitter.split_words(sentence)
        
        self.assertEqual(actual_tokens, expected_tokens)

    def test_split_words_with_single_word(self):
        # Test with a single word sentence
        sentence = "Hello"
        expected_tokens = ["Hello"]
        
        actual_tokens = self.splitter.split_words(sentence)
        
        self.assertEqual(actual_tokens, expected_tokens)

    def test_split_words_with_multiple_words(self):
        # Test with a sentence containing multiple words
        sentence = "Hello world! How are you?"
        expected_tokens = ["Hello", "world", "!", "How", "are", "you", "?"]
        
        actual_tokens = self.splitter.split_words(sentence)
        
        self.assertEqual(actual_tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()