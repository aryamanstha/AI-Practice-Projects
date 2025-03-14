import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)
print(os.getenv("OPENAI_API_KEY"))  

def chat_with_ai(prompt):
    response = client.chat.completions.create(
      model="gpt-4o-mini",
     messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ]
    )
    return response.choices[0].message.content.strip()


if __name__=="__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        response = chat_with_ai(user_input)
        print("Chatbot:", response)
        