import re
import requests

class AIModelHandler:
    def __init__(self, model_name="llama2", ollama_url="http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url

    def get_response(self, prompt, language="en"):
        try:
            if language == "hi":
                prompt = f"निम्नलिखित का उत्तर हिंदी में दें: {prompt}"
            else:
                prompt = f"Respond in {language}: {prompt}"

            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful medical assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                }
            )
            response.raise_for_status()
            content = response.json().get("message", {}).get("content", "")
            # # Format numbered/bulleted list as new lines
            # content = re.sub(r'\s*(\d+\.)', r'\n\n\1', content)           # Numbered items
            # content = re.sub(r'\s*•', r'\n\n•', content)                  # Bullet points (if present)
            # content = re.sub(r'(?<!\n)\n(?!\n)', ' ', content)            # Avoid single line breaks
            # content = content.replace('. ', '.\n\n')   
            return content if content else "Sorry, no response received from Ollama."
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"

    def analyze_mood_data(self, mood_history, language="en"):
        print(f"Simulating AI mood analysis with Ollama model: {self.model_name}")
        if not mood_history:
            return "No mood data available for analysis." if language == "en" else "विश्लेषण के लिए कोई मूड डेटा उपलब्ध नहीं है।"
        positive, negative, neutral = 0, 0, 0
        for entry in mood_history:
            mood = entry.get("mood", "").lower()
            if mood in ["happy", "joyful", "excited", "content"]:
                positive += 1
            elif mood in ["sad", "anxious", "stressed", "angry"]:
                negative += 1
            else:
                neutral += 1
        if language == "hi":
            return f"आपके मूड का सारांश: {positive} सकारात्मक, {negative} नकारात्मक, {neutral} तटस्थ।"
        return f"Mood summary: {positive} positive, {negative} negative, {neutral} neutral."

# Use Ollama's llama2 or mistral model
ollama_handler = AIModelHandler(model_name="llama2")

def get_ai_response(prompt, language="en", preferred_model="ollama"):
    return ollama_handler.get_response(prompt, language)

def analyze_mood_with_ai(mood_history, language="en", preferred_model="ollama"):
    return ollama_handler.analyze_mood_data(mood_history, language)
