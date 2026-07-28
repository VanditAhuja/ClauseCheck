from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    """
    Convert text into an embedding vector.
    """

    embedding = model.encode(text)

    return embedding


def similarity_score(text1, text2):
    """
    Compare two text strings using cosine similarity.
    """

    embedding1 = create_embedding(text1)

    embedding2 = create_embedding(text2)

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )

    return float(similarity[0][0])