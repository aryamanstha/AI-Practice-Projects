import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)
def generate_response(prompt, model="gpt-4o-mini",temperature=0.5)->str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

text="Hello, how are you today?"
def zero_shot_prompting()->str:
    prompt=f"""Translate the given piece of text into Spanish. The text is enclosed in triple backticks.
            Text: ```{text}```
        """
    return generate_response(prompt)

def few_shot_prompting()->str:
    prompt = """
    Translate the following sentences into French:
    English: Good morning! How are you?
    French: Bonjour! Comment ça va?
    English: Have a great day!
    French: Passe une bonne journée!
    English: Hello, how are you today?
    French:
    """
    return generate_response(prompt)

def chain_of_thought()->str:
    prompt = """
    Solve the following math problem step by step:
    A farmer has 10 apples. He gives 3 to his friend and buys 5 more. How many apples does he have now?
    """
    return generate_response(prompt)

def react_prompting()->str:
    prompt = """
    You are an AI assistant helping a user navigate a new city. The user asks: "Where can I find a good coffee shop nearby?"
    Think step by step about what information you need and provide a recommendation.
    """
    return generate_response(prompt)

if __name__== "__main__":
    print("Zero-shot prompting:",zero_shot_prompting())
    print("Few-shot prompting:",few_shot_prompting())
    print("Chain of thought:",chain_of_thought())
    print("React prompting:",react_prompting())
    
    