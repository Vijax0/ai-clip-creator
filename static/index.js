const configForm = document.getElementById("config-form");

function updateSettings() {
    const configFormData = new FormData(configForm);

    fetch("/get-config", {
        method: "POST",
        body: configFormData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Settings updated successfully:", data);
    })
    .catch(error => {
        console.error("Error updating settings:", error);
    });
}

function saveSettings() {
    updateSettings();
    const configFormData = new FormData(configForm);

    fetch("/save-config", {
        method: "POST",
        body: configFormData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Successfully saved settings:", data);
    })
    .catch(error => {
        console.error("Error saving settings:", error);
    });
}

const inputs = configForm.querySelectorAll("input, select, textarea");
inputs.forEach(input => {
    input.addEventListener("change", updateSettings)
})

configForm.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
    }
});

document.getElementById("save-settings").addEventListener("click", saveSettings)

document.addEventListener("DOMContentLoaded", function() {
    const valueContainers = document.querySelectorAll(".value-container");

    valueContainers.forEach(container => {
        const numberInput = container.querySelector("input[type='number']");
        const rangeInput = container.querySelector("input[type='range']")

        if (!numberInput || !rangeInput) return;

        function enforceConstraints (input) {
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
            target.value = source.value
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

document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.querySelector("#video-upload form");
    const loadingBar = document.getElementById("loading-bar");

    loadingBar.style.display = "none";

    if (uploadForm) {
        uploadForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const fileInput = this.querySelector('input[type="file"]');
            if (fileInput.files.length === 0) {
                return;
            }

            loadingBar.style.display = "block";

            const formData = new FormData(this);

            fetch("/", {
                method: "POST",
                body: formData
            })
            .then(response => response.text())
            .then(html => {

                loadingBar.style.display = "none";

                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                
                const newClipContainer = doc.getElementById("clip-container");
                if (newClipContainer) {
                    document.getElementById("clip-container").innerHTML = newClipContainer.innerHTML;
                }
            })
            .catch(error => {
                loadingBar.style.display = "none";
                console.error("Error uploading video:", error);
            });
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("folder-icon").addEventListener("click", function() {
        const element = document.getElementById("clips-menu");
        if (element.style.right == "0rem") {
            element.style.right = "-10.5rem"
        } else {
            element.style.right = "0rem";
        };
    });
});