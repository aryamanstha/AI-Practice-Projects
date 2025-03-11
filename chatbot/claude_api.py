import anthropic
from dotenv import load_dotenv
import os 
load_dotenv()

ANT_API_KEY=os.getenv("ANT_API_KEY")
client = anthropic.Client(api_key=ANT_API_KEY)

def chat_with_ai(prompt):
    response=client.messages.create(
        model='claude-3-7-sonnet-latest',
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    return response.content[0].text


if __name__=="__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        response = chat_with_ai(user_input)
        print("Claude Chatbot:", response)
