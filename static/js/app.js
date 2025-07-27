// app/static/js/app.js

// Handles all frontend UI behavior for the Creative Agent form interface.
// Includes input handling, preview logic, fetch calls, animations, and easter eggs.

// DOM References
const form = document.getElementById('creative-form');
const inputTypeSelect = document.getElementById('input-type');
const textInputBlock = document.getElementById('text-input-block');
const fileInputBlock = document.getElementById('file-input-block');
const inputField = document.getElementById('input');
const fileInput = document.getElementById('file');
const previewImg = document.getElementById('preview-img');
const previewVideo = document.getElementById('preview-video');
const robotIcon = document.getElementById('robot-icon');
const genBtn = document.getElementById('submit-btn');
const surpriseBtn = document.getElementById('surprise-btn');
const clearBtn = document.getElementById('clear-btn');

// ================================
// Utility Functions
// ================================

function setButtonsDisabled(disabled) {
  document.querySelectorAll('.button-row button').forEach(btn => {
    btn.disabled = disabled;
    btn.classList.toggle('disabled', disabled);
  });
}

function clearOutput() {
  document.getElementById('output')?.remove();
  document.getElementById('copy-btn')?.remove();
  document.getElementById('download-btn')?.remove();
  document.querySelector('h2')?.remove();
}

function syntaxHighlight(json) {
  if (typeof json != "string") json = JSON.stringify(json, null, 2);
  json = json.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(?:\s*:)?|\b(true|false|null)\b|-?\d+(\.\d+)?)/g, match => {
    let cls = "json-number";
    if (/^"/.test(match)) {
      cls = /:$/.test(match) ? "json-key" : "json-string";
    } else if (/true|false/.test(match)) {
      cls = "json-boolean";
    }
    return `<span class="${cls}">${match}</span>`;
  });
}

// ================================
// Input Type Toggle
// ================================

function toggleInputType() {
  const type = inputTypeSelect.value;
  if (type === "text") {
    textInputBlock.style.display = "block";
    fileInputBlock.style.display = "none";
    surpriseBtn.style.display = "inline-block";
    clearBtn.style.display = "inline-block";
  } else {
    textInputBlock.style.display = "none";
    fileInputBlock.style.display = "block";
    surpriseBtn.style.display = "none";
    clearBtn.style.display = "none";
  }
}

// ================================
// File Preview
// ================================

function handleFilePreview(event) {
  const file = event.target.files[0];
  if (!file) return;
  previewImg.style.display = "none";
  previewVideo.style.display = "none";
  const reader = new FileReader();
  reader.onload = function(e) {
    if (file.type.startsWith("image/")) {
      previewImg.src = e.target.result;
      previewImg.style.display = "block";
    } else if (file.type.startsWith("video/")) {
      previewVideo.src = e.target.result;
      previewVideo.style.display = "block";
    }
  };
  reader.readAsDataURL(file);
}

// ================================
// Surprise Me
// ================================

async function fetchSurpriseBrief() {
  setButtonsDisabled(true);
  surpriseBtn.textContent = "Loading...";
  try {
    const res = await fetch('/surprise');
    const data = await res.json();
    inputField.value = data.brief;
    robotIcon.classList.add("robot-surprise");
    setTimeout(() => robotIcon.classList.remove("robot-surprise"), 600);
  } catch (err) {
    alert("Failed to load surprise brief!");
    console.error(err);
  } finally {
    surpriseBtn.textContent = "Surprise Me";
    setButtonsDisabled(false);
  }
}

// ================================
// Submit Handler
// ================================

async function handleFormSubmit(e) {
  e.preventDefault();
  setButtonsDisabled(true);
  document.getElementById('loading').style.display = 'block';
  const dotsEl = document.getElementById('dots');
  let dotCount = 1;
  window.loadingInterval = setInterval(() => {
    dotCount = (dotCount % 3) + 1;
    dotsEl.textContent = '.'.repeat(dotCount);
  }, 500);

  try {
    const inputType = inputTypeSelect.value;
    let response;

    if (inputType === 'text') {
      const text = inputField.value;
      response = await fetch('/plans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text }),
      });
    } else {
      const file = fileInput.files[0];
      if (!file) throw new Error('No file selected.');
      const formData = new FormData();
      formData.append('file', file);
      const isImage = file.type.startsWith("image/");
      const endpoint = isImage ? '/plans/from-image' : '/plans/from-video';
      response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });
    }

    const plan = await response.json();
    if (!response.ok) throw new Error(plan.detail || "Unknown error");
    window.rawJsonPlan = plan;
    clearOutput();

    const pre = document.createElement('pre');
    pre.id = 'output';
    const code = document.createElement('code');
    code.innerHTML = syntaxHighlight(plan);
    pre.appendChild(code);
    document.body.appendChild(document.createElement('h2')).textContent = "Generated Plan";
    document.body.appendChild(pre);

    createCopyAndDownloadButtons();
  } catch (err) {
    alert("Error: " + err.message);
    console.error(err);
  } finally {
    setButtonsDisabled(false);
    clearInterval(window.loadingInterval);
    document.getElementById('loading').style.display = 'none';
  }
}

// ================================
// Copy & Download
// ================================

function createCopyAndDownloadButtons() {
  const copyBtn = document.createElement('button');
  copyBtn.textContent = "Copy to Clipboard";
  copyBtn.id = "copy-btn";
  copyBtn.onclick = () => {
    const jsonString = JSON.stringify(window.rawJsonPlan, null, 2);
    navigator.clipboard.writeText(jsonString).then(() => {
      copyBtn.textContent = "✅ Copied!";
      setTimeout(() => copyBtn.textContent = "Copy to Clipboard", 1200);
    });
  };

  const downloadBtn = document.createElement('button');
  downloadBtn.textContent = "Download as JSON";
  downloadBtn.id = "download-btn";
  downloadBtn.onclick = () => {
    const jsonString = JSON.stringify(window.rawJsonPlan, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `creative_plan_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
    a.click();
    URL.revokeObjectURL(url);
    downloadBtn.textContent = "✅ Downloaded!";
    setTimeout(() => downloadBtn.textContent = "Download as JSON", 1200);
  };

  const buttonRow = document.createElement('div');
  buttonRow.className = 'button-row';
  buttonRow.appendChild(copyBtn);
  buttonRow.appendChild(downloadBtn);
  document.body.appendChild(buttonRow);
}

// ================================
// Placeholder Rotation
// ================================

const placeholderPrompts = [
  "A jellyfish who does stand-up comedy.",
  "A detective film where the suspect is the moon.",
  "A haunted toaster who wants to be a chef.",
  "A cowboy lost in a futuristic shopping mall.",
  "Two raccoons run a late-night radio show.",
];

let placeholderIndex = 0;
function rotatePlaceholder() {
  if (inputTypeSelect.value === "text") {
    inputField.placeholder = placeholderPrompts[placeholderIndex];
    placeholderIndex = (placeholderIndex + 1) % placeholderPrompts.length;
  }
}

// ================================
// Robot Icon Easter Egg
// ================================

let clickCount = 0;
let clickTimer = null;
function toggleRobotIcon() {
  const src = robotIcon.getAttribute("src");
  const base = "/static/icons/";
  const newSrc = src.includes("robot_brother.svg") ? base + "robot.svg" : base + "robot_brother.svg";
  robotIcon.setAttribute("src", newSrc);
}

// ================================
// Initialize Event Listeners
// ================================

function setupEventListeners() {
  form?.addEventListener("submit", handleFormSubmit);
  inputTypeSelect?.addEventListener("change", toggleInputType);
  fileInput?.addEventListener("change", handleFilePreview);
  surpriseBtn?.addEventListener("click", fetchSurpriseBrief);
  clearBtn?.addEventListener("click", () => {
    inputField.value = "";
    clearOutput();
  });
  genBtn?.addEventListener("mouseenter", () => robotIcon.classList.add("robot-hover-animate"));
  genBtn?.addEventListener("mouseleave", () => robotIcon.classList.remove("robot-hover-animate"));
  robotIcon?.addEventListener("click", () => {
    clickCount++;
    if (clickTimer) clearTimeout(clickTimer);
    clickTimer = setTimeout(() => clickCount = 0, 1000);
    if (clickCount === 5) {
      toggleRobotIcon();
      clickCount = 0;
    }
  });
  setInterval(rotatePlaceholder, 5000);
}

// Kickstart setup
setupEventListeners();
rotatePlaceholder();
