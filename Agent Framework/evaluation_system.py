from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv
import streamlit as st


st.set_page_config(page_title="LangGraph Evaluation System", page_icon=":robot_face:", layout="wide")
st.title("LangGraph Evaluation System")
st.write("This is an evaluation system for LangGraph using Anthropic Claude 3.")

load_dotenv()

class State(TypedDict):
    messages:Annotated[list,add_messages]
    
graph_builder=StateGraph(State)

llm=ChatAnthropic(
    model="claude-3-7-sonnet-latest",
    api_key=os.getenv("ANT_API_KEY"),
    temperature=0.5,
    max_tokens=500,
)

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def evaluate_response(state: State):
    user_input = state["messages"][-2].content
    assistant_output = state["messages"][-1].content
    
    evaluation_prompt = f"""
    Evaluate the assistant’s performance based on the following structured criteria. 
        Provide a score (1-5) and a detailed justification for each metric. 
        Ensure your assessment is based solely on the provided user input and assistant response.
    Key Metrics
    1. Response Time
       - Score: [1-5] (5 = consistently under 2 seconds)  
       - Justification: Explain if the response time meets the goal of being under 2 seconds. 
       Consider the average response time across multiple interactions if applicable. 
       If the response time is consistently under 2 seconds, provide a score of 5. 
       If it frequently exceeds this threshold, provide a lower score and explain the observed delays.
       
    2. Task Completion Rate  
       - Score: [1-5] (5 = 80%+ successful task completion)  
       - Justification: Evaluate if the assistant successfully completes the tasks as intended by the user.
       Consider the user’s goal (e.g., booking, troubleshooting) and confirm if the assistant achieves this goal. 
       If the task completion rate is 80% or higher, provide a score of 5. 
       If it falls below this threshold, provide a lower score and explain the reasons for incomplete tasks.
       
    3. Error Rate  
       - Score: [1-5] (5 = errors below 5%)  
       - Justification: Assess the frequency and severity of errors in the assistant’s responses. 
       This includes crashes, unhandled exceptions, or incorrect outputs. If the error rate is below 5%, provide a score of 5. 
       If errors are frequent or severe, provide a lower score and describe the types of errors encountered.
       
    4. Relevance  
       - Score: [1-5] (5 = directly addresses all aspects of the user’s query without irrelevant elements)  
       - Justification: Evaluate if the assistant’s response directly addresses all aspects of the user’s query.
       Consider if there are any irrelevant or off-topic elements in the response.
       If the response is highly relevant and focused, provide a score of 5. 
       If there are irrelevant elements or the response misses key aspects of the query, provide a lower score and explain the observed issues.
       
    5. Helpfulness  
       - Score: [1-5] (5 = accurate, thorough, and actionable, providing useful details or guidance)  
       - Justification: Assess if the assistant’s response is accurate, thorough, and actionable.
       Consider if the response provides useful details, examples, or guidance that help the user achieve their goal. 
       If the response is highly helpful and meets the user’s needs, provide a score of 5.
       If the response lacks necessary details or is not actionable, provide a lower score and explain the observed shortcomings.
       
    6. Clarity  
       - Score: [1-5] (5 = logically structured, concise, and free of unnecessary jargon)  
       - Justification: Evaluate if the assistant’s response is logically structured and easy to follow.\
        Consider if the language is concise and free of unnecessary jargon.
        If the response is clear and understandable, provide a score of 5. 
        If the response is confusing or contains jargon, provide a lower score and explain the observed issues.
        
    7. Fluency  
       - Score: [1-5] (5 = grammatically correct, natural, and free of awkward phrasing)  
       - Justification: Assess if the assistant’s response is grammatically correct and natural. 
       Consider if the sentences are well-formed and free of awkward phrasing. 
       If the response is highly fluent and natural, provide a score of 5. 
       If there are grammatical errors or awkward phrasing, provide a lower score and explain the observed issues.
       
    8. Dialog Path Testing  
       - Score: [1-5] (5 = handles all expected conversation flows)  
       - Justification: Evaluate the assistant’s ability to handle both common and edge-case conversation flows. 
       This includes interruptions, corrections, and unexpected user inputs. 
       If the assistant handles all expected dialog paths smoothly, provide a score of 5.
       If there are issues with specific dialog paths, provide a lower score and explain the observed problems.
       
    9. Scalability & Load Testing  
       - Score: [1-5] (5 = stable under high concurrency)  
       - Justification: Assess the assistant’s performance under high user traffic. 
       Simulate high concurrency and evaluate if the system remains stable and responsive. 
       If the assistant performs well under stress, provide a score of 5. 
       If there are performance issues or resource constraints, provide a lower score and describe the observed limitations.

    The user input and assistant response are as follows:
    User input: {user_input}
    Assistant response: {assistant_output}
    """

    evaluation = llm.invoke([{"role": "user", "content": evaluation_prompt}])
    return {"messages": [evaluation]}

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_node("evaluate_response",evaluate_response)

graph_builder.add_edge(START,"chatbot")

graph_builder.add_edge("chatbot","evaluate_response")

graph_builder.add_edge("evaluate_response",END)

graph=graph_builder.compile()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask something...")    
    
if user_input:
    user_message = {"messages": [{"role": "user", "content": user_input}]}
    full_message_log = []

    with st.spinner("Thinking..."):
        for event in graph.stream(user_message):
            for step_name, value in event.items():
                full_message_log.append((step_name, value["messages"][-1].content))

    st.session_state.chat_history.append((user_input, full_message_log))

for user_input, logs in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_input)

    for step_name, content in logs:
        if step_name == "chatbot":
            with st.chat_message("assistant"):
                st.markdown(content)
        elif step_name == "evaluate_response":
            with st.expander("📊 Evaluation", expanded=False):
                st.markdown(content)
