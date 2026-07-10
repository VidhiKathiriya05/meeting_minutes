// ==========================================
// Elements
// ==========================================

const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("audioFile");
const meetingTitle = document.getElementById("meetingTitle");
const dropArea = document.getElementById("dropArea");
const selectedFile = document.getElementById("selectedFile");
const submitBtn = document.querySelector(".generate-btn");


// ==========================================
// Display Selected File
// ==========================================
function showFile(file) {
    if (!file) {
        selectedFile.textContent = "No file selected";
        return;
    }
    const size = (file.size / 1024 / 1024).toFixed(2);
    selectedFile.textContent = `${file.name} (${size} MB)`;
}


// ==========================================
// File Input
// ========================================
fileInput.addEventListener("change", function () {
    if (this.files.length > 0) {
        showFile(this.files[0]);
    }
});


// ==========================================
// Drag Over
// ==========================================
dropArea.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropArea.classList.add("active");
});


// ==========================================
// Drag Leave
// ==========================================
dropArea.addEventListener("dragleave", function () {
    dropArea.classList.remove("active");
});


// ==========================================
// Drop File
// ==========================================
dropArea.addEventListener("drop", function (e) {
    e.preventDefault();
    dropArea.classList.remove("active");
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        showFile(fileInput.files[0]);
    }
});


// ==========================================
// Browse Click
// ==========================================
dropArea.addEventListener("click", function () {
    fileInput.click();
});


// ==========================================
// Upload Form
// ==========================================
uploadForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const title = meetingTitle.value.trim();
    const file = fileInput.files[0];
    if (title === "") {
        alert("Please enter a meeting title.");
        meetingTitle.focus();
        return;
    }
    if (!file) {
        alert("Please select an audio file.");
        return;
    }
    const formData = new FormData();
    formData.append("title", title);
    formData.append("audio", file);
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }
        const data = await response.json();
        console.log("Upload Success:", data);
        localStorage.setItem("meeting_id", data.meeting_id);
        window.location.href = "/processing";
    }
    catch (error) {
        console.error(error);
        alert("Upload failed.\n\n" + error.message);
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Minutes';
    }
});