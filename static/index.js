const configForm = document.getElementById("config-form");

function updateSettings() {
  const configFormData = new FormData(configForm);

  fetch("/get-config", {
    method: "POST",
    body: configFormData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Settings updated successfully:", data);
    })
    .catch((error) => {
      console.error("Error updating settings:", error);
    });
}

function saveSettings() {
  updateSettings();
  const configFormData = new FormData(configForm);

  fetch("/save-config", {
    method: "POST",
    body: configFormData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Successfully saved settings:", data);
    })
    .catch((error) => {
      console.error("Error saving settings:", error);
    });
}

const inputs = configForm.querySelectorAll("input, select, textarea");
inputs.forEach((input) => {
  input.addEventListener("change", updateSettings);
});

configForm.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
  }
});

document
  .getElementById("save-settings")
  .addEventListener("click", saveSettings);

document.addEventListener("DOMContentLoaded", function () {
  const valueContainers = document.querySelectorAll(".value-container");

  valueContainers.forEach((container) => {
    const numberInput = container.querySelector("input[type='number']");
    const rangeInput = container.querySelector("input[type='range']");

    if (!numberInput || !rangeInput) return;

    function enforceConstraints(input) {
      const min = parseFloat(input.min);
      const max = parseFloat(input.max);
      let value = parseFloat(input.value);

      if (isNaN(value)) {
        value = min;
      } else if (value < min) {
        value = min;
      } else if (value > max) {
        value = max;
      }

      input.value = value;
    }

    function syncInputs(source, target) {
      target.value = source.value;
    }

    numberInput.addEventListener("input", function () {
      syncInputs(numberInput, rangeInput);
    });

    rangeInput.addEventListener("input", function () {
      syncInputs(rangeInput, numberInput);
    });

    numberInput.addEventListener("blur", function () {
      enforceConstraints(numberInput);
      syncInputs(numberInput, rangeInput);
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const uploadForm = document.querySelector("#video-upload form");
  const loadingBar = document.getElementById("loading-bar");
  const uploadStatus = document.getElementById("upload-status");
  const clipContainer = document.getElementById("clip-container");
  const uploadButton = document.getElementById("video-upload-button");

  loadingBar.style.display = "none";

  function renderClips(clips) {
    if (!clips || clips.length === 0) {
      clipContainer.innerHTML =
        "<p id='no-clips-message'>No clips were created for this video. Try lowering threshold or leniency settings.</p>";
      return;
    }

    const clipMarkup = clips
      .map((clipPath) => {
        const encodedPath = clipPath
          .split("/")
          .map(encodeURIComponent)
          .join("/");
        return `<video controls><source src="/static/${encodedPath}" type="video/mp4"></video>`;
      })
      .join("");

    clipContainer.innerHTML = clipMarkup;
  }

  if (uploadForm) {
    uploadForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const fileInput = this.querySelector('input[type="file"]');
      if (fileInput.files.length === 0) {
        uploadStatus.textContent =
          "Please select an MP4 video before uploading.";
        uploadStatus.dataset.state = "error";
        return;
      }

      uploadButton.disabled = true;
      loadingBar.style.display = "block";
      uploadStatus.textContent =
        "Uploading and processing video. This may take a while...";
      uploadStatus.dataset.state = "info";

      const formData = new FormData(this);

      fetch("/", {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
        body: formData,
      })
        .then(async (response) => {
          const payload = await response.json();
          if (!response.ok || payload.status !== "success") {
            throw new Error(payload.message || "Upload failed.");
          }
          return payload;
        })
        .then((payload) => {
          renderClips(payload.clips);
          uploadStatus.textContent =
            "Upload complete. Clips are now available below.";
          uploadStatus.dataset.state = "success";
        })
        .catch((error) => {
          uploadStatus.textContent =
            error.message || "Upload failed due to an unknown error.";
          uploadStatus.dataset.state = "error";
          console.error("Error uploading video:", error);
        })
        .finally(() => {
          loadingBar.style.display = "none";
          uploadButton.disabled = false;
        });
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("folder-icon").addEventListener("click", function () {
    const element = document.getElementById("clips-menu");
    if (element.style.right == "0rem") {
      element.style.right = "-10.5rem";
    } else {
      element.style.right = "0rem";
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const folderNames = document.querySelectorAll(".folder-name");

  folderNames.forEach((folderName) => {
    folderName.addEventListener("click", function () {
      this.classList.toggle("expanded");
      this.nextElementSibling.classList.toggle("show");
    });
  });
});
