import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="contracts"
)

def store_chunks(chunks, embeddings):
    existing = collection.get()
    if existing and existing.get("ids"):
        collection.delete(ids=existing["ids"])

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[str(index)],
            documents=[chunk],
            embeddings=[embedding.tolist()]
        )

def search_similar(query_embedding, top_k=3):
    results = collection.query(

        query_embeddings=[query_embedding.tolist()],

        n_results=top_k

    )
    return results["documents"][0]