document.addEventListener("DOMContentLoaded", () => {
    window.currentUserId = null;
    const languageSelectHeader = document.getElementById("language-select-header");
    const chatInput = document.getElementById("chat-input");
    const sendChatBtn = document.getElementById("send-chat-btn");
    const chatOutput = document.getElementById("chat-output");

    const userIdMoodInput = document.getElementById("user-id-mood");
    const moodSelect = document.getElementById("mood-select");
    const moodIntensityInput = document.getElementById("mood-intensity");
    const moodIntensityValue = document.getElementById("mood-intensity-value");
    const moodNotesInput = document.getElementById("mood-notes");
    const logMoodBtn = document.getElementById("log-mood-btn");
    const moodLogStatus = document.getElementById("mood-log-status");

    const feedbackInput = document.getElementById("feedback-input");
    const submitFeedbackBtn = document.getElementById("submit-feedback-btn");
    const feedbackStatus = document.getElementById("feedback-status");

    // Smooth scroll for navigation links
    document.querySelectorAll("header .nav-links a").forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });
    });

    // Active nav link highlighting on scroll
    const sections = document.querySelectorAll("main section[id]");
    const navLi = document.querySelectorAll("header .nav-links li a");

    window.addEventListener("scroll", () => {
        let current = "";
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 60) { // 60px for header height
                current = section.getAttribute("id");
            }
        });

        navLi.forEach(a => {
            a.classList.remove("active");
            if (a.getAttribute("href").substring(1) === current) {
                a.classList.add("active");
            }
        });
    });


    // Function to add message to chat output with animation
    function addChatMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message", "message-bubble");
        // render incoming Markdown (bold, italics, etc.)
        messageDiv.innerHTML = marked.parse(message);

        chatOutput.appendChild(messageDiv);
        
        // Trigger animation
        setTimeout(() => {
            messageDiv.classList.add("visible");
        }, 10); // Small delay to ensure transition triggers

        chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll to bottom
    }

    // Typing indicator function
    let typingIndicatorTimeout;
    function showTypingIndicator() {
        removeTypingIndicator(); // Remove any existing one
        const typingDiv = document.createElement("div");
        typingDiv.classList.add("bot-message", "message-bubble", "typing-indicator");
        typingDiv.innerHTML = `<span class=\"dot\"></span><span class=\"dot\"></span><span class=\"dot\"></span>`; // CSS animated dots
        chatOutput.appendChild(typingDiv);
        chatOutput.scrollTop = chatOutput.scrollHeight;
        // Automatically remove after some time if no response comes
        typingIndicatorTimeout = setTimeout(removeTypingIndicator, 8000);
    }

    function removeTypingIndicator() {
        clearTimeout(typingIndicatorTimeout);
        const existingIndicator = chatOutput.querySelector(".typing-indicator");
        if (existingIndicator) {
            existingIndicator.remove();
        }
    }

    // Send chat message
    async function handleSendMessage() {
        const message = chatInput.value.trim();
        const language = languageSelectHeader.value;
        if (!message) return;

        addChatMessage(message, "user");
        chatInput.value = "";
        showTypingIndicator();

        try {
            const response = await fetch("/api/chatbot/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                   message,
                   language,
                   user_id: window.currentUserId
                 })
            });
            removeTypingIndicator();
            const data = await response.json();
            if (response.ok) {
                addChatMessage(data.response, "bot");
            } else {
                addChatMessage(`Error: ${data.error || "Failed to get response"}`, "bot");
            }
        } catch (error) {
            removeTypingIndicator();
            addChatMessage(`Error: ${error.message}`, "bot");
        }
    }

    sendChatBtn.addEventListener("click", handleSendMessage);
    chatInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            handleSendMessage();
        }
    });

    // Update mood intensity display
    if (moodIntensityInput && moodIntensityValue) {
        moodIntensityInput.addEventListener("input", () => {
            moodIntensityValue.textContent = moodIntensityInput.value;
        });
    }

    // Log mood
    if (logMoodBtn) {
        logMoodBtn.addEventListener("click", async () => {
            const userId = userIdMoodInput.value.trim();
            const mood = moodSelect.value;
            const intensity = parseInt(moodIntensityInput.value);
            const notes = moodNotesInput.value.trim();
            const language = languageSelectHeader.value; // Use header language select

            if (!userId) {
                moodLogStatus.textContent = "User ID is required.";
                moodLogStatus.className = "status-message error-message visible";
                return;
            }
            if (isNaN(intensity) || intensity < 1 || intensity > 10) {
                moodLogStatus.textContent = "Intensity must be a number between 1 and 10.";
                moodLogStatus.className = "status-message error-message visible";
                return;
            }

            moodLogStatus.textContent = "Logging mood...";
            moodLogStatus.className = "status-message visible";

            try {
                const response = await fetch("/api/mood/log_mood", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ user_id: userId, mood, intensity, notes, language }),
                });
                const data = await response.json();
                if (response.ok) {
                    moodLogStatus.textContent = data.message;
                    moodLogStatus.className = "status-message success-message visible";
                    window.currentUserId = userId;
                } else {
                    moodLogStatus.textContent = `Error: ${data.error || "Failed to log mood"}`;
                    moodLogStatus.className = "status-message error-message visible";
                }
            } catch (error) {
                moodLogStatus.textContent = `Error: ${error.message}`;
                moodLogStatus.className = "status-message error-message visible";
            }
            setTimeout(() => { moodLogStatus.classList.remove("visible"); }, 4000);
        });
    }

    // Submit feedback
    if (submitFeedbackBtn) {
        submitFeedbackBtn.addEventListener("click", () => {
            const feedback = feedbackInput.value.trim();
            if (!feedback) {
                feedbackStatus.textContent = "Please enter your feedback.";
                feedbackStatus.className = "status-message error-message visible";
                return;
            }

            console.log("Feedback submitted:", feedback);
            feedbackStatus.textContent = "Thank you for your feedback!";
            feedbackStatus.className = "status-message success-message visible";
            feedbackInput.value = "";

            setTimeout(() => {
                feedbackStatus.classList.remove("visible");
            }, 3000);
        });
    }

    // Language selector synchronization (if you had two, now only one in header)
    // If there was another language selector, you would sync it here.
    // For now, we only have languageSelectHeader.

    // Initial active link update
    window.dispatchEvent(new Event("scroll"));

});

