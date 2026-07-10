// ==========================================
// Elements
// ==========================================

const steps = document.querySelectorAll(".step");
const progressBar = document.getElementById("progressBar");
const statusText = document.getElementById("statusText");
const meetingId = localStorage.getItem("meeting_id");
if (!meetingId) {
    alert("Meeting not found.");
    window.location.href = "/";
}

// ==========================================
// Step Messages
// ==========================================
const messages = [
    "Audio uploaded...",
    "Preparing audio...",
    "Transcribing speech...",
    "Analyzing meeting...",
    "Generating summary...",
    "Preparing final report..."
];
let currentStep = 0;


// ==========================================
// Update Progress UI
// ==========================================
function updateProgress(step) {
    if (step >= steps.length) return;
    for (let i = 0; i <= step; i++) {
        steps[i].classList.add("active");
        const icon = steps[i].querySelector(".icon");
        if (icon) {
            icon.innerHTML = "✓";
        }
    }
    const percentage = ((step + 1) / steps.length) * 100;
    progressBar.style.width = percentage + "%";
    statusText.innerText = messages[step];
}


// ==========================================
// Check Backend Status
// ==========================================
async function checkStatus() {
    try {
        const response = await fetch(`/meetings/${meetingId}`);
        if (!response.ok) {
            throw new Error("Unable to fetch meeting status.");
        }
        const meeting = await response.json();
        // Fake progress while backend works
        switch (meeting.status) {

    case "preprocessing":
        updateProgress(1);
        break;

    case "transcribing":
        updateProgress(2);
        break;

    case "chunking":
    case "analyzing":
        updateProgress(3);
        break;

    case "merging":
    case "generating_report":
        updateProgress(4);
        break;

    case "completed":
        break;
}
        // Completed
        if (meeting.status === "completed") {
            clearInterval(intervalId);
            updateProgress(messages.length - 1);
            progressBar.style.width= meeting.progress +"%";
            statusText.innerText = "Meeting Minutes Generated Successfully";
            setTimeout(() => {window.location.href = "/result";}, 1000);
        }
        // Failed
        if (meeting.status === "failed") {
            clearInterval(intervalId);
            statusText.innerText = "Processing Failed";
            alert("Meeting processing failed.");
        }
    }
    catch (error) {
        console.error(error);
    }
}


// ==========================================
// Start Polling
// ==========================================
updateProgress(0);
const intervalId = setInterval(checkStatus, 2000);