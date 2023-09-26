import pytest
from extractor.entity_extractor import EntityExtractor
from en_core_web_sm import load

nlp = load()
sent_text1 = (u"In Q4 alone , Bank of America processed over 23 million transactions , totaling nearly $ 7 billion "
", up 91 percent from the prior year .")
entities1 = ["Bank of America", "23 million", "$ 7 billion", "91 percent", "prior year"]


@pytest.mark.parametrize("sentence, expected", [(sent_text1, entities1)])
def extract_entity_from_sentence(sentence, expected):
    extractor = EntityExtractor(nlp)
    entities = extractor.extract(sentence)
    assert len(entities) == len(expected)
    assert all([ent.text in expected for ent in entities])
