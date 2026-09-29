// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const form = document.getElementById("analyzerForm");
  const fileInput = document.getElementById("resumeFile");
  const dropZone = document.getElementById("dropZone");
  const dropZoneContent = document.getElementById("dropZoneContent");
  const selectedFile = document.getElementById("selectedFile");
  const fileNameDisplay = document.getElementById("fileName");
  const removeFileBtn = document.getElementById("removeFileBtn");
  const jobDescription = document.getElementById("jobDescription");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const errorAlert = document.getElementById("errorAlert");

  // Results & State Elements
  const placeholderState = document.getElementById("placeholderState");
  const loadingState = document.getElementById("loadingState");
  const resultsContent = document.getElementById("resultsContent");
  const resetBtn = document.getElementById("resetBtn");

  const scoreCircle = document.getElementById("scoreCircle");
  const scoreValue = document.getElementById("scoreValue");
  const scoreStatus = document.getElementById("scoreStatus");
  const scoreDescription = document.getElementById("scoreDescription");

  const skillsFoundList = document.getElementById("skillsFoundList");
  const missingSkillsList = document.getElementById("missingSkillsList");
  const recommendationsList = document.getElementById("recommendationsList");

  // --- File Drag and Drop & Selection ---

  // Handle file input change
  fileInput.addEventListener("change", (e) => {
    if (fileInput.files.length > 0) {
      handleFile(fileInput.files[0]);
    }
  });

  // Drag over effects
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
        fileInput.files = e.dataTransfer.files;
        handleFile(file);
      } else {
        showError("Only PDF files are supported. Please select a valid .pdf file.");
      }
    }
  });

  function handleFile(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      showError("Please upload a file with the .pdf extension.");
      clearFileSelection();
      return;
    }
    hideError();
    fileNameDisplay.textContent = file.name;
    dropZoneContent.style.display = "none";
    selectedFile.style.display = "flex";
  }

  // Remove selected file
  removeFileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    clearFileSelection();
  });

  function clearFileSelection() {
    fileInput.value = "";
    fileNameDisplay.textContent = "";
    selectedFile.style.display = "none";
    dropZoneContent.style.display = "block";
  }

  // --- Form Submission & API Call ---

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    // Basic frontend validations
    if (!fileInput.files || fileInput.files.length === 0) {
      showError("Please select a PDF resume to upload.");
      return;
    }

    const jobDescText = jobDescription.value.trim();
    if (!jobDescText) {
      showError("Please enter a target job description.");
      return;
    }

    // Set UI to loading state
    showLoading();

    // Prepare multipart form data
    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);
    formData.append("job_description", jobDescText);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "An error occurred during analysis.");
      }

      // Display results
      displayResults(data);
    } catch (err) {
      showError(err.message || "Failed to connect to backend server.");
      showPlaceholder();
    } finally {
      hideLoading();
    }
  });

  // --- UI Helper Functions ---

  function showLoading() {
    analyzeBtn.disabled = true;
    placeholderState.style.display = "none";
    resultsContent.style.display = "none";
    loadingState.style.display = "block";
  }

  function hideLoading() {
    analyzeBtn.disabled = false;
    loadingState.style.display = "none";
  }

  function showPlaceholder() {
    loadingState.style.display = "none";
    resultsContent.style.display = "none";
    placeholderState.style.display = "block";
  }

  function showError(message) {
    errorAlert.textContent = message;
    errorAlert.style.display = "block";
  }

  function hideError() {
    errorAlert.textContent = "";
    errorAlert.style.display = "none";
  }

  function displayResults(data) {
    const score = data.match_score ?? 0;
    const skillsFound = data.skills_found || [];
    const missingSkills = data.missing_skills || [];
    const recommendations = data.recommendations || [];

    // 1. Update Match Score Display
    scoreValue.textContent = `${score}%`;

    // Dynamic conic gradient circle
    let scoreColor = "#ef4444"; // red
    if (score >= 75) {
      scoreColor = "#10b981"; // green
      scoreStatus.textContent = "Great Match!";
      scoreDescription.textContent = "Your resume aligns well with key job requirements.";
    } else if (score >= 45) {
      scoreColor = "#f59e0b"; // yellow
      scoreStatus.textContent = "Moderate Match";
      scoreDescription.textContent = "Your resume has a good baseline, but has room for targeted improvements.";
    } else {
      scoreColor = "#ef4444"; // red
      scoreStatus.textContent = "Needs Improvement";
      scoreDescription.textContent = "Several critical requirements from the job description are missing.";
    }

    scoreCircle.style.background = `conic-gradient(${scoreColor} ${score * 3.6}deg, #e2e8f0 0deg)`;

    // 2. Render Skills Found
    skillsFoundList.innerHTML = "";
    if (skillsFound.length > 0) {
      skillsFound.forEach((skill) => {
        const tag = document.createElement("span");
        tag.className = "skill-tag skill-found";
        tag.innerHTML = `✓ ${escapeHtml(skill)}`;
        skillsFoundList.appendChild(tag);
      });
    } else {
      skillsFoundList.innerHTML = `<span class="no-skills">No specific matching skills found in catalog.</span>`;
    }

    // 3. Render Missing Skills
    missingSkillsList.innerHTML = "";
    if (missingSkills.length > 0) {
      missingSkills.forEach((skill) => {
        const tag = document.createElement("span");
        tag.className = "skill-tag skill-missing";
        tag.innerHTML = `+ ${escapeHtml(skill)}`;
        missingSkillsList.appendChild(tag);
      });
    } else {
      missingSkillsList.innerHTML = `<span class="no-skills">Great! No key skill gaps detected from the catalog.</span>`;
    }

    // 4. Render Recommendations
    recommendationsList.innerHTML = "";
    if (recommendations.length > 0) {
      recommendations.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        recommendationsList.appendChild(li);
      });
    } else {
      recommendationsList.innerHTML = `<li>Your resume is well aligned with this job post.</li>`;
    }

    // Show Results container
    placeholderState.style.display = "none";
    resultsContent.style.display = "block";
  }

  // Reset Button Handler
  resetBtn.addEventListener("click", () => {
    form.reset();
    clearFileSelection();
    hideError();
    showPlaceholder();
  });

  // Utility: Simple XSS protection for text rendering
  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
});
