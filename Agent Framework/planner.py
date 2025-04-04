from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
import pprint
from rich import print

load_dotenv()

system_message=SystemMessage(content="You are a helpful assistant")
model=ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model='gpt-4o-mini',
    max_tokens=2048,
)

@tool
def search_tool(query:str)->str:
    """
    Searches the web for the information
    
    Args:
    query (str): The query to search for
    """
    search=GoogleSerperAPIWrapper(api_key=os.getenv("SERPER_API_KEY"))
    result=search.run(query)
    
    return results[:1500]  

@tool
def task_simplifier_tool(task:str)->str:
    """
    Simplifies the task by breaking it down into smaller tasks
    """
    prompt="""
    You are given a complex task to {task}. Your job is to analyze the task and 
    break it down into smaller, manageable tasks. Please provide a list of
    tasks that can be completed to achieve the main goal.
    """
    result=model.invoke(prompt)
    return result

tools=[search_tool,task_simplifier_tool]

query="""
    I want to launch an AI-powered mobile app that provides real-time language translation, 
    including speech-to-text and text-to-speech capabilities. Help me create a step-by-step development plan,
    including market research, tech stack selection, UI/UX design, and deployment.
"""
agent_executor=create_react_agent(model,tools,prompt=system_message)

messages=agent_executor.invoke({"messages":[("user",query)]})

result=messages['messages'][-1].content
print(f"[bold cyan]Latest Message:[/bold cyan]\n{result}")