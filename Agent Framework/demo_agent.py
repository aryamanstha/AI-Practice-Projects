from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
import json
from rich import print_json
from jsonschema import validate, ValidationError

load_dotenv()

system_message=SystemMessage(
    content="""You are a helpful assistant
    Use the tools provided to answer the user's question.
    You can use the calculator tool to perform calculations.
    You can use the search_web tool to search the web for information.
    If you are not sure about the answer, use the search_web tool.""")

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

search_web_schema = {
    "type": "object",
    "properties": {
        "result": {
            "type": "float"
        }
    },
    "required": ["result"]
}
@tool
def search_web(query:str)->str:
    """
    Search the web for a query.
    
    Arguments:
    query (str): The query to search for.
    """
    search=GoogleSerperAPIWrapper(api_key=os.getenv("SERPER_API_KEY"))
    result=search.run(query)
    search_result = {
        "result": result[:1500]  
    }
    try:
        validate(instance=search_result, schema=search_web_schema)
    except ValidationError as e:
        return f"JSON Validation Error: {e.message}"

    return json.dumps(search_result) 
    
tool=[calculator,search_web]

query="What's the current weather in Kathmandu?"

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