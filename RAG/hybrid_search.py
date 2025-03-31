import meilisearch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

client = meilisearch.Client('http://127.0.0.1:7700')
index = client.index('documents')

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_dimension = 384

faiss_index = faiss.IndexFlatL2(embedding_dimension)
documents= []

docs = [
    {"text": "This is a document about machine learning.", "source": "Document 1"},
    {"text": "This is a document about artificial intelligence.", "source": "Document 2"},
    {"text": "This is a document about deep learning.", "source": "Document 3"},
    {"text": "This is a document about Las Vegas.", "source": "Document 4"},
    {"text": "This is a document about gambling.", "source": "Document 5"},
    {"text": "This is a document about vacation.", "source": "Document 6"},
]

def index_document(doc_id, text, source):
    document = {"id": doc_id, "text": text, "source": source}
    index.add_documents([document])
    embedding = embedding_model.encode(text, convert_to_numpy=True)
    faiss_index.add(np.array([embedding]))
    documents.append({"text": text, "source": source})


for idx, doc in enumerate(docs):
    index_document(idx, doc["text"], doc["source"])


def hybrid_search(query, k=3):
 
    keyword_results = index.search(query, {"limit": k})
    keyword_docs = {int(hit["id"]): {"text": hit["text"], "source": hit["source"]} for hit in keyword_results["hits"]}

    query_embedding = embedding_model.encode(query, convert_to_numpy=True)
    _, faiss_indices = faiss_index.search(np.array([query_embedding]), k)
    semantic_docs = {idx: documents[idx] for idx in faiss_indices[0]}

    merged_results = {**keyword_docs, **semantic_docs}

    results_with_attribution = []
    for doc_id, doc in merged_results.items():
        result_text = doc["text"]
        source = doc["source"]
        result_with_attribution = f"Text: {result_text} (Source: {source})"
        results_with_attribution.append(result_with_attribution)

    return results_with_attribution


query = "What is Artificial Intelligence?"
results = hybrid_search(query)

print("Hybrid Search Results:")
for r in results:
    print(f"{r}")
