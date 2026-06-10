# 🚀 QA Automation Suite: End-to-End Testing Portfolio

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green?logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.x-yellow?logo=pytest&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Reporting-orange?logo=allure&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

Welcome to the **QA Automation Suite**! This project serves as a comprehensive portfolio piece demonstrating modern quality assurance and test automation techniques. It features a complete test framework designed to validate UI forms, file uploads, edge-case field validations, and full REST API workflows.

---

## 📋 Project Overview

This testing suite performs automated validation against two primary targets:
1. **Frontend UI Testing**: Uses [DemoQA Automation Practice Form](https://demoqa.com/automation-practice-form) to demonstrate robust UI interaction, element locating, state assertions, and dynamic error handling.
2. **Backend API Testing**: Uses [JSONPlaceholder](https://jsonplaceholder.typicode.com/) to demonstrate complete CRUD operations (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) without requiring external authentication keys.

---

## ✨ Key Features

- **End-to-End UI Automation**: Submits full web forms, handles popups/modals, and bypasses overlapping UI elements (e.g., sticky footer ads) using JavaScript execution.
- **Deep Field Validations**: Validates boundary value analysis, negative testing, and security payload injections (XSS) on input fields.
- **File Upload Testing**: Automates file selection and validates restrictions on file types (PDF, EXE, TXT) and sizes.
- **Complete REST API Suite**: Fully tests API response codes, JSON payloads, data integrity, and response times.
- **Beautiful Reporting**: Generates interactive HTML dashboards using **Allure**, complete with severity tags, feature mapping, and step-by-step logs.
- **CI/CD Integration**: Fully configured with **GitHub Actions** to automatically trigger the test suite on every push and pull request.

---

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **Browser Automation**: Selenium WebDriver, webdriver-manager
- **Test Framework**: Pytest
- **Reporting**: Allure-Pytest, Pytest-HTML
- **API Testing**: Requests
- **CI/CD Pipeline**: GitHub Actions

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Maheredd/form-qa-automation.git
   cd form-qa-automation
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Running the Tests

You can run the entire test suite, or target specific testing modules.

**Run All Tests:**
```bash
pytest tests/ -v
```

**Run Specific Modules:**
```bash
# Run only API tests
pytest tests/test_api.py -v

# Run only UI Field Validations
pytest tests/test_field_validations.py -v

# Run only File Upload tests
pytest tests/test_file_upload.py -v

# Run only Full Form Submissions
pytest tests/test_form_submission.py -v
```

---

## 📊 Generating Allure Reports

This suite is fully integrated with Allure to provide beautiful, management-ready test dashboards.

1. **Run tests and gather result data:**
   ```bash
   pytest tests/ -v --alluredir=reports/allure-results
   ```

2. **Serve the HTML Dashboard:**
   *(Requires Allure Commandline or npm)*
   ```bash
   npx allure-commandline serve reports/allure-results
   ```
   This will spin up a local server and automatically open the interactive dashboard in your default web browser.

---

## 📁 Project Structure

```text
├── .github/workflows/
│   └── test_pipeline.yml         # CI/CD Pipeline Configuration
├── tests/
│   ├── test_api.py               # REST API CRUD Test Cases
│   ├── test_field_validations.py # UI Negative/Boundary Input Tests
│   ├── test_file_upload.py       # UI File Upload/Restriction Tests
│   └── test_form_submission.py   # UI End-to-End Form Tests
├── reports/                      # Auto-generated Test Reports
├── .gitignore                    # Git tracking exclusions
├── conftest.py                   # Pytest fixtures and WebDriver setup
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🐛 Bugs Discovered

Because this suite is built to test real-world scenarios, it successfully catches existing bugs on the DemoQA platform. 
*Example findings from this suite include:*
- Form accepts invalid email formats (`plaintext`, `@nodomain.com`, `double@@email.com`) without throwing proper validation errors.
- Form throws an invalid border color on perfectly valid 10-digit phone numbers under certain submission conditions.

---
*Developed as a QA Automation Portfolio Project.*
