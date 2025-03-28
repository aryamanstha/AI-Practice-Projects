from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import numpy as np

client = QdrantClient("http://localhost:6333")

collection_name = "sample_collection"

if not client.collection_exists(collection_name):
    client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )
    print(f"Collection '{collection_name}' created successfully!")
else:
    print(f"Collection '{collection_name}' already exists!")
vector_data = [
    (0, [0.1, 0.2, 0.3, 0.4], "A", "Vector 0 - Category A"),
    (1, [0.5, 0.6, 0.7, 0.8], "B", "Vector 1 - Category B"),
    (2, [0.9, 0.1, 0.2, 0.3], "C", "Vector 2 - Category C"),
    (3, [0.4, 0.5, 0.6, 0.7], "D", "Vector 3 - Category D"),
    (4, [0.8, 0.9, 0.1, 0.2], "E", "Vector 4 - Category E"),
    (5, [0.3, 0.4, 0.5, 0.6], "F", "Vector 5 - Category F"),
]
client.upsert(
    collection_name=collection_name,
    points=[
        {
            "id": vector_id,"vector": vector,"payload": {"category": category,"description": description}
        }for vector_id,vector,category,description in vector_data
    ]
)
print("Vectors Inserted Successfully!")

query = np.random.rand(4).tolist()

# Perform a search
search_results = client.search(
    collection_name=collection_name,
    query_vector=query,
    limit=3 
)

for result in search_results:
    print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")