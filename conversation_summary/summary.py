from langchain.memory import ConversationSummaryMemory
# from langchain_openai import OpenAI
from langchain_community.llms import Anthropic
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import getpass
import os
from langchain.chat_models import init_chat_model

load_dotenv()

ant_api_key=os.getenv("ANT_API_KEY")

llm = init_chat_model("claude-3-7-sonnet-latest",api_key=ant_api_key,model_provider="anthropic")

# llm = Anthropic(model="claude-3-7-sonnet-latest", temperature=0.7)
conversation_with_summary = ConversationChain(
    llm=llm,
    memory=ConversationSummaryMemory(llm=llm),
    verbose=True
)
conversation_with_summary.predict(input="Tell me more about it")

conversation_with_summary.predict(input="What is the summary of our conversation?")