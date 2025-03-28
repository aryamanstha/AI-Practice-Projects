from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


sample_text = "Once upon a time, there was a little boy"

def get_embeddings(text,model=model):
    return model.encode([text])

embedding_array=np.array(get_embeddings(sample_text))
print(embedding_array)
np.save("embedding.npy",embedding_array)

