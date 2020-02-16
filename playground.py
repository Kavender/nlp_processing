from extractor.entity_extractor import EntityExtractor
from en_core_web_sm import load
nlp = load()
sent_text1 = u"In Q4 alone , Bank of America processed over 23 million transactions , totaling nearly $ 7 billion , up 91 percent from the prior year ."
entities1 = ['Bank of America', '23 million', '$ 7 billion', '91 percent', 'prior year']

def extract_entity_from_sentence(sentence):
    extractor = EntityExtractor(nlp)
    extractor.set_entity_rules([{"IS_DIGIT": True}, {"TAG": "CD"}], "SHORT_MONEY")
    extractor.set_entity_rules([{"IS_DIGIT": True}, {"TAG": "CD"}, {"TAG": "NNS"}], "PLURAL_NOUN")
    extractor.set_entity_patterns(['Q4'], 'DATE')
    return extractor.extract(sentence)



if __name__ == "__main__":
    entities = extract_entity_from_sentence(sent_text1)
    print([(ent, ent.label_) for ent in entities])
