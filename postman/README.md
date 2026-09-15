# API Testing with Postman

This directory contains the production-grade Postman collection and environment for testing the REST API of [Automation Exercise](https://automationexercise.com).

---

## 1. Files in this Directory

- [`Automation_Exercise_API.postman_collection.json`](file:///c:/Users/Admin/qa-ecommerce-testing-1/postman/Automation_Exercise_API.postman_collection.json): Postman Collection v2.1.0 with 10 requests organized into logical folders, covering both positive happy-path and negative error scenarios with integrated JavaScript assertions (`pm.test`).
- [`Automation_Exercise.postman_environment.json`](file:///c:/Users/Admin/qa-ecommerce-testing-1/postman/Automation_Exercise.postman_environment.json): Environment variables file defining `baseUrl`, `validEmail`, and `validPassword`.

---

## 2. API Test Matrix

### Products & Catalog
| Request Name | Method | Endpoint | Scenario Type | Expected Transport Status | Expected Payload `responseCode` |
|---|---|---|---|---|---|
| **GET All Products List** | `GET` | `/api/productsList` | Positive | `200 OK` | `200` (List non-empty, valid schema) |
| **POST All Products List** | `POST` | `/api/productsList` | Negative | `200 OK` | `405` ("Method not supported") |
| **GET All Brands List** | `GET` | `/api/brandsList` | Positive | `200 OK` | `200` (Brands non-empty) |
| **POST Search Product** | `POST` | `/api/searchProduct` | Positive | `200 OK` | `200` (Matches search query) |
| **POST Search Product Missing Param** | `POST` | `/api/searchProduct` | Negative | `200 OK` | `400` ("search_product missing") |

### Authentication & Accounts
| Request Name | Method | Endpoint | Scenario Type | Expected Transport Status | Expected Payload `responseCode` |
|---|---|---|---|---|---|
| **POST Verify Login (Valid)** | `POST` | `/api/verifyLogin` | Positive | `200 OK` | `200` ("User exists!") |
| **POST Verify Login (Invalid)** | `POST` | `/api/verifyLogin` | Negative | `200 OK` | `404` ("User not found!") |
| **POST Verify Login (Missing Email)** | `POST` | `/api/verifyLogin` | Negative | `200 OK` | `400` ("parameter is missing") |
| **DELETE Verify Login** | `DELETE` | `/api/verifyLogin` | Negative | `200 OK` | `405` ("Method not supported") |
| **GET User Detail By Email** | `GET` | `/api/getUserDetailByEmail` | Positive | `200 OK` | `200` (User profile object matches) |

---

## 3. How to Use in Postman

1. Open the **Postman** desktop application or Postman Web.
2. Click **Import** (top left).
3. Drag and drop both files:
   - `postman/Automation_Exercise_API.postman_collection.json`
   - `postman/Automation_Exercise.postman_environment.json`
4. Select the environment **"Automation Exercise - Production"** in the environment dropdown (top right).
5. Click on the collection, click **Run collection**, and click **Run Automation Exercise REST API**.
6. All tests will execute sequentially with real-time test assertions passed.

---

## 4. Key QA Engineering Concepts (Interview Answers)

### A. Transport Layer vs. Application Layer Status Codes
In RESTful API design, a server should return standard HTTP status codes in the response header (`400 Bad Request`, `404 Not Found`, `405 Method Not Allowed`).
However, `automationexercise.com` always returns **`HTTP 200 OK`** at the transport layer, and communicates errors via the JSON payload:
```json
// POST /api/verifyLogin with invalid password
// HTTP Status Header: 200 OK
{
  "responseCode": 404,
  "message": "User not found!"
}
```
**Why this matters:**
Testing only `pm.response.to.have.status(200)` gives a **false positive** because an error response still has status 200. Our test scripts inspect both layers:
```javascript
pm.test("Transport status is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Business logic status is 404", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.responseCode).to.eql(404);
    pm.expect(jsonData.message).to.eql("User not found!");
});
```

### B. Payload Validation vs Status-Only Checks
A robust API test suite must validate:
1. **Status:** Transport code and business response code.
2. **Performance:** Response time SLA (e.g. `< 3000ms`).
3. **Structure & Schema:** Keys exist with correct types (`products` is array, contains `id`, `name`, `price`).
4. **Data Integrity:** Returned data matches the request (e.g. search for `"top"` returns items containing `"top"`).
