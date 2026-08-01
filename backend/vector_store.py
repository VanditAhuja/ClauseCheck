from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_vectorizer = None
_matrix = None
_chunks = []

def store_chunks(chunks):
    global _vectorizer, _matrix, _chunks
    _chunks = chunks
    _vectorizer = TfidfVectorizer().fit(chunks)
    _matrix = _vectorizer.transform(chunks)

def search_similar(question, top_k=3):
    global _vectorizer, _matrix, _chunks
    if _vectorizer is None:
        return []
    query_vec = _vectorizer.transform([question])
    sims = cosine_similarity(query_vec, _matrix)[0]
    top_indices = sims.argsort()[-top_k:][::-1]
    return [_chunks[i] for i in top_indices]