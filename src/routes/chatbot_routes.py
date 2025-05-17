from flask import Blueprint, request, jsonify
# Import the AI response function
from src.ai_models import get_ai_response, analyze_mood_with_ai # Assuming analyze_mood_with_ai might be used later
from src.routes.mood_routes import mood_data_store

chatbot_bp = Blueprint("chatbot_bp", __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    language = data.get("language", "en")  # Default to English
    preferred_model = "ollama" # Hardcoding to gemini as per current focus

    # Grab the current user’s ID
    user_id = data.get("user_id")

    # Pull their in-memory mood history (session-scoped)
    mood_history = mood_data_store.get(user_id, []) if user_id else []
    # Summarize it via the same AI handler
    mood_summary = analyze_mood_with_ai(mood_history, language)

    # Prepend the mood summary to the user’s prompt
    prompt = f"User mood summary: {mood_summary}\nUser: {user_message}"
    response_message = get_ai_response(prompt, language, preferred_model)

    return jsonify({
        "response": response_message,
        "language": language,
        "original_message": user_message
    })

@chatbot_bp.route("/suggest_therapist", methods=["POST"])
def suggest_therapist():
    data = request.json
    user_mood_details = data.get("mood_details", "No specific details provided.")
    language = data.get("language", "en")

    response_text = ""
    if language == "hi":
        # Using string concatenation to avoid multiline f-string issues robustly
        line1_hi = f"आपकी मनोदशा के विवरण के आधार पर (\n{user_mood_details}\n),"
        line2_hi = " हम जल्द ही चिकित्सक सुझाव प्रदान करेंगे। यह सुविधा विकास में है."
        response_text = line1_hi + line2_hi
    else:
        # Using string concatenation for English
        line1_en = f"Based on your mood details (\n{user_mood_details}\n),"
        line2_en = " therapist suggestions will be provided soon. This feature is under development."
        response_text = line1_en + line2_en
    
    return jsonify({"message": response_text, "status": "Therapist suggestion feature under development"})

