import openai
import os
from dotenv import load_dotenv

load_dotenv()
client=openai.OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_ai(prompt):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


if __name__=="__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        response = chat_with_ai(user_input)
        print("Chatbot:", response)
        