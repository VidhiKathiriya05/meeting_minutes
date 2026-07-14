const meetingId = localStorage.getItem("meeting_id");
if (!meetingId) {
    alert("Meeting ID not found.");
    window.location.href = "/";
}
async function loadMeeting() {
    try {
        const response = await fetch(`/meetings/${meetingId}`);
        if (!response.ok) {
            throw new Error("Unable to load meeting.");
        }
        const meeting = await response.json();
        console.log(meeting);
        console.log(meeting.speaker_transcript);
        console.log("Transcript:", meeting.transcript);
        
        // ===========================
        // Basic Information
        // ===========================
        document.getElementById("meetingTitle").textContent =
            meeting.title || "-";
        document.getElementById("meetingDate").textContent =
            new Date(meeting.created_at).toLocaleDateString();
        document.getElementById("meetingDuration").textContent =
            "Processed Audio";
        document.getElementById("participants").textContent =
            meeting.participants?.join(", ") || "N/A";
        
        if (meeting.summary && typeof meeting.summary === "object") {
            // Fallback for older meetings saved before the summary format was fixed
            const s = meeting.summary;
            document.getElementById("summary").innerHTML = `
                <p><strong>Objective:</strong> ${s.meeting_objective || "-"}</p>
                <p><strong>Discussion:</strong> ${s.main_discussion || "-"}</p>
                <p><strong>Conclusions:</strong> ${s.important_conclusions || "-"}</p>
                <p><strong>Outcome:</strong> ${s.final_outcome || "-"}</p>
            `;

        } else if (meeting.summary && typeof meeting.summary === "string" && meeting.summary.trim() !== "") {
            // Current format: summary is a single paragraph string
            document.getElementById("summary").innerHTML = `<p>${meeting.summary}</p>`;

        } else {
            document.getElementById("summary").textContent = "No summary available.";
        }
        // Helper Function
        // ===========================
        function populateList(id, items) {
            const element = document.getElementById(id);
            element.innerHTML = "";
            if (!items || items.length === 0) {
                element.innerHTML = "<li>None</li>";
                return;
            }
            items.forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                element.appendChild(li);
            });
        }
        populateList("keyPoints", meeting.key_points);
        populateList("decisions", meeting.decisions);
        populateList("questions", meeting.questions);
        populateList("risks", meeting.risks);
        populateList("nextSteps", meeting.next_steps);

        // ===========================
        // Action Items
        // ===========================
        const actionTable = document.getElementById("actionItems");
        actionTable.innerHTML = "";
        if (meeting.action_items && meeting.action_items.length > 0) {
            meeting.action_items.forEach(action => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${action.owner || "-"}</td>
                    <td>${action.task || "-"}</td>
                    <td>${action.status || "-"}</td>
                `;
                actionTable.appendChild(row);
            });
        }

        // ===========================
        // Transcript
        // ===========================
                const transcript = document.getElementById("transcript");
        transcript.innerHTML = "";

        if (meeting.speaker_transcript) {
            const div = document.createElement("div");
            div.className = "speaker-card";

            div.innerHTML = `
                <div class="speaker-name">Speaker Transcript</div>
                <pre>${meeting.speaker_transcript}</pre>
            `;

            transcript.appendChild(div);

        } else if (meeting.transcript) {
            const div = document.createElement("div");
            div.className = "speaker-card";

            div.innerHTML = `
                <div class="speaker-name">Transcript</div>
                <pre>${meeting.transcript}</pre>
            `;

            transcript.appendChild(div);
        }

    } catch (error) {
        console.error(error);
        alert("Failed to load meeting.");
    }
}

loadMeeting();
// ===========================
// Export Buttons
// ===========================
document.querySelector(".pdf-btn").addEventListener("click", () => {
    window.location.href = `/meetings/${meetingId}/pdf`;
});
document.querySelector(".doc-btn").addEventListener("click", () => {
    window.location.href = `/meetings/${meetingId}/docx`;
});