from extractor.entity_extractor import EntityExtractor
from extractor.phrase_extractor import PhraseExtractor
from en_core_web_sm import load
from pprint import pprint
import networkx as nx
nlp = load()

sent_text = u"Uber CEO Dara Khosrowshahi disclosed a massive data breach that affected 57 million riders and drivers back in 2016 ."
sent_text1 = u"In Q4 alone , Bank of America processed over 23 million transactions , totaling nearly $ 7 billion , up 91 percent from the prior year ."
sent_text2 = u"Beltone Amaze provides the longest battery life available on the market -- 24 hours of use when streaming 50 percent of the time and 30 hours of use without streaming.The rechargeable solution is so easy and intuitive that 9 out of 10 users will start using the system without instructions ."
sent_text3 = "In the 18 months since Lore joined Walmart after selling his company , Jet.com , to the retailer for $3.3 billion , e-commerce sales sky-rocketed ."
entities1 = ['Bank of America', '23 million', '$ 7 billion', '91 percent', 'prior year']

def extract_entity_from_sentence(sentence):
    extractor = EntityExtractor(nlp)
    extractor.set_entity_rules([{"IS_DIGIT": True}, {"TAG": "CD"}], "SHORT_MONEY")
    extractor.set_entity_rules([{"IS_DIGIT": True}, {"TAG": "CD"}, {"TAG": "NNS"}], "PLURAL_NOUN")
    extractor.set_entity_patterns(['Q4'], 'DATE')
    return extractor.extract(sentence)


def extract_keywords(sentence):
    extractor = PhraseExtractor(nlp)
    return extractor.extract(sentence)


if __name__ == "__main__":
    combined_text = " ".join([sent_text, sent_text1, sent_text2, sent_text3])
    entities = extract_entity_from_sentence(sent_text1)
    print([(ent, ent.label_) for ent in entities])
    print("-----")

    phrases = extract_keywords(combined_text)
    for phrase in phrases:
        print(phrase.text)
