document.addEventListener("DOMContentLoaded", () => {
    // TAB SWITCHING
    const tabs = document.querySelectorAll(".tab-btn");
    const panels = document.querySelectorAll(".tab-panel");
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const target = tab.dataset.tab;
            // remove active from buttons
            tabs.forEach(btn => {
                btn.classList.remove("active");
            });
            // hide all panels
            panels.forEach(panel => {
                panel.classList.remove("active");
            });
            // activate clicked tab
            tab.classList.add("active");
            // show related panel
            const activePanel = document.getElementById(target);
            if(activePanel){
                activePanel.classList.add("active");
            }
        });
    });
    // UPLOAD BUTTON
    const uploadBtn = document.querySelector(".upload-btn");
    if(uploadBtn){
        uploadBtn.addEventListener("click", () => {
            window.location.href="/upload";
        });
    }
    // MEETING SELECTION UI
    const meetings = document.querySelectorAll(".meeting-item");
    meetings.forEach(meeting => {
        meeting.addEventListener("click", () => {
            meetings.forEach(item => {
                item.classList.remove("active");
            });
            meeting.classList.add("active");
        });
    });
});