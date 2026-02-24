import os
from groq import Groq
from dotenv import load_dotenv
from riddle_logic import build_prompt

load_dotenv()

# Initialize the Groq client once at the module level
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Defining a primary model (Llama 3.3 70B is excellent for Hebrew and complex logic)
MODEL_NAME = "llama-3.3-70b-versatile"

def get_ai_response(character_name, message_history):
    """
    Sends a request to Groq using the character's system prompt and chat history.
    """
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("No GROQ_API_KEY found in environment variables")

    # 1. Prepare the System Prompt
    system_instructions = build_prompt(character_name)
    
    # 2. Convert history to Groq/OpenAI format
    # Groq expects a simple list of {"role": "...", "content": "..."}
    groq_messages = [
        {"role": "system", "content": system_instructions}
    ]
    
    for msg in message_history:
        # Standardize roles: Groq uses 'user' and 'assistant'
        role = "user" if msg['role'] == "user" else "assistant"
        groq_messages.append({
            "role": role,
            "content": msg['content']
        })

    # 3. Execution with a single try-except block
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=groq_messages,
            temperature=0.7, # Adjust for creativity
            max_tokens=1024,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        print(f"DEBUG: Error with Groq API: {e}")
        # Custom Hebrew error message for the UI
        return "אופס, נראה שקרתה שגיאה בתקשורת עם השרת. כדאי לנסות שוב בעוד רגע."