import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="sample_collection")

collection.upsert(
    documents=[
        "This is a document about casino ",
        "This is a document about beach"
    ],
    ids=["id1", "id2"]
)

collection.upsert(
    documents=["Las Vegas is famous for its casinos"],
    ids=["id4"],
    metadatas=[{"category": "entertainment", "location": "Las Vegas"}]
)

results = collection.query(
    query_texts=["Tell me about casinos"],
    n_results=2,
    where={"category": "entertainment"}  
)

print(results)

stored_docs = collection.get()
print(f"Stored documents: \n{stored_docs}")