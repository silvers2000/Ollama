from flask import Blueprint, request, jsonify
from datetime import datetime

# In-memory storage for mood data (for demonstration purposes)
# In a real application, this would be a database.
mood_data_store = {}

mood_bp = Blueprint("mood_bp", __name__)

@mood_bp.route("/log_mood", methods=["POST"])
def log_mood():
    data = request.json
    user_id = data.get("user_id") # Assuming a user_id is provided for tracking
    mood = data.get("mood") # e.g., "happy", "sad", "anxious"
    intensity = data.get("intensity") # e.g., 1-10 scale
    notes = data.get("notes", "") # Optional notes from the user
    language = data.get("language", "en")

    if not user_id or not mood or intensity is None:
        return jsonify({"error": "Missing user_id, mood, or intensity"}), 400

    timestamp = datetime.utcnow().isoformat()
    mood_entry = {
        "timestamp": timestamp,
        "mood": mood,
        "intensity": intensity,
        "notes": notes,
        "language": language
    }

    if user_id not in mood_data_store:
        mood_data_store[user_id] = []
    mood_data_store[user_id].append(mood_entry)

    response_message = ""
    if language == "hi":
        response_message = f"नमस्ते {user_id}! आपकी मनोदशा (\'{mood}\') सफलतापूर्वक लॉग हो गई है।"
    else:
        response_message = f"Hello {user_id}! Your mood (\'{mood}\') has been logged successfully."

    return jsonify({"message": response_message, "entry_logged": mood_entry}), 201

@mood_bp.route("/get_mood_history/<user_id>", methods=["GET"])
def get_mood_history(user_id):
    language = request.args.get("language", "en") # Get language from query parameters
    if user_id not in mood_data_store:
        error_message = ""
        if language == "hi":
            error_message = f"{user_id} के लिए कोई मूड डेटा नहीं मिला।"
        else:
            error_message = f"No mood data found for user {user_id}."
        return jsonify({"error": error_message}), 404

    user_moods = mood_data_store[user_id]
    
    response_message = ""
    if language == "hi":
        response_message = f"{user_id} के लिए मूड इतिहास।"
    else:
        response_message = f"Mood history for user {user_id}."

    return jsonify({"message": response_message, "mood_history": user_moods})

@mood_bp.route("/analyze_mood/<user_id>", methods=["GET"])
def analyze_mood(user_id):
    # Placeholder for mood analysis logic
    # This would involve more complex processing in a real application
    language = request.args.get("language", "en")
    if user_id not in mood_data_store or not mood_data_store[user_id]:
        error_message = ""
        if language == "hi":
            error_message = f"{user_id} के लिए विश्लेषण करने के लिए कोई मूड डेटा नहीं मिला।"
        else:
            error_message = f"No mood data to analyze for user {user_id}."
        return jsonify({"error": error_message}), 404

    # Basic analysis: count moods (example)
    mood_counts = {}
    for entry in mood_data_store[user_id]:
        mood = entry["mood"]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    analysis_result = {"mood_summary": mood_counts, "message": "Basic mood count analysis."}

    response_message = ""
    if language == "hi":
        response_message = f"{user_id} के लिए मूड विश्लेषण।"
    else:
        response_message = f"Mood analysis for user {user_id}."

    return jsonify({"message": response_message, "analysis": analysis_result})


