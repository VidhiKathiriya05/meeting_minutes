document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("chatInput");
    const sendButton = document.getElementById("sendBtn");
    const messages = document.getElementById("chatMessages");
    let meeting = null;
    let activeMeetingId = null;

    function resetChat(meetingName) {
        messages.replaceChildren();
        const empty = document.createElement("div");
        empty.className = "chat-empty";
        const title = document.createElement("h2");
        title.textContent = "Meeting AI Assistant";
        const description = document.createElement("p");
        description.textContent = `Ask anything about ${meetingName}. This chat is temporary and is only shown for this meeting.`;
        empty.append(title, description);
        messages.appendChild(empty);
        input.value = "";
    }

    window.addEventListener("meeting:selected", event => {
        meeting = event.detail;
        if (meeting.id !== activeMeetingId) {
            activeMeetingId = meeting.id;
            resetChat(meeting.original_filename || meeting.title || "this meeting");
        }
    });

    function addMessage(content, type) {
        const item = document.createElement("div");
        item.className = `chat-message ${type}`;
        item.textContent = content;
        messages.appendChild(item);
        messages.scrollTop = messages.scrollHeight;
        return item;
    }

    async function sendMessage() {
        const question = input.value.trim();
        if (!question) return;
        if (!meeting) { addMessage("Select an uploaded meeting before starting a chat.", "ai-message"); return; }
        if (meeting.status !== "completed") { addMessage("This audio is still processing. You can chat once processing is complete.", "ai-message"); return; }
        const requestedMeeting = meeting;
        messages.querySelector(".chat-empty")?.remove();
        addMessage(question, "user-message");
        input.value = "";
        sendButton.disabled = true;
        const loading = addMessage("Thinking...", "ai-message loading");
        try {
            const response = await fetch("/chat/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ meeting_id: requestedMeeting.id, question }) });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || "Chat request failed");
            loading.remove();
            if (activeMeetingId !== requestedMeeting.id) return;
            addMessage(data.answer || "No answer received.", "ai-message");
        } catch (error) {
            loading.remove();
            if (activeMeetingId !== requestedMeeting.id) return;
            addMessage(error.message || "Unable to connect with the meeting assistant.", "ai-message");
        } finally { sendButton.disabled = false; input.focus(); }
    }
    sendButton.addEventListener("click", sendMessage);
    input.addEventListener("keydown", event => { if (event.key === "Enter") sendMessage(); });
});
