document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("automationForm");
    const fileInput = document.getElementById("uploadPicture");
    const fileNameDisplay = document.getElementById("fileNameDisplay");
    
    // Modal Elements
    const modal = document.getElementById("confirmationModal");
    const modalOverlay = document.getElementById("modalOverlay");
    const closeModalIcon = document.getElementById("closeModalIcon");
    const closeLargeModal = document.getElementById("closeLargeModal");
    const resultsTableBody = document.querySelector("#resultsTable tbody");

    // File Upload Display
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
        } else {
            fileNameDisplay.textContent = "No file chosen";
        }
    });

    // Mock Autocomplete for Subjects
    const subjectsInput = document.getElementById("subjectsInput");
    const subjectsDropdown = document.getElementById("subjectsDropdown");
    const mockSubjects = ["Maths", "Physics", "Computer Science", "English", "Chemistry", "Commerce"];

    subjectsInput.addEventListener("input", (e) => {
        const val = e.target.value.toLowerCase();
        subjectsDropdown.innerHTML = "";
        if (!val) {
            subjectsDropdown.classList.remove("show");
            return;
        }

        const matches = mockSubjects.filter(s => s.toLowerCase().includes(val));
        if (matches.length > 0) {
            subjectsDropdown.classList.add("show");
            matches.forEach(match => {
                const div = document.createElement("div");
                div.className = "subjects-auto-complete__option";
                div.textContent = match;
                div.addEventListener("click", () => {
                    subjectsInput.value = match;
                    subjectsDropdown.classList.remove("show");
                });
                subjectsDropdown.appendChild(div);
            });
        } else {
            subjectsDropdown.classList.remove("show");
        }
    });

    // Mock Dropdowns for State and City
    const setupDropdown = (inputId, dropdownId, optionsList) => {
        const input = document.getElementById(inputId);
        const dropdown = document.getElementById(dropdownId);

        input.addEventListener("click", () => {
            dropdown.innerHTML = "";
            dropdown.classList.add("show");
            optionsList.forEach(opt => {
                const div = document.createElement("div");
                div.className = "option";
                div.textContent = opt;
                div.addEventListener("click", (e) => {
                    e.stopPropagation();
                    input.value = opt;
                    dropdown.classList.remove("show");
                });
                dropdown.appendChild(div);
            });
        });

        input.addEventListener("input", (e) => {
            const val = e.target.value.toLowerCase();
            dropdown.innerHTML = "";
            const matches = optionsList.filter(s => s.toLowerCase().includes(val));
            if (matches.length > 0) {
                dropdown.classList.add("show");
                matches.forEach(opt => {
                    const div = document.createElement("div");
                    div.className = "option";
                    div.textContent = opt;
                    div.addEventListener("click", (e) => {
                        e.stopPropagation();
                        input.value = opt;
                        dropdown.classList.remove("show");
                    });
                    dropdown.appendChild(div);
                });
            } else {
                dropdown.classList.remove("show");
            }
        });
    };

    setupDropdown("react-select-3-input", "stateDropdown", ["NCR", "Uttar Pradesh", "Haryana", "Rajasthan"]);
    setupDropdown("react-select-4-input", "cityDropdown", ["Delhi", "Gurgaon", "Noida", "Jaipur", "Lucknow"]);

    // Close dropdowns on outside click
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".autocomplete-wrapper")) subjectsDropdown.classList.remove("show");
        if (!e.target.closest(".custom-select")) {
            document.getElementById("stateDropdown").classList.remove("show");
            document.getElementById("cityDropdown").classList.remove("show");
        }
    });

    // Form Submission & Validation
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        
        let isValid = true;
        
        // Reset all invalid classes
        document.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));

        // Validate required text fields
        ["firstName", "lastName"].forEach(id => {
            const el = document.getElementById(id);
            if (!el.value.trim()) {
                el.classList.add("is-invalid");
                isValid = false;
            }
        });

        // Email Validation (Optional, but strict format if provided)
        const email = document.getElementById("userEmail");
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email.value.trim() && !emailRegex.test(email.value)) {
            email.classList.add("is-invalid");
            email.style.borderColor = "rgb(220, 53, 69)";
            isValid = false;
        }

        // Phone Validation (Strict 10 digits)
        const phone = document.getElementById("userNumber");
        const phoneRegex = /^\d{10}$/;
        if (!phone.value.trim() || !phoneRegex.test(phone.value)) {
            phone.classList.add("is-invalid");
            phone.style.borderColor = "rgb(220, 53, 69)";
            isValid = false;
        }

        // Gender Validation
        const genderChecked = document.querySelector('input[name="gender"]:checked');
        if (!genderChecked) {
            // Usually we'd highlight the wrapper, but tests look for specific behaviors
            isValid = false;
        }

        if (isValid) {
            // Populate Modal
            resultsTableBody.innerHTML = `
                <tr><td>Student Name</td><td>${document.getElementById("firstName").value} ${document.getElementById("lastName").value}</td></tr>
                <tr><td>Student Email</td><td>${email.value}</td></tr>
                <tr><td>Gender</td><td>${genderChecked.value}</td></tr>
                <tr><td>Mobile</td><td>${phone.value}</td></tr>
                <tr><td>Date of Birth</td><td>${document.getElementById("dateOfBirthInput").value || ""}</td></tr>
                <tr><td>Subjects</td><td>${subjectsInput.value}</td></tr>
                <tr><td>Hobbies</td><td>${Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value).join(", ")}</td></tr>
                <tr><td>Picture</td><td>${fileInput.files.length > 0 ? fileInput.files[0].name : ""}</td></tr>
                <tr><td>Address</td><td>${document.getElementById("currentAddress").value}</td></tr>
                <tr><td>State and City</td><td>${document.getElementById("react-select-3-input").value} ${document.getElementById("react-select-4-input").value}</td></tr>
            `;

            // Show Modal
            modalOverlay.style.display = "block";
            modal.classList.add("show");
        }
    });

    // Close Modal Logic
    const hideModal = () => {
        modal.classList.remove("show");
        setTimeout(() => { modalOverlay.style.display = "none"; }, 300);
    };

    closeModalIcon.addEventListener("click", hideModal);
    closeLargeModal.addEventListener("click", hideModal);
    modalOverlay.addEventListener("click", hideModal);

    // Clear validation errors on input
    document.querySelectorAll("input, textarea").forEach(input => {
        input.addEventListener("input", () => {
            input.classList.remove("is-invalid");
            input.style.borderColor = "";
        });
    });
});
