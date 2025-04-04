from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()

system_message=SystemMessage(content="You are a helpful assistant")

@tool
def calculator(x: float, y: float, operation: str) -> float:
    """
    A simple calculator that performs basic arithmetic operations.
    Args:
        x (float): First number.
        y (float): Second number.
        operation (str): Can be "add", "subtract", "multiply", or "divide".
    Returns:
        float: The result of the calculation.
    """
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation=="multiply":
        return x*y
    elif operation =="division":
        if y==0:
            return "Error: Division by zero is not allowed"
        else:
            return x/y
    else:
        return "Error: Invalid operation"

@tool
def search_web(query:str)->str:
    """
    Search the web for a query.
    
    Arguments:
    query (str): The query to search for.
    """
    search=GoogleSerperAPIWrapper(api_key=os.getenv("SERPER_API_KEY"),type="places")
    result=search.run(query)
    
    return results[:1500]    
    
tool=[calculator,search_web]

query="Can you list me some popular restaurants in Nepal?"

model=ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model='gpt-4o-mini',
    max_tokens=500
)

agent_executor=create_react_agent(model,tool,prompt=system_message)

messages=agent_executor.invoke({"messages":[("user",query)]})

print({
    "input":query,
    "output":messages['messages'][-1].content,
})