from flask import Blueprint, request, jsonify
# Import the AI response function
from src.ai_models import get_ai_response, analyze_mood_with_ai # Assuming analyze_mood_with_ai might be used later
from src.routes.mood_routes import mood_data_store

chat_history_store = {}


chatbot_bp = Blueprint("chatbot_bp", __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    language = data.get("language", "en")  # Default to English
    preferred_model = "ollama" # Hardcoding to gemini as per current focus

    # Grab the current user’s ID
    user_id = data.get("user_id")

    # 1) Pull & summarize mood history
    mood_history = mood_data_store.get(user_id, []) if user_id else []
    mood_summary = analyze_mood_with_ai(mood_history, language)

    # 2) Fetch or init this session’s chat history
    history = chat_history_store.setdefault(user_id, [])

    # 3) Add mood summary as system context, then the new user message
    history.append({
        "role":    "system",
        "content": f"User mood summary: {mood_summary}"
    })
    history.append({"role": "user", "content": user_message})

    # 4) Build a single prompt including all turns so far
    prompt = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in history
    )

    # 5) Query the model with the full history
    response_message = get_ai_response(prompt, language, preferred_model)

    # 6) Append the assistant’s reply to history
    history.append({"role": "assistant", "content": response_message})
 
    return jsonify({
        "response":         response_message,
        "language":         language,
        "original_message": user_message
    })

@chatbot_bp.route("/suggest_therapist", methods=["POST"])
def suggest_therapist():
    data = request.json
    # 1) extract everything we need
    user_id          = data.get("user_id")
    user_mood_details = data.get("mood_details", "No specific details provided.")
    language         = data.get("language", "en")
    preferred_model  = "ollama"

    # 2) initialize this user’s chat history if needed
    history = chat_history_store.setdefault(user_id, [])

    # 3) treat their mood_details as the last “user” turn
    history.append({"role": "user", "content": user_mood_details})

    # 4) build a single prompt including all prior turns
    prompt = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in history
    )

    # 5) ask your LLM for a response
    response_text = get_ai_response(prompt, language, preferred_model)

    # 6) record the assistant’s reply in history
    history.append({"role": "assistant", "content": response_text})

    # 7) return it
    return jsonify({"message": response_text})

