from document_loader import load_txt_file
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
document = load_txt_file()

def character_splitter():
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=10, chunk_overlap=0
    )
    texts = text_splitter.split_text(document)
    return texts

def semantic_splitter():
    text_splitter = SemanticChunker(embed_model, breakpoint_threshold_type="percentile")
    docs = text_splitter.create_documents([document])
    return [doc.page_content for doc in docs]


if __name__ == "__main__":
    # print(character_splitter())
    print(semantic_splitter())
    