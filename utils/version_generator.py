
from collections import Counter
import re
import time
from numpy import mean, random
from operator import itemgetter 
from utils.nltk_utils import get_word_synsets
from utils.stopwords import NLPStopwords



class VersionGeneration:

	def __init__(self, base_words, version_id=None, language='English'):
		self.base_words = base_words
		self.stopwords = NLPStopwords(language)
		self.version_id = str(int(time.time())) if version_id is None else version_id

	def generate_version(self):
		candidate_words = self.expand_to_synets(topN=10)
		scored_candiates = [word for word, _ in self.scoring(candidate_words)]
		num_lower, num_upper = min(len(scored_candiates), 3), min(len(scored_candiates), 5)
		rand_version_name = "_".join(random.choice(scored_candiates, 
												   random.randint(num_lower, num_upper),
										 		   replace=True))
		return f'{rand_version_name}_{self.version_id}'

	def expand_to_synets(self, topN: int):
		more_words = Counter(self.base_words)
		for word in self.base_words:
			word_synet = get_topic_domains(word, use_definition=True, stopwords=self.stopwords)
			more_words += word_synet
		return more_words.most_common(topN)


	def scoring(self, word_counts):
		word2scores = []
		for word, count in word_counts:
			length_score = self._score_word_length(word)
			vowel2cons_ratio = self._cal_vowel_to_consonant_ratio(word)
			avg_score = mean([vowel2cons_ratio, length_score])
			word2scores.append((word, count*avg_score))
		return sorted(word2scores, key=itemgetter(1, 0), reverse=[True, False])

	@staticmethod
	def _cal_vowel_to_consonant_ratio(word):
	    if not word or len(word) == 0:
	        return 0
	    word = re.sub(r'[^a-zA-Z0-9]', '', word)
	    re_vowels = re.compile(r'[a|e|i|o|u]')
	    re_cons = re.compile(r'[^a|e|i|o|u]')
	    vowels = float(len(re.findall(re_vowels, word)))
	    consonants = float(len(re.findall(re_cons, word)))
	    if vowels is 0.0 or consonants is 0.0:
	        return 0
	    if vowels < consonants:
	        return vowels / consonants
	    else:
	        return consonants / vowels  

	@staticmethod
	def _score_word_length(word) -> float:
	    """Rule of thumb, we prefer medium length of words, normally between 8-15
	    """
	    if not word or len(word) == 0:
	        return 0
	    word_length = len(word)
	    if word_length > 20:
	        return 0.1
	    elif word_length > 15 and word_length <= 20:
	        return 0.25
	    elif word_length <= 4:
	        return 0.5
	    elif word_length >= 10 and word_length <= 15:
	        return 0.75
	    else:
	        return 1.0



