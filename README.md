# Medi Bot - Mental Health Support AI

## Project Overview

Medi Bot is an AI-powered web application designed to provide emotional support, allow users to track their moods, and offer a space for feedback. It supports multiple languages (English and Hindi) and features a modern, professional, and animated user interface. This version integrates the Google Gemini API for live AI-powered chatbot responses and includes significant UI/UX enhancements.

## Features Implemented

1.  **Modern & Animated UI/UX:** A complete visual overhaul with a professional design, including a hero section with illustration, feature cards, improved forms, smooth navigation, and subtle animations for an engaging user experience.
2.  **Multilingual Chatbot (Gemini Powered):** Users can interact with the chatbot in English or Hindi. The AI responses are powered by the Google Gemini API (`models/gemini-1.5-flash-latest`). Includes animated chat bubbles and a typing indicator.
3.  **Mood Logging:** Users can log their mood (e.g., happy, sad, anxious), specify an intensity level (1-10) with a range slider, and add optional notes. This data is tracked per user ID.
4.  **Mood History & Basic Analysis:** Backend API endpoints exist for retrieving mood history and basic analysis (currently a simple count of moods). Frontend components for displaying this are not yet built.
5.  **User Feedback:** A dedicated section allows users to submit feedback or suggest new features through an enhanced form.
6.  **Language Selection:** Users can easily switch the interface and chatbot language between English and Hindi using a header-based selector.

## Technology Stack (as implemented)

*   **Backend:** Flask (Python)
*   **Frontend:** HTML5, CSS3 (with modern layouts like Flexbox/Grid, custom properties, and animations), JavaScript (for DOM manipulation, API calls, and interactive UI elements).
*   **AI Model Integration:** Google Gemini API (`models/gemini-1.5-flash-latest`) for chatbot responses.
*   **Libraries/Frameworks:** Font Awesome for icons, Google Fonts (Poppins).

## Project Structure (`/home/ubuntu/medi_bot`)

```
medi_bot/
├── venv/                   # Python virtual environment
├── src/
│   ├── static/
│   │   ├── index.html      # Main frontend page (redesigned)
│   │   ├── style.css       # CSS for the frontend (enhanced with animations)
│   │   ├── script.js       # JavaScript for frontend logic (enhanced for interactivity)
│   │   └── hero_illustration.png # Hero image for the landing page
│   ├── routes/
│   │   ├── chatbot_routes.py # API endpoints for the chatbot (uses Gemini)
│   │   └── mood_routes.py    # API endpoints for mood tracking
│   ├── ai_models.py          # AI model integration (Gemini, and placeholders)
│   └── main.py               # Main Flask application entry point
└── requirements.txt        # Python dependencies (includes google-generativeai)
```

## How to Run Locally (if downloaded)

1.  **Prerequisites:** Python 3.11+ and pip.
2.  **API Key:** Ensure you have a valid Gemini API key. The application is currently configured to use the key `AIzaSyBriz-OFny_rCxMxybUGQCGKOFgEaNOE28` as provided. If you need to use a different key, you will need to update it in `/home/ubuntu/medi_bot/src/ai_models.py`.
3.  **Unzip the project:** Extract the `medi_bot_ui_enhanced.zip` file.
4.  **Navigate to the project directory:** `cd path/to/medi_bot`
5.  **Create and activate a virtual environment (recommended):**
    *   `python3.11 -m venv venv`
    *   On Linux/macOS: `source venv/bin/activate`
    *   On Windows: `venv\Scripts\activate`
6.  **Install dependencies:** `pip install -r requirements.txt`
7.  **Run the Flask application:** `python src/main.py`
8.  Open your web browser and go to `http://127.0.0.1:5000`.

## Current Deployment

The application is temporarily deployed and accessible at the URL provided in the completion message. This URL is for demonstration and testing purposes and will not be permanently available.

## Future Enhancements (as per original request)

*   Integrate actual LLAMA 3.3 70B and potentially GPT APIs if desired, alongside Gemini.
*   Implement full therapist connection functionality.
*   Develop a Flutter frontend for mobile application experience.
*   Use Firebase for backend services and data persistence (currently using in-memory store for mood data).
*   Expand language support further.
*   Implement more sophisticated mood analysis using AI.
*   Add a dark mode toggle for the UI.

