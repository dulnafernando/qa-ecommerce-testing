# Test Cases Repository — Index & Traceability Matrix

This directory contains the structured test case repository for the E-Commerce Platform. Each test case is assigned a unique identifier, categorized by functional module, prioritized, and linked to its execution status and corresponding bug reports.

---

## 1. Traceability & Execution Summary

| Module | Test File | Total Cases | Passed | Failed / Bugs Found | Automated |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Authentication** | [`TC_Authentication.md`](./TC_Authentication.md) | 6 | 6 | 0 | 6 |
| **Products & Catalog** | [`TC_Products_Catalog.md`](./TC_Products_Catalog.md) | 6 | 4 | 2 (BUG-001, BUG-003) | 3 |
| **Cart & Checkout** | [`TC_Cart_Checkout.md`](./TC_Cart_Checkout.md) | 6 | 5 | 1 (BUG-004) | 5 |
| **REST API** | [`TC_REST_API.md`](./TC_REST_API.md) | 10 | 5 | 5 (BUG-002) | 10 |
| **TOTAL** | | **28** | **20** | **8** | **24** |

---

## 2. Priority & Severity Classification Framework

In professional QA organizations, **Priority** and **Severity** are distinct dimensions used during defect triage:

- **Severity (Technical Impact)**: Measures how severely a bug impairs the application's functionality or architecture:
  - **Critical**: System crash, data corruption, security vulnerability, or financial loss (e.g., negative checkout total).
  - **Major**: Core feature fails with no workaround (e.g., login failure, API contract breach).
  - **Medium**: Non-critical feature fails, or workaround exists (e.g., sorting bug, cosmetic alignment).
  - **Low**: Minor cosmetic, typo, or minor usability annoyance (e.g., missing confirmation message).

- **Priority (Business Urgency)**: Dictates the business scheduling order for engineering to resolve the defect:
  - **P1 (Immediate)**: Must be patched immediately; blocks release or risks immediate revenue/reputation loss.
  - **P2 (High)**: Must be resolved in the current sprint before general deployment.
  - **P3 (Medium)**: Normal backlog queue; fix in upcoming maintenance cycle.
  - **P4 (Low)**: Low urgency; fix when time permits.

---

## 3. Master Test Cases Matrix

| Case ID | Module | Title | Type | Priority | Severity | Status | Defect Reference |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC_AUTH_001` | Auth | Valid credentials login | Positive | P1 | Critical | **PASS** | — |
| `TC_AUTH_002` | Auth | Unregistered email login | Negative | P1 | Major | **PASS** | — |
| `TC_AUTH_003` | Auth | Incorrect password login | Negative | P1 | Major | **PASS** | — |
| `TC_AUTH_004` | Auth | Blank fields validation | Negative | P2 | Medium | **PASS** | — |
| `TC_AUTH_005` | Auth | SQL injection resistance | Security | P1 | Critical | **PASS** | — |
| `TC_AUTH_006` | Auth | User session logout | Functional | P1 | Major | **PASS** | — |
| `TC_PROD_001` | Catalog | Full catalog display | Functional | P1 | Major | **PASS** | — |
| `TC_PROD_002` | Catalog | Search with matching term | Functional | P1 | Major | **PASS** | — |
| `TC_PROD_003` | Catalog | Search non-existent term | Functional | P2 | Medium | **PASS** | — |
| `TC_PROD_004` | Catalog | Product details metadata | Functional | P1 | Major | **PASS** | — |
| `TC_PROD_005` | Catalog | Quantity boundary analysis | Boundary | P1 | Critical | **FAIL** | [`BUG-001`](../bug-reports/BUG-001-negative-order-total-checkout.md) |
| `TC_PROD_006` | Catalog | Add to cart keyboard a11y | Usability | P3 | Medium | **FAIL** | [`BUG-003`](../bug-reports/BUG-003-catalog-add-to-cart-missing-href-accessibility.md) |
| `TC_CART_001` | Cart | Add multiple items | Functional | P1 | Critical | **PASS** | — |
| `TC_CART_002` | Cart | Async cart item removal | Functional | P2 | Major | **PASS** | — |
| `TC_CART_003` | Cart | Line total math calculation | Financial | P1 | Critical | **PASS** | — |
| `TC_CHK_001` | Checkout | End-to-end checkout & pay | E2E | P1 | Critical | **PASS** | — |
| `TC_CHK_002` | Checkout | Missing payment fields | Validation | P1 | High | **PASS** | — |
| `TC_CHK_003` | Cart | Missing delete confirmation | Usability | P3 | Low | **FAIL** | [`BUG-004`](../bug-reports/BUG-004-cart-removal-missing-confirmation-and-undo.md) |
| `TC_API_001` | API | GET `/api/productsList` | Functional | P1 | Major | **PASS** | — |
| `TC_API_002` | API | POST `/api/productsList` | Standard | P2 | Major | **FAIL** | [`BUG-002`](../bug-reports/BUG-002-api-returns-200-on-client-and-method-errors.md) |
| `TC_API_003` | API | GET `/api/brandsList` | Functional | P2 | Medium | **PASS** | — |
| `TC_API_004` | API | POST `/api/searchProduct` | Functional | P1 | Major | **PASS** | — |
| `TC_API_005` | API | POST `/api/searchProduct` (empty) | Validation | P2 | Major | **FAIL** | [`BUG-002`](../bug-reports/BUG-002-api-returns-200-on-client-and-method-errors.md) |
| `TC_API_006` | API | POST `/api/verifyLogin` (valid) | Functional | P1 | Critical | **PASS** | — |
| `TC_API_007` | API | POST `/api/verifyLogin` (invalid) | Validation | P1 | Major | **FAIL** | [`BUG-002`](../bug-reports/BUG-002-api-returns-200-on-client-and-method-errors.md) |
| `TC_API_008` | API | POST `/api/verifyLogin` (no email) | Validation | P2 | Major | **FAIL** | [`BUG-002`](../bug-reports/BUG-002-api-returns-200-on-client-and-method-errors.md) |
| `TC_API_009` | API | DELETE `/api/verifyLogin` | Standard | P2 | Major | **FAIL** | [`BUG-002`](../bug-reports/BUG-002-api-returns-200-on-client-and-method-errors.md) |
| `TC_API_010` | API | GET `/api/getUserDetailByEmail` | Functional | P1 | Major | **PASS** | — |
