# coding: utf-8
from typing import List, Tuple, Iterable
from spacy.tokens import Token, Span, Doc
from itertools import chain
from collections import defaultdict
import string
import networkx as nx
from math import floor
from nltk.metrics.distance import edit_distance
from extractor.base_extractor import BaseExtractor
from utils.constants import BRACKET_ESCAPES
from utils.stopwords import NLPStopwords
from utils.types import Word, Phrase
from utils.misc import overlap_items, consecutive


class PhraseExtractor(BaseExtractor):
    """Abstract base class from which all NPExtractor classes inherit. Implement an ``extract(text)`` method to return
    a list of noun phrases.
    Follow TextRank algorithm to build a graph that represent the text. A graph based ranking algorithm is used to
    extract phrase that are most important in the text. Nodes are words of certain part-of-speech (nouns and adjectives)
    and edges represent occurrence of nodes (of span), controlled by two layer distance between nodes (window_layer=2).
    Nodes are ranked by TextRank graph-based ranking algorithm with the depth of tree as weight.
    """

    def __init__(self, nlp, **kwargs) -> None:
        self.nlp = nlp
        self.stop_words = NLPStopwords().stopwords
        self.valid_tags = {"NN", "NNS", "NNP", "NNPS", "JJ", "JJS"}  # 'VBG', 'IN'
        self.graph = nx.Graph()
        # self.weights = {} #Weight container (can be either word or candidate weights)

    def extract(self, text: str, window=3, normalize=False, top_percent=None, topN=10):
        """Return a list of noun phrases (strings) for a body of text."""
        doc = self.nlp(text)
        nodes = [
            (Word(sent_id, token.i, token), token.tag_ in self.valid_tags)
            for sent_id, sent in enumerate(doc.sents)
            for token in sent
        ]
        weighted_keywords = self.get_keywords_orderby_rank_score(nodes, window, normalize)
        # combined keywords into phrase and get the weighted sum to rerank
        keyphrases = self.get_combined_keywords(doc, window, normalize)
        # compute the number of top keywords
        if top_percent is not None:
            num_nodes = self.graph.number_of_nodes()
            topN = int(min(floor(num_nodes * top_percent), num_nodes))
        return keyphrases

    def get_keywords_orderby_rank_score(self, nodes: List[Tuple[Word, bool]], window: int, normalize: bool):
        # build sentence word graph
        self.build_weighted_undirected_word_graph(nodes, window=window, normalize=normalize)
        # compute pagerank score
        weighted_scores = nx.pagerank(self.graph, alpha=0.85, tol=0.0001, weight="weight")
        keywords = sorted(weighted_scores, key=weighted_scores.get, reverse=True)
        return keywords

    def build_weighted_undirected_word_graph(self, nodes: List[Tuple[Word, bool]], window: int, normalize: bool):
        # add nodes to the graph
        node_stat = lambda tok: tok.lemma_ if normalize else tok.text
        dict_attr = defaultdict(list)
        for node, is_valid in nodes:
            if is_valid:
                dict_attr[node_stat(node.token)].append(node.wordnum)
        self.graph.add_nodes_from(dict_attr.keys())
        nx.set_node_attributes(self.graph, values=dict_attr, name="wordnum")
        # add edge to the graph
        for i, (node, is_valid) in enumerate(nodes):
            node_token = node.token
            if not is_valid:
                continue
            start = max([abs(i - window), node_token.left_edge.i])
            end = min([i + window, len(nodes), node_token.right_edge.i + 1])
            for j in range(start, end):
                neighbor_node, is_neighbor_valid = nodes[j]
                neighbor_token = neighbor_node.token
                distance = self.calculate_dependency_distance(node_token, neighbor_token, normalize)
                if is_neighbor_valid and node != neighbor_node:
                    self.graph.add_edge(node_stat(node_token), node_stat(neighbor_token), weight=distance)

    def calculate_dependency_distance(self, token: Token, neighbor_token: Token, normalize: bool) -> int:
        if normalize:
            distance = edit_distance(token.lemma_, neighbor_token.lemma_)
        else:
            distance = edit_distance(token.text, neighbor_token.text)
        return distance

    def get_combined_keywords(self, doc: Doc, window, normalize):
        phrases = []
        for component in sorted(nx.connected_components(self.graph), key=len, reverse=True):
            component_wordnum = sum([self.graph.nodes[node]["wordnum"] for node in component], [])
            if len(component) > 1:
                for pos_range in consecutive(sorted(component_wordnum), stepsize=window):
                    multigram = self.build_phrase(doc, min(pos_range), max(pos_range) + 1)
                    phrases.append(multigram)
            else:
                # to improve on the edge case, could rebuld the graph again with different valid criteria
                for word_num in component_wordnum:
                    unigram = self.build_phrase(doc, word_num, word_num + 1)
                    phrases.append(unigram)
        # filter out noisy case, such as `JJ` only or stopwords only
        filtered_phrases = self.candidate_filtering(
            phrases, stoplist=list(self.stop_words) + list(string.punctuation) + list(BRACKET_ESCAPES.keys())
        )
        return filtered_phrases

    def candidate_filtering(
        self,
        candidates: Iterable[Phrase],
        stoplist=None,
        minimum_length=3,
        maximum_ngrams=5,
        valid_punctuation_marks="-",
        only_alphanum=True,
        pos_blacklist=None,
    ):
        stop_list = [] if stoplist is None else stoplist
        stop_pos = [] if pos_blacklist is None else pos_blacklist
        for candidate in candidates:
            # discard if words are in the stoplist
            if (candidate.text in self.stop_words) or (candidate.text_lemma in self.stop_words):
                del candidate
            elif not overlap_items(candidate.pos, {"NN", "NNS", "NNP", "NNPS"}):
                del candidate
            # discard if tags are in the pos_blacklist
            elif overlap_items(candidate.pos, stop_pos):
                del candidate
            # discard candidates composed of 1-2 characters
            elif len("".join(candidate.words)) < minimum_length:
                del candidate
            # discard candidates composed of more than 5 words
            elif len(candidate.words) > maximum_ngrams:
                del candidate
            # discard if not containing only alpha-numeric characters
            elif only_alphanum and not all([self._is_alphanum(w, valid_punctuation_marks) for w in candidate.words]):
                del candidate
        return candidates

    @staticmethod
    def _is_alphanum(word: str, valid_punctuation_marks="-"):
        """Check if a word is valid, i.e. it contains only alpha-numeric
        characters and valid punctuation marks.
        Args:
            word (string): a word.
            valid_punctuation_marks (str): punctuation marks that are valid
                    for a candidate, defaults to '-'.
        """
        for punct in valid_punctuation_marks.split():
            word = word.replace(punct, "")
        return word.isalnum()

    @staticmethod
    def build_phrase(doc: Doc, start: int, end: int) -> Phrase:
        tokens = doc[start:end]
        words = [tok.text for tok in tokens]
        lemmas = [tok.lemma_ for tok in tokens]
        lst_pos = [tok.tag_ for tok in tokens]
        phrase_text = " ".join(words).replace("  '", "'")
        phrase_lemma = " ".join(lemmas).replace("  '", "'")
        return Phrase(phrase_text, phrase_lemma, words, lemmas, lst_pos, start, end)
