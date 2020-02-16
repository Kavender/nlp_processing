# coding: utf-8
"""Extract Named Entities from text with SpaCy model and pattern matching.
EntityRuler: matching one or more patterns of per-token attr:value pairs,
with optional quantity qualifiers.
Examples
---------
>>> from extractor import EntityExtractor
>>> from en_core_web_sm import load
>>> nlp = load()
>>> extractor.set_entity_rules([{"IS_DIGIT": True}, {"TAG": "CD"}], "SHORT_MONEY")
>>> extractor.set_entity_rules([{"IS_DIGIT": True}, {"TAG": "CD"}, {"TAG": "NNS"}], "PLURAL_NOUN")
>>> extractor.set_entity_patterns(['Q4'], 'DATE')
>>> entities = extractor.extract(sentence)
>>> print([(ent, ent.label_) for ent in entities])
[(Q4, 'DATE'), (Bank of America, 'ORG'), (23 million transactions, 'PLURAL_NOUN'), (7 billion, 'SHORT_MONEY'), (91 percent, 'PERCENT'), (the prior year, 'DATE')]
"""
from typing import Tuple, List, Dict, Iterable, Union
from extractor.base_extractor import BaseExtractor
from spacy.tokens import Doc, Span
from spacy.matcher import Matcher, PhraseMatcher
from spacy.pipeline import EntityRuler
from spacy.util import filter_spans


class EntityExtractor(BaseExtractor):
    """ Extract an ordered sequence of named entities (PERSON, ORG, LOC, etc.) from
    a ``Doc``, optionally filtering by entity types and frequencies"""


    def __init__(self, nlp, **kwargs) -> None:
        self.nlp = nlp
        self.ruler = EntityRuler(nlp, overwrite_ents=True)
        self.matcher = PhraseMatcher(nlp.vocab)

    def set_entity_patterns(self, patterns:Union[str, List[Dict[str, str]]], label: str):
        patterns = [self.nlp.make_doc(pattern) for pattern in patterns]
        self.matcher.add(label, None, *patterns)

    def set_entity_rules(self, patterns: Union[str, List[Dict[str, str]]], label: str):
        """e.g "pattern": "MyCorp Inc.", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]
        The EntityRuler lets you add spans to the `Doc.ents` using rules or exact phrase matches.
        It can be combined with the statistical `EntityRecognizer` to boost accuracy.
        """
        if isinstance(patterns, list):
            if all(isinstance(item, str) for item in patterns):
                pass
            elif all(isinstance(item, dict) for item in patterns):
                patterns = [patterns]
            else:
                raise TypeError(f"patterns={patterns} is invalid; values must be one of List[str] for List[dict]")
        else:
            raise TypeError(f"patterns={patterns} is invalid; values must be one of List[str] for List[dict]")
        patterns = [{"label": label, "pattern": pattern} for pattern in patterns]
        self.ruler.add_patterns(patterns)

    def entity_spans(self, doc: Doc, matched_ents: List[Tuple[int, int, int]]) -> List[Span]:
        entity_spans: List[Span] = []
        recognized_entities = list(doc.ents)
        for match_id, start, end in matched_ents:
            label = self.nlp.vocab.strings[match_id]
            entity = Span(doc, start, end, label=label)
            entity_spans.append(entity)
        entity_spans.extend(doc.ents)
        return filter_spans(entity_spans)

    def extract(self, text: str, on_match=None) -> List[Span]:
        """Extract entities with predefined patterns and consolidate with entities
        recognized by `ner` model if applicable, return entities recognized from
        modified pipeline.

        Parameters
        ----------
        doc : Doc
            Description of parameter `doc`.
        on_match : callable
            Callback function to act on matches.
            Takes the arguments ``matcher``, ``doc``, ``i`` and ``matches``..

        Returns
        -------
        List[Span]
            Recognized entities from `rule`, `ner`, `matcher` component.

        """
        if len(self.ruler) > 0:
            self.nlp.add_pipe(self.ruler)
        doc = self.nlp(text)
        matches = self.matcher(doc)
        entities = self.entity_spans(doc, matches)
        return entities
