// main.js
// Author: William Richmond
// Date: 2024-12-01
// Class: CYBR-260-45
// Assignment: Final Project
// Description: Handles interactivity for the SecureFileGuard HTML interface.
// Revised on: 2024-12-08

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed.");

    // Get elements
    const fileInput = document.getElementById("file-input");
    const uploadButton = document.getElementById("upload-button");
    const uploadArea = document.getElementById("upload-area");
    const resultsContainer = document.getElementById("results-container");

    // Check if required elements exist
    if (!fileInput || !uploadButton || !uploadArea || !resultsContainer) {
        console.error("One or more required elements are missing in the DOM.");
        return;
    }

    // Function: handleFileUpload
    // Purpose: Processes file selection and uploads it to the backend.
    // Inputs:
    //   - file (File): The selected file to upload.
    // Returns: None
    async function handleFileUpload(file) {
        if (!file) {
            console.error("No file selected.");
            alert("No file selected.");
            return;
        }

        console.log("File selected for upload:", file.name);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/upload/upload", {
                method: "POST",
                body: formData,
            });

            console.log("Response received:", response);
            if (response.ok) {
                const result = await response.json();
                console.log("Upload result:", result);
                displayScanResults(result);
            } else {
                console.error("Failed to upload file:", response.statusText);
                alert("Failed to upload the file. Please try again.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("An error occurred while uploading the file.");
        }
    }

    // Function: displayScanResults
    // Purpose: Displays scan results in the UI.
    // Inputs:
    //   - result (Object): The scan results from the backend.
    // Returns: None
    function displayScanResults(result) {
        console.log("Displaying scan results:", result);

        const threat = result?.threat || "None detected";

        resultsContainer.innerHTML = `
            <h3>Scan Results</h3>
            <p>Status: ${result.status || "Unknown"}</p>
            <p>Threat: ${threat}</p>
        `;
    }

    // Event listener: File input change
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        handleFileUpload(file);
    });

    // Event listener: Upload button click
    uploadButton.addEventListener("click", () => {
        console.log("Upload button clicked.");
        const file = fileInput.files[0];
        handleFileUpload(file);
    });

    // Drag-and-Drop functionality for upload area
    uploadArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        uploadArea.classList.add("dragging");
    });

    uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("dragging");
    });

    uploadArea.addEventListener("drop", (event) => {
        event.preventDefault();
        uploadArea.classList.remove("dragging");

        const file = event.dataTransfer.files[0];
        if (file) {
            console.log("File dropped:", file.name);
            handleFileUpload(file);
        } else {
            alert("No file detected. Please try again.");
        }
    });

    uploadArea.addEventListener("click", () => {
        fileInput.click();
    });
});
