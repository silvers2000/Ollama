# 🧠 Medi Bot – Mental Health Chatbot (Powered by Ollama)

Medi Bot is a locally hosted AI-powered web application designed to offer mental health support, mood tracking, and real-time interaction through a conversational chatbot. It leverages **Ollama** to run large language models like **LLaMA2** or **LLaMA3** directly on your machine for a secure, private, and fast user experience.

---

## 🚀 Key Features

### 🌐 Local AI Chatbot (Ollama)
- Uses **Ollama** to run local LLMs (LLaMA2, LLaMA3, etc.) on your GPU or CPU.
- No internet dependency for model queries.
- Supports multilingual interaction: English and Hindi.
- Real-time typing animations and chat interface.

### 📊 Mood Logger
- Allows users to log their current mood.
- Select mood from presets (happy, sad, anxious, etc.).
- Intensity slider (1–10) and optional notes for self-reflection.

### 💬 Feedback Collector
- Lets users give feedback on their experience.
- Data can be stored for further enhancement or sentiment analysis.

### 🎨 Animated & Responsive UI
- Built with modern UI/UX principles.
- Smooth animations, SVG graphics, and user-friendly layout.
- Fully responsive across desktop and mobile devices.

---

## 🛠️ Technology Stack

| Component     | Technology                    |
|---------------|-------------------------------|
| Frontend      | HTML, CSS, JavaScript         |
| Backend       | Flask                          |
| AI Model      | Ollama (LLaMA2 / LLaMA3)       |
| Communication | REST API via `requests` module|
| Extras        | Flask-CORS, animated UI       |

---

## 🧠 Ollama Model Integration

Medi Bot does not rely on external APIs like OpenAI or Gemini. Instead, it interacts with Ollama using the following pattern:

```python
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama2",
        "messages": [
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
)
