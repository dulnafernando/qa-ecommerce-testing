# Bug Report: BUG-002

## Defect Summary
**Title:** REST API Endpoints Return HTTP 200 OK Transport Status on 4xx Client and Method Errors  
**Bug ID:** `BUG-002`  
**Module:** REST API / HTTP Transport Protocol  
**Reported By:** Dulna Fernando (QA Automation Lead)  
**Date Logged:** 2026-09-15  
**Environment:** Production (`https://automationexercise.com/api/*`)  
**Severity:** **Major** (Violates REST protocol standards and breaking API gateway / client contracts)  
**Priority:** **P2 — High**  
**Associated Test Cases:** `TC_API_002`, `TC_API_005`, `TC_API_007`, `TC_API_008`, `TC_API_009`  

---

## 1. Description
The application's REST API endpoints consistently return **`HTTP 200 OK`** at the network transport layer, even when the request represents an invalid method (`405`), a missing parameter (`400`), or an invalid resource/login (`404`).

Instead of utilizing standard HTTP response status codes, the server embeds the true status code inside a JSON body attribute called `responseCode` (e.g., `{"responseCode": 405, "message": "This request method is not supported."}`).

---

## 2. Evidence & Steps to Reproduce

### Case A: Unsupported HTTP Method (`405 Method Not Allowed`)
- **Request:**
  ```http
  POST /api/productsList HTTP/1.1
  Host: automationexercise.com
  ```
- **Actual HTTP Response Header:**
  ```http
  HTTP/1.1 200 OK
  Content-Type: text/html; charset=UTF-8
  ```
- **Actual Response Body:**
  ```json
  {"responseCode": 405, "message": "This request method is not supported."}
  ```
- **Expected HTTP Response:**
  - Status code: `405 Method Not Allowed`.
  - Header: `Allow: GET`.

---

### Case B: Missing Required Parameter (`400 Bad Request`)
- **Request:**
  ```http
  POST /api/searchProduct HTTP/1.1
  Host: automationexercise.com
  Content-Type: application/x-www-form-urlencoded
  (Empty Body)
  ```
- **Actual HTTP Response Header:**
  ```http
  HTTP/1.1 200 OK
  ```
- **Actual Response Body:**
  ```json
  {"responseCode": 400, "message": "Bad request, search_product parameter is missing in POST request."}
  ```
- **Expected HTTP Response:**
  - Status code: `400 Bad Request`.

---

### Case C: Unregistered User Authentication (`404 Not Found` / `401 Unauthorized`)
- **Request:**
  ```http
  POST /api/verifyLogin HTTP/1.1
  Host: automationexercise.com
  Content-Type: application/x-www-form-urlencoded
  
  email=nonexistent_user_99999@test.com&password=InvalidPassword123
  ```
- **Actual HTTP Response Header:**
  ```http
  HTTP/1.1 200 OK
  ```
- **Actual Response Body:**
  ```json
  {"responseCode": 404, "message": "User not found!"}
  ```
- **Expected HTTP Response:**
  - Status code: `404 Not Found` or `401 Unauthorized`.

---

## 3. Impact & Business Consequences
1. **Broken Client Libraries**: Standard HTTP client libraries (Axios, Fetch, Requests, Apollo, Retrofit) treat `200 OK` as a success, requiring consumers to write anti-pattern wrapper code inspecting body contents to catch errors.
2. **Monitoring & Alerting Failure**: Cloud monitoring tools (Datadog, AWS CloudWatch, Sentry, New Relic) rely on HTTP 4xx/5xx status codes to measure error rates and trigger alerting thresholds. Masking errors behind 200 OK renders error-rate monitoring useless.
3. **CDN & Cache Corruption**: Reverse proxies and CDNs (Cloudflare, Fastly, Akamai) may cache a 200 OK response, serving error bodies to subsequent requests.

---

## 4. Architectural Recommendation
Update the API gateway / controller middleware to synchronize the HTTP transport status code with the payload status code:
```python
# Before (Anti-pattern)
return JsonResponse({"responseCode": 400, "message": "Missing parameter"}, status=200)

# After (RESTful / RFC 9110 Compliant)
return JsonResponse({"responseCode": 400, "message": "Missing parameter"}, status=400)
```
