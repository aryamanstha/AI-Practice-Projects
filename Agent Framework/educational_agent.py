from langchain_core.messages import SystemMessage,HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from langgraph.prebuilt import create_react_agent
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import tempfile
from langchain_community.tools import YouTubeSearchTool

# ========== Load Environment and Config ========== #
load_dotenv()
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# ========== Initialize Streamlit App ========== #
st.set_page_config(page_title="Specialized Agent", layout="wide")
st.title("Educational Agent")

# ========== Init Session State ========== #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
# ========== LLM Setup ========== #
system_message = SystemMessage(content="""You are a helpful assistant
When the user asks for a quiz, use the quiz_creator tool.
When the user asks for information, use the search_tool.
When the user asks for a video, use the search_youtube tool.
Always follow the user's instructions based on the context.""")

model = ChatAnthropic(
    api_key=os.getenv("ANT_API_KEY"),
    model='claude-3-7-sonnet-latest',
    max_tokens=500,
)

# ========== Define Tools ========== #
@tool
def quiz_creator(query: str) -> str:
    """
    Creates a quiz based on the provided topic.
    """
    prompt = f"""You are a teacher creating practice questions based on the following content:
    "{query}"
    Generate multiple-choice quiz questions based on the above query. 
    Each question should have 4 options and indicate the correct answer.
    Format:
    Q1: ...
    A. ...
    B. ...
    C. ...
    D. ...
    Answer: ...
    
    Q2: ...
    ...
    Make sure the questions test real understanding. Also provide a short explanation why the answer is correct.
    """
    result = model.invoke(prompt)
    return result

@tool
def search_tool(query: str) -> str:
    """
    Searches the web for the information
    """
    search = GoogleSerperAPIWrapper(api_key=os.getenv("SERPER_API_KEY"),type="news")
    results = search.run(query)
    return results[:1500]

def load_and_embed_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embeddings)
    return vectordb

@tool
def document_summarizer(query: str) -> str:
    """
    Summarizes a long document or article.
    """
    prompt = f"""You are a helpful assistant. Summarize the following content for me:
    "{query}"
    """
    result = model.invoke(prompt)
    return result

@tool
def search_youtube(query: str) -> str:
    """
    Searches YouTube for the information
    """
    search = YouTubeSearchTool()
    results = search.run(query,10)
    return results

@tool
def study_plan_generator(query: str) -> str:
    """
    Generates a personalized study plan based on the user's goals and available time.
    """
    prompt = f"""You are a helpful assistant. Generate a study plan based on the following goals and time availability:
    "{query}"
    """
    result = model.invoke(prompt)
    return result
# ========== Setup Agent ========== #
tools = [quiz_creator, search_tool,search_youtube,study_plan_generator,document_summarizer]
agent_executor= create_react_agent(model, tools, prompt=system_message)


# ========== Handle File Upload and PDF Summary ========== #
uploaded_file = st.file_uploader("Upload a PDF to summarize", type=["pdf"])

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.get("last_uploaded_filename", ""):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        st.session_state.last_uploaded_filename = uploaded_file.name

        vectordb = load_and_embed_pdf(pdf_path)
        st.session_state.pdf_knowledge_base = vectordb
        st.session_state.chat_history.append(("user", f"Uploaded PDF: {uploaded_file.name}"))


        docs = vectordb.similarity_search("Summarize the document", k=5)
        full_text = "\n".join([doc.page_content for doc in docs])
        summary_prompt = f"""You are a helpful assistant. Summarize the following document content for me:\n\n{full_text}"""
        summary = model.invoke(summary_prompt)
        st.session_state.chat_history.append(("assistant", summary.content))

# ========== Chat Input and Response ========== #
query = st.chat_input("Write a message...")

if query:
    st.session_state.chat_history.append(("user", query))

    with st.spinner("Generating answer..."):
        conversation_history = [
        HumanMessage(content=msg) if role == "user" else AIMessage(content=msg)
            for role, msg in st.session_state.chat_history
        ]
        conversation_history.insert(0, system_message)

        result = agent_executor.invoke({"messages": conversation_history})
        response = result['messages'][-1].content
        st.session_state.chat_history.append(("assistant", response))

# ========== Display Chat History ========== #
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)





# query="""
#     Create a quiz on the topic of "Artificial Intelligence".
#     Include multiple-choice questions with options and correct answers.
#     """