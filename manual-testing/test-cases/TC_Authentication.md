# Test Cases: Authentication & User Accounts

This suite covers test cases for user authentication, session persistence, security boundary validation, and logout functionality.

---

## Summary Matrix

| Test Case ID | Test Case Title | Type | Priority | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_AUTH_001** | Successful Login with Valid Registered Credentials | Positive | P1 | Critical | **PASS** |
| **TC_AUTH_002** | Login Attempt with Unregistered Email | Negative | P1 | Major | **PASS** |
| **TC_AUTH_003** | Login Attempt with Incorrect Password | Negative | P1 | Major | **PASS** |
| **TC_AUTH_004** | Login Submission with Blank Mandatory Fields | Negative | P2 | Medium | **PASS** |
| **TC_AUTH_005** | SQL Injection Attempt in Login Fields | Security | P1 | Critical | **PASS** |
| **TC_AUTH_006** | User Session Termination via Logout | Functional | P1 | Major | **PASS** |

---

## Detailed Test Cases

### TC_AUTH_001: Successful Login with Valid Registered Credentials
- **Module:** Authentication
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Automated & Manual
- **Preconditions:** Registered user account exists (`dulna.test@example.com` / `Test@12345`).
- **Test Steps:**
  1. Navigate to base URL: `https://automationexercise.com`.
  2. Click on `Signup / Login` in header navigation.
  3. Verify page title is `"Automation Exercise - Signup / Login"`.
  4. Locate "Login to your account" form.
  5. Enter valid email in `[data-qa="login-email"]`.
  6. Enter valid password in `[data-qa="login-password"]`.
  7. Click `[data-qa="login-button"]`.
- **Expected Result:**
  - User is redirected to Home Page (`/`).
  - Header displays `Logged in as Dulna Test`.
  - `Signup / Login` link is replaced with `Logout` and `Delete Account`.
- **Actual Result:** As expected. Header updates immediately with logged-in user state.
- **Status:** **PASS**

---

### TC_AUTH_002: Login Attempt with Unregistered Email
- **Module:** Authentication
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** Email `unregistered_qa_user_9999@test.com` does not exist in user database.
- **Test Steps:**
  1. Navigate to `https://automationexercise.com/login`.
  2. Enter `unregistered_qa_user_9999@test.com` into email field.
  3. Enter any standard password (e.g., `Password123!`).
  4. Click `Login`.
- **Expected Result:**
  - Login fails; user remains on `/login`.
  - System displays user-friendly error message: `"Your email or password is incorrect!"`.
  - Password field is cleared or protected.
- **Actual Result:** As expected. Red error banner displays `"Your email or password is incorrect!"`.
- **Status:** **PASS**

---

### TC_AUTH_003: Login Attempt with Incorrect Password
- **Module:** Authentication
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** Registered account exists (`dulna.test@example.com`).
- **Test Steps:**
  1. Navigate to `https://automationexercise.com/login`.
  2. Enter `dulna.test@example.com` into email field.
  3. Enter incorrect password `CompletelyWrongPass123`.
  4. Click `Login`.
- **Expected Result:**
  - User is not authenticated.
  - Error banner displays: `"Your email or password is incorrect!"`.
  - No session tokens or cookies are issued.
- **Actual Result:** As expected. Generic error displayed without disclosing which field was invalid (prevents user enumeration).
- **Status:** **PASS**

---

### TC_AUTH_004: Login Submission with Blank Mandatory Fields
- **Module:** Authentication
- **Priority:** Medium (P2)
- **Severity:** Medium
- **Execution Type:** Automated & Manual
- **Preconditions:** Browser open on `/login`.
- **Test Steps:**
  1. Leave email and password fields completely empty.
  2. Click `Login` button.
- **Expected Result:**
  - Form submission is intercepted client-side by HTML5 validation (`required` attribute).
  - Browser displays native tooltip: `"Please fill out this field."`.
  - No HTTP network request is dispatched to server.
- **Actual Result:** Form displays native HTML5 validation prompt.
- **Status:** **PASS**

---

### TC_AUTH_005: SQL Injection Attempt in Login Fields
- **Module:** Authentication / Security
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Automated & Manual
- **Preconditions:** Browser open on `/login`.
- **Test Steps:**
  1. Enter standard SQL injection string in email: `' OR '1'='1`.
  2. Enter `' OR '1'='1` in password field.
  3. Click `Login`.
- **Expected Result:**
  - Input is sanitized and parameterized; no SQL syntax error, database dump, or unauthorized session creation occurs.
  - Form rejects input or presents invalid login error.
- **Actual Result:** Authentication fails gracefully; error banner `"Your email or password is incorrect!"` displayed. Zero SQL leak.
- **Status:** **PASS**

---

### TC_AUTH_006: User Session Termination via Logout
- **Module:** Authentication
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** User is logged in with active session.
- **Test Steps:**
  1. Click `Logout` in top navigation bar (`a[href="/logout"]`).
  2. Attempt to navigate back using browser "Back" button.
- **Expected Result:**
  - Session is destroyed.
  - User is redirected to `/login`.
  - Browser back button does not restore authenticated user state.
- **Actual Result:** Session terminated; redirect to `/login` successful.
- **Status:** **PASS**
