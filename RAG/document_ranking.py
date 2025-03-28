from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
import numpy as np

client = QdrantClient(host="localhost", port=6333)

client.recreate_collection(
    collection_name="sample_collection",
    vectors_config=VectorParams(
        size=384, 
        distance=Distance.COSINE,  
    )
)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

documents = [
    "This is a document about machine learning.",
    "This is a document about artificial intelligence.",
    "This is a document about deep learning."
]

embeddings = model.encode(documents).tolist()

for i, embedding in enumerate(embeddings):
    client.upsert(
        collection_name="sample_collection",
        points=[
            {"id": i, "vector": embedding, "payload": {"content": documents[i]}}
        ]
    )

print("Documents inserted successfully!")

query = "Tell me about deep learning."
query_embedding = model.encode([query]).tolist()[0]

results = client.search(
    collection_name="sample_collection",
    query_vector=query_embedding,
    limit=3 
)

for result in results:
    print(f"Document ID: {result.id}, Content: {result.payload['content']}, Score: {result.score}")