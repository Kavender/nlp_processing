from gensim.downloader import api


def load_gensim_embedding(model_name="glove-wiki-gigaword-200"):
    """Load gensim model word embeddings.
        Return:
        wv_from_bin: Word embeddings from model loaded.
    """
    wv_from_bin = api.load(model_name)
    print(f"Loaded {model_name} with vocab size {len(wv_from_bin.vocab)}")
    return wv_from_bin
