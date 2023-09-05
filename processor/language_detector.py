from abc import ABC, abstractmethod
from typing import List, Union
from dataclasses import dataclass
from pathlib import Path
import warnings
import re
import fasttext


@dataclass
class LangDetected:
    language: str
    score: float

INVALID_CHARS_TO_REMOVE = {'\u200b', '\u200c', '\u200d', '\xa0', '\u2061', '\u202f', '\u2062', '\u202c', '\u202d', '\u200e', '\u202e', '\u2060'}

class BaseLanguageDetector(ABC):
    """The Base LanguageDetector used for identify language with given confidence"""

    def __init__(
        self, default_language: str = "UNKNOWN",  default_score: float = 0.0,
    ):
        self.default_language = default_language
        self.default_score = default_score

    @abstractmethod
    def detect(self, text: str) -> List[LangDetected]:
        """Returns a list of upto three identified languages"""
        pass

    def detect_main_language(self, text: str) -> str:
        lang_names = self.detect(text)
        return lang_names[0].language if lang_names else self.default_language


def FasttextLanguageDetector(BaseLanguageDetector):

    def __init__(self, model_path: Union[str, Path]]):
        super().__init__()
        self.model = fasttext.load_model(model_path)
    
    @staticmethod
    def _clean_text(self, text: str) -> str:
        if '\n' in text:
            warnings.warn("The text contains newline characters Fasttext cannot handle.")
            text = text.replace('\n', ' ')
        text = text.encode("utf-8", errors='ignore').decode("utf-8")
        for char in INVALID_CHARS_TO_REMOVE:
            if char in text:
                text = text.replace(char, ' ')
        # This line removes removes non-ASCII characters.
        return re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    @staticmethod
    def _get_lang(self, label: str, confidence: float) -> LangDetected:
        lang_code = self.default_language
        if confidence > self.threshold:
            lang_code = label.replace("__label__", "")
        if lang_code == "unk":  # Original code of FastText model for unknonw:
            lang_code = self.default_language
        return LangDetected(language=lang_code, score=confidence)

    def detect(self, text: str, *args, **kwargs) -> List[LangDetected]:
        text = self._clean_text(text)
        predictions, scores = self.model.predict(text, *args, **kwargs)
        lang_detected = [self._get_lang(label, confidence) for label, confidence in zip(predictions, scores)]
        return lang_detected
    


