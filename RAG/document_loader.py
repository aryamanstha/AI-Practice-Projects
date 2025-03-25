import asyncio
import bs4
from langchain_community.document_loaders import PyPDFLoader,WebBaseLoader,TextLoader,UnstructuredWordDocumentLoader

async def load_pdf_pages():
    file_path = "D:/AI-Practice-Projects/QLoRA.pdf"
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages


def load_webpage():
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    assert len(docs) > 0
    print(docs[0].page_content[:500])

def load_txt_file():
    file_path = "D:/AI-Practice-Projects/sample.txt" 
    loader = TextLoader(file_path)
    docs = loader.load()
    assert len(docs) > 0  
    # print(docs[0].page_content[:500])
    return docs[0].page_content
    
    

def load_docx_file():
    file_path = "D:/AI-Practice-Projects/sample.docx"
    loader = UnstructuredWordDocumentLoader(file_path,mode="elements",strategy="fast")
    docs = loader.load()
    
    assert len(docs) > 0
    print(docs[0].page_content[:500])

if __name__ == "__main__":
    load_webpage()
    load_txt_file()
    load_docx_file()
    pages = asyncio.run(load_pdf_pages())
    print(f"{pages[0].metadata}\n")
    print(pages[0].page_content[:500])
    

