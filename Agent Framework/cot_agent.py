from langchain_core.messages import SystemMessage,HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model='gpt-4o-mini',
    max_tokens=2048,
)

def call_model(state: MessagesState):
    system_prompt = (
        "You are a helpful assistant. "
        "Answer all questions based on the conversation history. "
        "Perform reasoning and take actions accordingly."
    )
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)
    return {"messages": response}

def reason_and_act(state: MessagesState):
    conversation_history = state["messages"]
    
    response = call_model(state)
    
    conversation_history.append({"role": "assistant", "content": response["messages"].content})


    return {"messages": conversation_history}

workflow = StateGraph(state_schema=MessagesState)

workflow.add_node("reasoning", reason_and_act)

workflow.add_edge(START, "reasoning")

memory = MemorySaver()

app = workflow.compile(checkpointer=memory)

query = """
    A snail is at the bottom of a 10-meter well. Every day, it climbs 3 meters up but slips back 2 meters at night.
    How many days will it take for the snail to get out of the well?
"""

state = {"messages": [{"role": "user", "content": query}]} 
response = app.invoke(
    state,
    config={"configurable": {"thread_id": "1"}} 
)


print("\n[bold cyan]Agent's Conversation History and Reasoning Process:[/bold cyan]")
for step in response["messages"]:
    role = "User" if isinstance(step, HumanMessage) else "Assistant"
    print(f"[bold cyan]{role}[/bold cyan]: {step.content}\n")