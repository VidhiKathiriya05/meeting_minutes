document.addEventListener("DOMContentLoaded", () => {
    const state = { meetings: [], selectedId: null, selectedMeeting: null, poller: null, processingNavigationId: null };
    const uploadButton = document.querySelector(".upload-btn");
    const fileInput = document.getElementById("audioUpload");
    const meetingList = document.getElementById("meetingList");
    const searchInput = document.querySelector(".navbar input");
    const sidebarSearch = document.getElementById("sidebarSearch");
    const statValues = document.querySelectorAll(".stat-card .stat-value");
    const analyticsValues = document.querySelectorAll(".analytics-card .analytics-value");
    const analyticsBar = document.querySelector(".analytics-card .progress-fill");
    const insight = document.querySelector(".insight-box");

    function text(selector, value) {
        const element = document.querySelector(selector);
        if (element) element.textContent = value;
    }

    function formatDate(value) {
        return value ? new Date(value).toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" }) : "-";
    }

    function phase(status) {
        const names = {
            uploaded: "Uploaded", preprocessing: "Preparing audio", transcribing: "Transcribing audio",
            chunking: "Preparing analysis", analyzing: "Analyzing meeting", merging: "Creating summary",
            generating_report: "Preparing report", completed: "Completed", failed: "Processing failed"
        };
        return names[status] || "Processing";
    }

    function activateTab(tabName) {
        document.querySelectorAll(".tab-btn, .tab-panel").forEach(element => element.classList.remove("active"));
        document.querySelector(`.tab-btn[data-tab="${tabName}"]`)?.classList.add("active");
        document.getElementById(tabName)?.classList.add("active");
    }

    function listItems(target, values, emptyMessage) {
        target.innerHTML = "";
        const items = Array.isArray(values) ? values : [];
        if (!items.length) {
            const li = document.createElement("li");
            li.textContent = emptyMessage;
            target.appendChild(li);
            return;
        }
        items.forEach(value => {
            const li = document.createElement("li");
            li.textContent = typeof value === "string" ? value : (value.task || JSON.stringify(value));
            target.appendChild(li);
        });
    }

    function renderSidebar() {
        const query = (searchInput?.value || "").trim().toLowerCase();
        meetingList.innerHTML = "";
        const visible = state.meetings.filter(meeting => `${meeting.original_filename || ""} ${meeting.title}`.toLowerCase().includes(query));
        if (!visible.length) {
            meetingList.textContent = query ? "No matching uploads" : "No uploaded meetings";
            return;
        }
        const renderGroup = (label, meetings) => {
            if (!meetings.length) return;
            const heading = document.createElement("h4");
            heading.textContent = label;
            meetingList.appendChild(heading);
            meetings.forEach(meeting => renderMeetingItem(meeting));
        };
        const renderMeetingItem = meeting => {
            const item = document.createElement("div");
            item.className = `meeting-item${meeting.id === state.selectedId ? " active" : ""}`;
            const filename = meeting.original_filename || meeting.title;
            item.title = filename;
            item.addEventListener("click", () => selectMeeting(meeting.id));
            const name = document.createElement("span");
            name.className = "meeting-name";
            name.textContent = `📄  ${filename}`;
            const controls = document.createElement("span");
            controls.className = "meeting-controls";
            const toggle = document.createElement("button");
            toggle.className = "meeting-control meeting-menu-toggle";
            toggle.textContent = "...";
            toggle.title = "File actions";
            toggle.setAttribute("aria-label", "Open file actions");
            toggle.setAttribute("aria-expanded", "false");
            const menu = document.createElement("div");
            menu.className = "meeting-menu";
            const addAction = (label, action, danger = false) => {
                const button = document.createElement("button");
                button.textContent = label;
                if (danger) button.className = "danger";
                button.addEventListener("click", event => { event.stopPropagation(); menu.classList.remove("open"); action(); });
                menu.appendChild(button);
            };
            addAction("Rename", () => {
                const nextName = window.prompt("Rename uploaded file", filename);
                if (nextName !== null && nextName.trim() && nextName.trim() !== filename) updateMeeting(meeting.id, { filename: nextName.trim() });
            });
            addAction(meeting.pinned ? "Unpin" : "Pin", () => updateMeeting(meeting.id, { pinned: !meeting.pinned }));
            addAction("Delete", () => deleteMeeting(meeting.id, filename), true);
            toggle.addEventListener("click", event => {
                event.stopPropagation();
                document.querySelectorAll(".meeting-menu.open").forEach(openMenu => {
                    if (openMenu !== menu) {
                        openMenu.classList.remove("open");
                        openMenu.parentElement?.querySelector(".meeting-menu-toggle")?.setAttribute("aria-expanded", "false");
                    }
                });
                menu.classList.toggle("open");
                toggle.setAttribute("aria-expanded", menu.classList.contains("open").toString());
            });
            controls.append(toggle, menu);
            item.append(name, controls);
            meetingList.appendChild(item);
        };
        renderGroup("Pinned Files", visible.filter(meeting => meeting.pinned));
        renderGroup("All Files", visible.filter(meeting => !meeting.pinned));
    }

    function renderStats() {
        const total = state.meetings.length;
        const pending = state.meetings.filter(m => !["completed", "failed"].includes(m.status)).length;
        const completed = state.meetings.filter(m => m.status === "completed").length;
        [total, pending, completed, "Live"].forEach((value, i) => { if (statValues[i]) statValues[i].textContent = value; });
    }

    function renderActions(actions) {
        const container = document.getElementById("summaryActions");
        container.innerHTML = "";
        if (!actions?.length) {
            container.textContent = "No action items available.";
            return;
        }
        actions.forEach(action => {
            const row = document.createElement("div");
            row.className = "action-item";
            const task = document.createElement("span");
            task.textContent = typeof action === "string" ? action : `${action.task || "Action item"}${action.owner ? ` — ${action.owner}` : ""}`;
            const status = document.createElement("span");
            status.className = "status pending";
            status.textContent = typeof action === "object" && action.status ? action.status : "Pending";
            row.append(task, status);
            container.appendChild(row);
        });
    }

    function renderTranscript(meeting) {
        const container = document.querySelector(".transcript-container");
        if (!container) return;
        const speakerTranscript = meeting.speaker_transcript?.trim();
        const transcript = meeting.transcript?.trim();
        const card = document.createElement("div");
        card.className = "speaker-card";
        const heading = document.createElement("div");
        heading.className = "speaker-name";
        heading.textContent = speakerTranscript ? "Speaker Transcript" : "Transcript";
        const body = document.createElement("pre");
        body.textContent = speakerTranscript || transcript || (meeting.status === "completed" ? "No transcript available." : "Transcript will appear as soon as transcription is complete.");
        card.append(heading, body);
        container.replaceChildren(card);
    }

    function updateExports(meeting) {
        let card = document.getElementById("downloadCard");
        if (!card) {
            card = document.createElement("div");
            card.id = "downloadCard";
            card.className = "summary-card";
            card.innerHTML = '<h2>Downloads</h2><div class="overview-grid"><a class="upload-btn" id="downloadDocx">Download DOCX</a><a class="upload-btn" id="downloadPdf">Download PDF</a></div>';
            document.querySelector(".summary-container").appendChild(card);
        }
        const ready = meeting && meeting.status === "completed";
        card.hidden = !ready;
        if (ready) {
            document.getElementById("downloadDocx").href = `/meetings/${meeting.id}/docx`;
            document.getElementById("downloadPdf").href = `/meetings/${meeting.id}/pdf`;
        }
    }

    function renderMeeting(meeting) {
        state.selectedMeeting = meeting;
        text("#summaryTitle", meeting.title || "-");
        text("#summaryDate", formatDate(meeting.created_at));
        text("#summaryParticipants", meeting.participants?.length ? meeting.participants.join(", ") : "Not detected");
        text("#summaryText", meeting.summary || (meeting.status === "completed" ? "No summary was generated." : `${phase(meeting.status)} (${meeting.progress || 0}%).`));
        listItems(document.getElementById("summaryKeyPoints"), meeting.key_points, "No key points available.");
        renderActions(meeting.action_items);
        renderTranscript(meeting);

        const speakerCount = meeting.participants?.length || (meeting.speaker_transcript ? new Set((meeting.speaker_transcript.match(/Speaker\s+\d+/gi) || [])).size : 0);
        if (analyticsValues[0]) analyticsValues[0].textContent = phase(meeting.status);
        if (analyticsValues[1]) analyticsValues[1].textContent = speakerCount || "-";
        if (analyticsValues[2]) analyticsValues[2].textContent = meeting.action_items?.length || 0;
        if (analyticsValues[3]) analyticsValues[3].textContent = `${meeting.progress || 0}%`;
        if (analyticsBar) analyticsBar.style.width = `${meeting.progress || 0}%`;
        if (insight) insight.innerHTML = `AI Insight:<br>${meeting.status === "completed" ? (meeting.summary || "Meeting analysis is ready.") : `${phase(meeting.status)} — ${meeting.progress || 0}% complete.`}`;
        updateExports(meeting);
        if (meeting.id === state.processingNavigationId) {
            if (meeting.status === "completed") {
                activateTab("summary");
                state.processingNavigationId = null;
            } else if (meeting.status !== "failed") {
                activateTab("analytics");
            }
        }
        window.dispatchEvent(new CustomEvent("meeting:selected", { detail: meeting }));
    }

    async function selectMeeting(id) {
        state.selectedId = id;
        localStorage.setItem("meeting_id", id);
        renderSidebar();
        try {
            const response = await fetch(`/meetings/${id}`);
            if (!response.ok) throw new Error("Unable to load meeting");
            const meeting = await response.json();
            renderMeeting(meeting);
        } catch (error) {
            console.error(error);
            text("#summaryText", "Unable to load this meeting.");
        }
    }

    async function updateMeeting(id, changes) {
        try {
            const response = await fetch(`/meetings/${id}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(changes)
            });
            const payload = await response.json();
            if (!response.ok) throw new Error(payload.detail || "Unable to update file");
            await refreshMeetings();
            if (id === state.selectedId) await selectMeeting(id);
        } catch (error) {
            alert(error.message || "Unable to update file.");
        }
    }

    async function deleteMeeting(id, filename) {
        if (!window.confirm(`Delete “${filename}”? This permanently removes its uploaded audio and generated reports.`)) return;
        try {
            const response = await fetch(`/meetings/${id}`, { method: "DELETE" });
            if (!response.ok) {
                const payload = await response.json();
                throw new Error(payload.detail || "Unable to delete file");
            }
            if (state.selectedId === id) {
                state.selectedId = null;
                state.selectedMeeting = null;
                localStorage.removeItem("meeting_id");
            }
            await refreshMeetings();
            const nextMeeting = state.meetings[0];
            if (nextMeeting) await selectMeeting(nextMeeting.id);
        } catch (error) {
            alert(error.message || "Unable to delete file.");
        }
    }

    async function refreshMeetings() {
        const response = await fetch("/meetings/");
        if (!response.ok) throw new Error("Unable to load meetings");
        state.meetings = await response.json();
        renderStats();
        renderSidebar();
        if (state.selectedId) await selectMeeting(state.selectedId);
    }

    async function upload(file) {
        const title = file.name.replace(/\.[^/.]+$/, "") || file.name;
        const data = new FormData();
        data.append("title", title);
        data.append("audio", file);
        uploadButton.disabled = true;
        uploadButton.textContent = "Uploading...";
        try {
            const response = await fetch("/upload", { method: "POST", body: data });
            const payload = await response.json();
            if (!response.ok) throw new Error(payload.detail || "Upload failed");
            state.processingNavigationId = payload.meeting_id;
            await refreshMeetings();
            await selectMeeting(payload.meeting_id);
        } catch (error) {
            alert(error.message || "Upload failed.");
        } finally {
            uploadButton.disabled = false;
            uploadButton.textContent = "+ Upload Meeting";
            fileInput.value = "";
        }
    }

    document.querySelectorAll(".tab-btn").forEach(tab => tab.addEventListener("click", () => {
        activateTab(tab.dataset.tab);
    }));
    uploadButton.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", () => fileInput.files[0] && upload(fileInput.files[0]));
    searchInput?.addEventListener("input", renderSidebar);
    sidebarSearch.addEventListener("click", () => searchInput?.focus());
    document.addEventListener("click", () => document.querySelectorAll(".meeting-menu.open").forEach(menu => {
        menu.classList.remove("open");
        menu.parentElement?.querySelector(".meeting-menu-toggle")?.setAttribute("aria-expanded", "false");
    }));

    (async () => {
        try {
            await refreshMeetings();
            const savedId = Number(localStorage.getItem("meeting_id"));
            const initial = state.meetings.find(m => m.id === savedId) || state.meetings[0];
            if (initial) {
                if (initial.status !== "completed" && initial.status !== "failed") state.processingNavigationId = initial.id;
                await selectMeeting(initial.id);
            }
        } catch (error) { console.error(error); }
        state.poller = setInterval(refreshMeetings, 4000);
    })();
});
