import nltk
from nltk.corpus import wordnet as wordNet


def get_lemma(word):
    lemma = wordNet.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
def get_word_synsets(word):
    return wordNet.synsets(word, pos=None)


def filter_stopwords(words, stopwords):
    return filter(lambda x: x.lower() not in stopwords, words)


def get_topic_domains(synsets, use_definition=False, stopwords=[]):
    results = []
    for _synset in synsets:
        results.extend(filter_stopwords(_synset.lemma_names(), stopwords))
        results.extend(filter_stopwords(_synset.definition().split(), stopwords))
    return Counter(results)