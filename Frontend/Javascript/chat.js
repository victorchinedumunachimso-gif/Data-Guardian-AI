// ========================================
// Data Guardian AI
// AI Chat
// ========================================

console.log("✅ chat.js loaded");


document.addEventListener("DOMContentLoaded", function () {

    console.log("🚀 Chat page started");


    const chatInput =
        document.getElementById("chatInput");

    const sendButton =
        document.getElementById("sendButton");

    const chatMessages =
        document.getElementById("chatMessages");


    // ====================================
    // Check HTML elements
    // ====================================

    if (!chatInput) {

        console.error("❌ chatInput not found");

        return;
    }

    if (!sendButton) {

        console.error("❌ sendButton not found");

        return;
    }

    if (!chatMessages) {

        console.error("❌ chatMessages not found");

        return;
    }


    console.log("✅ Chat elements found");


    // ====================================
    // Send Message
    // ====================================

    async function sendMessage() {

        const prompt =
            chatInput.value.trim();


        if (!prompt) {

            return;

        }


        // =================================
        // Get Analysis
        // =================================

        const saved =
            localStorage.getItem(
                "analysisResult"
            );


        console.log(
            "💾 Saved analysis:",
            saved
        );


        if (!saved) {

            addMessage(
                "Please analyze a dataset first.",
                "ai"
            );

            return;

        }


        let analysisResult;


        try {

            analysisResult =
                JSON.parse(saved);

        }

        catch (error) {

            console.error(
                "❌ Could not parse analysis:",
                error
            );

            addMessage(
                "The saved analysis data is invalid.",
                "ai"
            );

            return;

        }


        // =================================
        // Show User Message
        // =================================

        addMessage(
            prompt,
            "user"
        );


        chatInput.value = "";

        sendButton.disabled = true;

        sendButton.textContent =
            "Thinking...";


        try {

            console.log(
                "📤 Sending request to backend..."
            );


            const response = await fetch(

                "http://127.0.0.1:8000/api/v1/chat",

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        prompt:
                            prompt,

                        analysis_result:
                            analysisResult

                    })

                }

            );


            console.log(
                "📡 Backend status:",
                response.status
            );


            const data =
                await response.json();


            console.log(
                "🤖 Backend response:",
                data
            );


            if (!response.ok) {

                addMessage(

                    "Backend error: " +
                    (data.detail ||
                    "Unknown error"),

                    "ai"

                );

                return;

            }


            // =================================
            // Extract AI Response
            // =================================

            const chatResponse =
                data.chat_response;


            let answer =
                "No response received.";


            if (
                chatResponse &&
                Array.isArray(
                    chatResponse.response
                )
            ) {

                answer =
                    chatResponse.response
                        .map(
                            item => "• " + item
                        )
                        .join("<br>");

            }

            else if (
                chatResponse &&
                chatResponse.response
            ) {

                answer =
                    chatResponse.response;

            }


            addMessage(
                answer,
                "ai"
            );


        }

        catch (error) {

            console.error(
                "❌ Chat connection error:",
                error
            );


            addMessage(

                "Failed to connect to the backend.",

                "ai"

            );

        }

        finally {

            sendButton.disabled =
                false;

            sendButton.textContent =
                "Send";

            chatInput.focus();

        }

    }


    // ====================================
    // Add Message
    // ====================================

    function addMessage(
        message,
        type
    ) {

        const messageDiv =
            document.createElement("div");


        messageDiv.className =
            type === "user"
                ? "message user-message"
                : "message ai-message";


        messageDiv.innerHTML = `

            <strong>
                ${
                    type === "user"
                        ? "You"
                        : "Data Guardian AI"
                }
            </strong>

            <p>
                ${message}
            </p>

        `;


        chatMessages.appendChild(
            messageDiv
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }


    // ====================================
    // Button
    // ====================================

    sendButton.addEventListener(
        "click",
        sendMessage
    );


    // ====================================
    // Enter Key
    // ====================================

    chatInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();

            }

        }
    );


    console.log(
        "🎉 AI Chat initialized successfully"
    );

});