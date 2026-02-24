from datetime import datetime
import random
from flask import Flask, render_template
from riddle_logic import get_character_list, build_prompt # Add this import at the top
from flask import request, jsonify # Make sure to import jsonify and request
# import gemini_chat
import groq_chat
# Initialize the Flask application
app = Flask(__name__)

# --- CONFIGURATION ---
# The date your relationship started
START_DATE = datetime(2023, 3, 12)

# Calculate the 3-year anniversary date automatically
ANNIVERSARY_DATE = START_DATE.replace(year=START_DATE.year + 3)

MEMORY_PICTURES = [f"images/image{i}.jpeg" for i in range(1, 17)]

@app.route("/")
def home():
    """
    This function runs when someone visits the main page.
    It calculates the countdown and renders the HTML template.
    """
    # 1. Calculate the time remaining until the 3-year anniversary
    time_remaining = ANNIVERSARY_DATE - datetime.now()
    
    # We add 1 to make the countdown inclusive (e.g., if it's the day before, it shows "1 day left").
    # We also use max(0, ...) to ensure it shows 0 instead of a negative number after the date has passed.
    days_until = max(0, time_remaining.days + 1)
    
    # 2. Send the data to the frontend template
    return render_template(
        "index.html",
        days_until_anniversary=days_until
    )

@app.route("/memory-game")
def memory_game():
    """
    Prepares and renders the memory game page.
    Generates pairs where one card is the 'left' half and one is the 'right' half.
    """
    cards = []
    for img in MEMORY_PICTURES:
        # Create the Left Half card
        cards.append({'url': img, 'side': 'left'})
        # Create the Right Half card
        cards.append({'url': img, 'side': 'right'})
    
    # Shuffle all the halves together
    random.shuffle(cards)
    
    return render_template("memory_game.html", cards=cards)

# The 'endpoint' is the name of this function: 'riddle'
@app.route('/riddle')
def riddle():
    # Fetch the list from the helper file
    characters = get_character_list()
    return render_template('riddle.html', characters=characters)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    char_name = data.get('character')
    history = data.get('history')
    
    try:
        # קריאה לפונקציה מתוך riddle.py
        reply = groq_chat.get_ai_response(char_name, history)
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "סליחה, אני קצת מבולבל כרגע. נסי שוב?"}), 500


if __name__ == "__main__":
    # This makes the server run when you execute `python app.py`
    # debug=True allows the server to auto-reload when you save changes.
    app.run(debug=True)
