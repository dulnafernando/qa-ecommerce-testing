# E-Commerce QA Automation & Manual Testing Framework

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.58+-green?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![pytest](https://img.shields.io/badge/pytest-8.0+-blue?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Postman](https://img.shields.io/badge/Postman-v10+-orange?logo=postman&logoColor=white)](https://www.postman.com/)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Automated%20CI-brightgreen?logo=githubactions&logoColor=white)](.github/workflows/tests.yml)
[![Tests](https://img.shields.io/badge/Tests-21%20Passed-success)](#-test-metrics--execution-summary)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An end-to-end, production-grade Quality Assurance testing portfolio targeting [Automation Exercise](https://automationexercise.com) — a full-scale e-commerce platform with web UI and RESTful API backends.

This repository demonstrates the complete QA engineering lifecycle: **Manual Test Design (Scenarios, Boundary Value Analysis, Severity vs. Priority Triage)**, **Real-World Defect Discovery**, **UI Automation with Playwright (Page Object Model)**, **Data-Driven Testing**, **Dual-Layer REST API Testing (Postman + Python `requests`)**, and **Continuous Integration (GitHub Actions)**.

---

## 📑 Table of Contents
1. [Core Architectural Highlights & QA Thinking](#-core-architectural-highlights--qa-thinking)
2. [Test Metrics & Execution Summary](#-test-metrics--execution-summary)
3. [Repository Directory Structure](#-repository-directory-structure)
4. [Manual QA & Real Defect Discovery](#-manual-qa--real-defect-discovery)
5. [UI Automation & Page Object Model (POM)](#-ui-automation--page-object-model-pom)
6. [API Testing: Postman to Python Automation](#-api-testing-postman-to-python-automation)
7. [Failure Diagnostics & Test Reporting](#-failure-diagnostics--test-reporting)
8. [Cross-Browser Verification](#-cross-browser-verification)
9. [Quickstart & Execution Guide](#-quickstart--execution-guide)
10. [CI/CD Pipeline (GitHub Actions)](#-cicd-pipeline-github-actions)
11. [Engineering Retrospective & Future Roadmap](#-engineering-retrospective--future-roadmap)

---

## 🎯 Core Architectural Highlights & QA Thinking

### 1. Strict Page Object Model (POM) Separation
- **Pages (`pages/`)**: Encapsulate locators, browser interactions, and action methods. Pages **never** assert business state.
- **Tests (`tests/`)**: Hold pure test logic and assertions. If a locator or DOM structure changes, only the corresponding Page class is modified, ensuring 100% test maintenance scalability.

### 2. Defensive Automation (AJAX & Dynamic DOM Handling)
- Avoids arbitrary `time.sleep()`.
- Uses Playwright's auto-waiting locators and explicit lifecycle states (e.g., `locator.wait_for(state="detached")` for asynchronous cart deletions to prevent race conditions).
- Distinguishes between native HTML5 client-side constraints (`el.checkValidity() == False`) and server-rendered error banners.

### 3. Business Logic & Mathematical Verification
- Tests don't just verify that static text appears; they verify mathematical business logic.
- Cart and checkout tests parse unit prices, quantities, and composite subtotals to verify that $\text{Price} \times \text{Quantity} == \text{Line Total}$ and $\sum \text{Line Totals} == \text{Order Total}$.

### 4. Zero Fabricated Bugs Policy
- **Every bug report in this project reflects a real, verified defect on the live website.**
- Discovered and documented critical bugs including negative order totals (`Rs. -100`), REST API RFC 9110 transport status code violations, and accessibility compliance issues.

---

## 📊 Test Metrics & Execution Summary

| Test Layer | Test Module | Cases | Execution Engine | Status | Typical Runtime |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **UI Smoke** | `tests/ui/test_smoke.py` | 1 | Playwright (Chromium) | **PASS** | ~3s |
| **UI Auth** | `tests/ui/test_login.py` | 5 | Playwright + Data-Driven JSON | **PASS** | ~38s |
| **UI Cart** | `tests/ui/test_cart.py` | 2 | Playwright (Catalog $\to$ Cart) | **PASS** | ~30s |
| **UI Checkout** | `tests/ui/test_checkout.py` | 3 | Playwright (Cart $\to$ Pay $\to$ Confirm) | **PASS** | ~45s |
| **REST API** | `tests/api/test_products_api.py` | 5 | Python `requests` + `pytest` | **PASS** | ~8s |
| **REST API** | `tests/api/test_auth_api.py` | 5 | Python `requests` + `pytest` | **PASS** | ~9s |
| **TOTAL** | **Full Automated Suite** | **21** | **pytest Runner** | **100% PASS** | **~130s** |

---

## 📂 Repository Directory Structure

```text
qa-ecommerce-testing/
├── .github/
│   └── workflows/
│       └── tests.yml                  # GitHub Actions CI workflow (runs on push/PR)
├── docs/
│   └── cross_browser_testing.md       # Comparative findings across Chromium, Firefox & WebKit
├── manual-testing/
│   ├── test-scenarios.md              # High-level E2E user journeys & scenario matrices
│   ├── test-cases/                    # Structured test cases with traceability
│   │   ├── README.md                  # Test case repository index & execution summary
│   │   ├── TC_Authentication.md       # Login, security & session termination cases
│   │   ├── TC_Products_Catalog.md     # Catalog browsing, search & BVA quantity cases
│   │   ├── TC_Cart_Checkout.md        # Multi-item cart, AJAX deletion & checkout cases
│   │   └── TC_REST_API.md             # Status code, schema & method validation cases
│   └── bug-reports/                   # Real, reproducible defect documentation
│       ├── README.md                  # Defect triage & Severity vs. Priority interview guide
│       ├── BUG-001-negative-order-total-checkout.md
│       ├── BUG-002-api-returns-200-on-client-and-method-errors.md
│       ├── BUG-003-catalog-add-to-cart-missing-href-accessibility.md
│       └── BUG-004-cart-removal-missing-confirmation-and-undo.md
├── pages/                             # Page Object Model classes
│   ├── base_page.py                   # Common navigation and timeout abstractions
│   ├── login_page.py                  # Authentication form interactions
│   ├── products_page.py               # Catalog cards, search & category filters
│   ├── cart_page.py                   # Dynamic cart table, quantities & deletions
│   ├── checkout_page.py               # Address review, order summary & comments
│   └── payment_page.py                # Payment gateway inputs & confirmation
├── postman/                           # Manual API testing suite
│   ├── Automation_Exercise_API.postman_collection.json  # 10 requests with test scripts
│   └── Automation_Exercise.postman_environment.json     # Variable definitions
├── reports/                           # Test execution HTML reports
│   └── report.html                    # Self-contained pytest-html execution report
├── screenshots/                       # Automated failure captures (gitignored)
├── test_data/                         # Data-driven test fixtures
│   └── login_data.json                # Parameterized valid & invalid credentials
├── tests/
│   ├── api/                           # Automated Python API tests (requests)
│   │   ├── __init__.py
│   │   ├── test_auth_api.py           # Login verification & user profile endpoints
│   │   └── test_products_api.py       # Product catalog, brands & search endpoints
│   └── ui/                            # End-to-end browser tests (Playwright)
│       ├── test_smoke.py              # Application availability sanity check
│       ├── test_login.py              # Parameterized authentication tests
│       ├── test_cart.py               # Cart aggregation & deletion tests
│       └── test_checkout.py           # Order placement & financial calculation tests
├── conftest.py                        # Pytest fixtures & screenshot-on-failure hook
├── pytest.ini                         # Pytest configuration, markers & report flags
├── requirements.txt                   # Locked production & test dependencies
└── README.md                          # Project documentation
```

---

## 🔍 Manual QA & Real Defect Discovery

A core distinction in QA interviews is demonstrating **analytical testing mindset** beyond just writing scripts. This project includes full manual test design and bug reporting for real defects found during exploratory testing.

### Severity vs. Priority Framework
- **Severity (Technical Impact)**: How deeply the bug damages application functionality or architecture (Critical, Major, Medium, Low).
- **Priority (Business Urgency)**: How quickly the defect must be fixed based on user exposure and business risk (P1 - Immediate, P2 - High, P3 - Medium, P4 - Low).

### Defect Showcase

| Bug ID | Title | Severity | Priority | Root Cause Summary |
| :--- | :--- | :---: | :---: | :--- |
| [**BUG-001**](manual-testing/bug-reports/BUG-001-negative-order-total-checkout.md) | **Negative Order Totals at Checkout** | **Critical** | **P1** | `#quantity` input lacks `min="1"` validation and server lacks positive integer check, allowing a negative balance (`Rs. -100`) to be checked out. |
| [**BUG-002**](manual-testing/bug-reports/BUG-002-api-returns-200-on-client-and-method-errors.md) | **API Returns 200 OK for 4xx Errors** | **Major** | **P2** | Transport layer returns `HTTP 200 OK` on `400`, `404`, and `405` errors, embedding codes in JSON body. Violates RFC 9110 and breaks API gateway monitoring. |
| [**BUG-003**](manual-testing/bug-reports/BUG-003-catalog-add-to-cart-missing-href-accessibility.md) | **Add to Cart Buttons Lack `href`** | **Medium** | **P3** | Anchor tags `<a class="add-to-cart">` lack `href` attribute, stripping them of `role="link"` and breaking keyboard Tab traversal and screen readers. |
| [**BUG-004**](manual-testing/bug-reports/BUG-004-cart-removal-missing-confirmation-and-undo.md) | **Cart Item Deletion Lacks Confirmation** | **Low** | **P3** | Asynchronous AJAX removal detaches row instantly without confirmation modal or toast "Undo" window. |

---

## 🌐 UI Automation & Page Object Model (POM)

The browser automation suite utilizes **Playwright for Python**, capitalizing on native auto-waiting, browser context isolation, and multi-engine support.

### Key Implementation Patterns
1. **The Phase 4 Locator Resolution**: On `/products`, "Add to Cart" links exist in duplicate (one in static `.productinfo` and one in hover `.product-overlay`). By targeting `.productinfo .add-to-cart`, tests avoid element ambiguity and hover-flakiness.
2. **Data-Driven Parameterization**: `test_login.py` runs 5 test cases from `login_data.json` via `@pytest.mark.parametrize`:
   - Valid registered credentials.
   - Non-existent user email.
   - Incorrect password for registered user.
   - Missing email input.
   - Missing password input.
3. **Financial Assertions**:
   ```python
   # tests/ui/test_checkout.py
   calculated_subtotal = sum(item["total"] for item in line_items)
   assert calculated_subtotal == invoice_total, "Order total does not match line item sum!"
   ```

---

## ⚡ API Testing: Postman to Python Automation

The API testing strategy follows a two-tier model:

1. **Postman Collection (`postman/`)**:
   - 10 structured requests across Products, Brands, Search, and Auth.
   - Pre-configured environment variables (`baseUrl`).
   - JavaScript assertions (`pm.test`) verifying HTTP status, JSON schema, and message payloads.
2. **Automated Python API Suite (`tests/api/`)**:
   - Implemented via `requests` and `pytest`.
   - Dual-layer assertion pattern to handle the target application's status code quirk:
     ```python
     assert response.status_code == 200, "Transport HTTP status failed"
     data = response.json()
     assert data.get("responseCode") == 404, "Domain status failed"
     assert data.get("message") == "User not found!"
     ```
   - Enables blazing-fast execution (~17 seconds for 10 tests) without third-party CLI dependencies.

---

## 📸 Failure Diagnostics & Test Reporting

### 1. Automatic Failure Screenshots
Configured in `conftest.py` using `pytest_runtest_makereport`:
- Listens to pytest's test-execution phase.
- If a test fails in the `"call"` phase and has access to a Playwright `page` fixture, it captures a full-page PNG screenshot saved to `screenshots/<test_name>_<timestamp>.png`.
- Embedded automatically into the HTML report for instant visual RCA.

### 2. Branded HTML Reporting
Configured in `pytest.ini` using `pytest-html`:
- Generates a standalone, self-contained `reports/report.html`.
- Custom CSS injected via `pytest_html_report_title` hook with clear test outcome graphs.

---

## 🌍 Cross-Browser Verification

All UI tests have been executed and verified against all three major browser rendering engines:
- **Chromium** (Google Chrome, Microsoft Edge, Brave)
- **Firefox** (Gecko)
- **WebKit** (Apple Safari engine on Linux/Windows)

Detailed observations on rendering quirks, modal layout timing, and font metrics are documented in [`docs/cross_browser_testing.md`](docs/cross_browser_testing.md).

---

## 🚀 Quickstart & Execution Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.12 and 3.14)
- Git

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/dulnafernando/qa-ecommerce-testing.git
cd qa-ecommerce-testing

# Create and activate virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
# Optional for full cross-browser testing:
playwright install firefox webkit
```

### 2. Running Tests

```bash
# Run entire test suite (UI + API)
pytest -v

# Run only fast REST API tests (~17s)
pytest -v -m api

# Run only UI End-to-End tests
pytest -v -m ui

# Run a specific test file
pytest -v tests/ui/test_login.py

# Run UI tests in headed mode (visible browser)
pytest -v tests/ui/test_cart.py --headed

# Run UI tests on Firefox or WebKit
pytest -v tests/ui/test_smoke.py --browser firefox
pytest -v tests/ui/test_smoke.py --browser webkit
```

### 3. Viewing Test Reports
After running tests, open the generated HTML report:
```bash
# On Windows:
start reports/report.html
# On macOS:
open reports/report.html
# On Linux:
xdg-open reports/report.html
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

This project runs automated tests on every `git push` and `pull_request` targeting the `main` branch:

- **Runner**: `ubuntu-latest`
- **Steps**:
  1. Python 3.12 environment initialization with `pip` caching.
  2. Installation of locked dependencies (`requirements.txt`).
  3. Playwright browser engine & system library installation.
  4. Execution of REST API tests (`pytest -m api`).
  5. Execution of UI End-to-End tests (`pytest -m ui`).
  6. Artifact upload of `reports/report.html` (retained for 14 days).
  7. Automated upload of failure screenshots in `screenshots/` if any step fails.

---

## 💡 Engineering Retrospective & Future Roadmap

No software project is ever "done." Here is an honest appraisal of architecture trade-offs and planned future enhancements:

1. **Parallel Test Execution with `pytest-xdist`**:
   - *Current State*: Tests run sequentially (~130 seconds total runtime).
   - *Enhancement*: Distribute tests across multiple browser workers (`pytest -n auto`) to reduce full suite runtime to under 40 seconds.
2. **Dynamic Test Data Generation (`Faker`)**:
   - *Current State*: Credentials and payment info use static data stored in JSON files.
   - *Enhancement*: Integrate the Python `Faker` library to generate randomized user registrations and unique checkout inputs on every test run.
3. **Visual Regression Testing**:
   - *Current State*: Assertions verify DOM text, attributes, and mathematical totals.
   - *Enhancement*: Introduce Playwright pixel-comparison snapshots (`expect(page).to_have_screenshot()`) to catch unexpected CSS regressions and layout shifts.
4. **Docker Containerization**:
   - *Current State*: Relies on local Python/Playwright installations.
   - *Enhancement*: Provide a `Dockerfile` and `docker-compose.yml` to guarantee 100% deterministic test execution across any developer OS.

---

## 👤 Author & Acknowledgments

- **Author**: Dulna Fernando
- **Target Application**: [Automation Exercise](https://automationexercise.com)
- **Role**: QA Automation Engineer / Test Lead
