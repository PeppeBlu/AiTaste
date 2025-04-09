
from groq import Groq
import os
import datetime


client = Groq(
    api_key="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"
)

def chat():
    while True:
        print("\n\nEnter your message (or 'exit' to quit):")
        user_input = input("\n\nYou: ")
        if user_input.lower() == 'exit':
            break
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            if response is not None:
                print("\n\nAI:", response.choices[0].message.content)
            else:
                print("No response received.")
        except Exception as e:
            print("Error:", str(e))
   


while True:
    print("1. Chat")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        chat()
    elif choice == "2":
        break
    else:
        print("Invalid choice. Please try again.")
    