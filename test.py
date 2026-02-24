import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


# 1. Initialize the client
# It's best practice to store your key in an environment variable named 'GROQ_API_KEY'
# Alternatively, you can pass it directly: Groq(api_key="your_key_here")
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 2. Ask the LLM a question
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the difference between a list and a tuple in Python.",
        }
    ],
    model="llama-3.3-70b-versatile",
)

# 3. Print the response
print(chat_completion.choices[0].message.content)