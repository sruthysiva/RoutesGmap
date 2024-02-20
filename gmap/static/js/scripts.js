function displayFileName(input) {
    var fileNameDisplay = document.getElementById("file-name-display");
    var warningMessage = document.getElementById("warning-message");
    if (input.files.length > 0) {
        fileNameDisplay.innerText = "Selected file: " + input.files[0].name;
        warningMessage.innerText = "";
    } else {
        fileNameDisplay.innerText = "";
        warningMessage.innerText = "Please select a file.";
    }
}

function validateForm() {
    var fileInput = document.getElementById("id_file");
    var warningMessage = document.getElementById("warning-message");
    if (fileInput.files.length === 0) {
        warningMessage.innerText = "Please select a file.";
        return false; // Prevent form submission
    } else {
        var fileName = fileInput.files[0].name;
        if (!isValidExtension(fileName)) {
            warningMessage.innerText = "Invalid file type. Please upload a CSV or Excel file.";
            return false; // Prevent form submission
        }
        warningMessage.innerText = "";
        return true; // Allow form submission
    }
}

function clearFileInput() {
    var fileInput = document.getElementById("id_file");
    var fileNameDisplay = document.getElementById("file-name-display");
    var warningMessage = document.getElementById("warning-message");

    fileInput.value = null;  // Clear the file input
    fileNameDisplay.innerText = "";
    warningMessage.innerText = "";
}

function isValidExtension(fileName) {
    var allowedExtensions = ['.csv', '.xls', '.xlsx'];
    return allowedExtensions.some(ext => fileName.toLowerCase().endsWith(ext));
}