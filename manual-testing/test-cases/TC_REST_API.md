# Test Cases: REST API Endpoints

This suite covers REST API endpoints across product catalogs, search queries, and user authentication, detailing status code expectations, response schema structure, and transport vs. payload contract discrepancies.

---

## Summary Matrix

| Test Case ID | Test Case Title | Method | Endpoint | Priority | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_API_001** | Retrieve All Products List | GET | `/api/productsList` | P1 | Major | **PASS** |
| **TC_API_002** | Unsupported HTTP Method on Products List | POST | `/api/productsList` | P2 | Major | **FAIL (Defect BUG-002)** |
| **TC_API_003** | Retrieve All Brands List | GET | `/api/brandsList` | P2 | Medium | **PASS** |
| **TC_API_004** | Search Product with Valid Parameter | POST | `/api/searchProduct` | P1 | Major | **PASS** |
| **TC_API_005** | Search Product Without Mandatory Parameter | POST | `/api/searchProduct` | P2 | Major | **FAIL (Defect BUG-002)** |
| **TC_API_006** | Verify Login with Valid Credentials | POST | `/api/verifyLogin` | P1 | Critical | **PASS** |
| **TC_API_007** | Verify Login with Unregistered Email | POST | `/api/verifyLogin` | P1 | Major | **FAIL (Defect BUG-002)** |
| **TC_API_008** | Verify Login Missing Email Parameter | POST | `/api/verifyLogin` | P2 | Major | **FAIL (Defect BUG-002)** |
| **TC_API_009** | Unsupported Method on Verify Login | DELETE | `/api/verifyLogin` | P2 | Major | **FAIL (Defect BUG-002)** |
| **TC_API_010** | Retrieve User Profile by Registered Email | GET | `/api/getUserDetailByEmail` | P1 | Major | **PASS** |

---

## Detailed Test Cases

### TC_API_001: Retrieve All Products List
- **Module:** REST API / Products
- **HTTP Method:** `GET`
- **Endpoint:** `https://automationexercise.com/api/productsList`
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated (`pytest` + `requests` & Postman)
- **Test Steps:**
  1. Send `GET /api/productsList` with header `Accept: application/json`.
  2. Parse HTTP response code and JSON body.
- **Expected Result:**
  - HTTP Status: `200 OK`.
  - JSON Schema: `{"responseCode": 200, "products": [...]}`.
  - Each item in `products` contains: `id` (int), `name` (str), `price` (str), `brand` (str), `category` (object).
- **Actual Result:** Returns HTTP 200 with complete array of products matching schema.
- **Status:** **PASS**

---

### TC_API_002: Unsupported HTTP Method on Products List (RFC 9110 Violation)
- **Module:** REST API / HTTP Standards
- **HTTP Method:** `POST`
- **Endpoint:** `https://automationexercise.com/api/productsList`
- **Priority:** Medium (P2)
- **Severity:** Major
- **Execution Type:** Automated (`test_post_all_products_list_method_not_allowed`)
- **Test Steps:**
  1. Dispatch `POST` request to `/api/productsList` with arbitrary body.
  2. Inspect HTTP status code and response payload.
- **Expected Result:**
  - HTTP Transport Status: `405 Method Not Allowed`.
  - Response Header: `Allow: GET`.
  - Body: Informative error message.
- **Actual Result:** 
  - **HTTP Transport Status is 200 OK** (Incorrect).
  - Payload contains `{"responseCode": 405, "message": "This request method is not supported."}`.
- **Status:** **FAIL (Logged as BUG-002)**

---

### TC_API_004: Search Product with Valid Parameter
- **Module:** REST API / Search
- **HTTP Method:** `POST`
- **Endpoint:** `https://automationexercise.com/api/searchProduct`
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated
- **Preconditions:** Server catalog contains items matching `"top"`.
- **Test Steps:**
  1. Send `POST /api/searchProduct` with form-urlencoded body: `search_product=top`.
- **Expected Result:**
  - HTTP Status: `200 OK`.
  - JSON Body: `{"responseCode": 200, "products": [...]}`.
  - Length of `products` array $> 0$.
- **Actual Result:** HTTP 200 returned with matching products array.
- **Status:** **PASS**

---

### TC_API_005: Search Product Without Mandatory Parameter
- **Module:** REST API / Validation
- **HTTP Method:** `POST`
- **Endpoint:** `https://automationexercise.com/api/searchProduct`
- **Priority:** Medium (P2)
- **Severity:** Major
- **Execution Type:** Automated
- **Test Steps:**
  1. Send `POST /api/searchProduct` with empty body `{}`.
- **Expected Result:**
  - HTTP Transport Status: `400 Bad Request`.
  - JSON Body: Error message explaining missing parameter.
- **Actual Result:**
  - **HTTP Transport Status is 200 OK** (Incorrect).
  - Payload contains `{"responseCode": 400, "message": "Bad request, search_product parameter is missing in POST request."}`.
- **Status:** **FAIL (Logged as BUG-002)**

---

### TC_API_006: Verify Login with Valid Credentials
- **Module:** REST API / Auth
- **HTTP Method:** `POST`
- **Endpoint:** `https://automationexercise.com/api/verifyLogin`
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Automated
- **Preconditions:** Registered user exists.
- **Test Steps:**
  1. Send `POST /api/verifyLogin` with `email=<registered_email>` and `password=<valid_password>`.
- **Expected Result:**
  - HTTP Status: `200 OK`.
  - JSON Body: `{"responseCode": 200, "message": "User exists!"}`.
- **Actual Result:** Returns HTTP 200 with `"User exists!"`.
- **Status:** **PASS**

---

### TC_API_007: Verify Login with Unregistered Email
- **Module:** REST API / Auth
- **HTTP Method:** `POST`
- **Endpoint:** `https://automationexercise.com/api/verifyLogin`
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated
- **Test Steps:**
  1. Send `POST /api/verifyLogin` with `email=nonexistent@example.com` and `password=anyPassword`.
- **Expected Result:**
  - HTTP Transport Status: `404 Not Found` (or `401 Unauthorized`).
  - JSON Body: Informative user not found message.
- **Actual Result:**
  - **HTTP Transport Status is 200 OK** (Incorrect).
  - Payload contains `{"responseCode": 404, "message": "User not found!"}`.
- **Status:** **FAIL (Logged as BUG-002)**
