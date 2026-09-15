# Manual Test Scenarios — E-Commerce Platform

This document outlines the high-level **Test Scenarios** for the [Automation Exercise](https://automationexercise.com) e-commerce web application. 

In professional QA methodology, **Test Scenarios** provide end-to-end, user-centric coverage of functional journeys ("*what* to test"), serving as the blueprint from which detailed **Test Cases** ("*how* to test") are derived.

---

## 1. Test Design Techniques Applied

To ensure high defect-yield and efficient test coverage without redundant test bloat, the following test design techniques were applied:

1. **Equivalence Partitioning (EP)**:
   - Dividing input domains into valid and invalid classes (e.g., valid email formats vs. malformed emails, registered users vs. unregistered users).
2. **Boundary Value Analysis (BVA)**:
   - Testing edges of input ranges: item quantity fields tested at `-1`, `0`, `1`, `999`, and extreme boundaries.
3. **State Transition Testing**:
   - Verifying state lifecycles: Anonymous Visitor $\to$ Authenticated User $\to$ Cart Active $\to$ Checkout Pending $\to$ Order Invoiced $\to$ Logged Out.
4. **Error Guessing & Exploratory Testing**:
   - Probing edge cases based on common e-commerce failure modes: direct URL navigation to protected checkout pages, cart tampering, and API method mismatches.

---

## 2. Test Scenario Matrix

| Scenario ID | Module | Scenario Description | Objective / Risk Addressed | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **TS_AUTH_01** | Authentication | User Account Login & Session Lifecycle | Verify registered user can authenticate, maintain session state, and safely terminate session. | High (P1) |
| **TS_AUTH_02** | Authentication | Invalid Credentials & Account Security | Verify authentication fails cleanly on incorrect passwords, nonexistent accounts, and empty inputs without leaking server details. | High (P1) |
| **TS_AUTH_03** | Authentication | New User Registration & Duplicate Email Handling | Verify new user onboarding flow and system rejection of duplicate registered email addresses. | Medium (P2) |
| **TS_PROD_01** | Catalog & Search | Product Browsing, Filtering & Keyword Search | Verify products load accurately across categories/brands and keyword search yields relevant items. | High (P1) |
| **TS_PROD_02** | Product Details | Product Details View & Quantity Selection | Verify product metadata (price, availability, condition, brand) and quantity bounds enforcement. | High (P1) |
| **TS_CART_01** | Shopping Cart | Add to Cart from Catalog and Detail Pages | Verify items can be added, cart modal reflects added item, and cart badge updates accurately. | High (P1) |
| **TS_CART_02** | Shopping Cart | Cart Quantity Modification & Item Removal | Verify modifying quantities updates totals and deleting an item immediately detaches it from the cart. | High (P1) |
| **TS_CART_03** | Shopping Cart | Cart Calculation & Financial Integrity | Verify individual line totals ($\text{Price} \times \text{Quantity}$) and composite cart subtotal integrity. | Critical (P1) |
| **TS_CHK_01** | Checkout & Payment | End-to-End Order Placement (Happy Path) | Verify authenticated user proceeds from cart $\to$ delivery review $\to$ payment submission $\to$ order confirmation. | Critical (P1) |
| **TS_CHK_02** | Checkout & Payment | Client-Side & Server-Side Payment Validation | Verify checkout fails gracefully when mandatory payment fields (card number, CVV, expiry) are missing or invalid. | High (P1) |
| **TS_CHK_03** | Access Control | Unauthenticated Checkout Enforcement | Verify guest users attempting to checkout are redirected to login/registration before accessing payment gateways. | High (P1) |
| **TS_API_01** | REST API | Catalog & Search API Contract Verification | Verify GET `/api/productsList` and POST `/api/searchProduct` return valid JSON schema and correct status codes. | High (P2) |
| **TS_API_02** | REST API | Authentication & User API Validation | Verify POST `/api/verifyLogin` validates user credentials with appropriate HTTP contract adherence. | High (P2) |

---

## 3. Detailed Scenario Walkthroughs

### Scenario TS_AUTH_01: Valid User Authentication & Navigation
- **Primary Actor:** Returning customer with pre-existing registered credentials.
- **Preconditions:** User account exists in database (`test_data/login_data.json`).
- **Flow:**
  1. User navigates to Home Page.
  2. Clicks `Signup / Login` header navigation link.
  3. Fills registered email and password in the login form.
  4. Submits login form.
  5. System validates credentials, establishes session, and redirects to Home Page.
  6. Header updates to display `Logged in as <Username>`.
  7. User clicks `Logout`; session terminates and page returns to login screen.
- **Success Criteria:** Persistent authenticated state during navigation, zero session leakage post-logout.

---

### Scenario TS_PROD_02: Product Quantity Boundary Enforcement
- **Primary Actor:** Shopper on Product Details page.
- **Preconditions:** Product exists in inventory.
- **Flow:**
  1. User navigates to `/product_details/1`.
  2. Enters valid quantity (e.g., `3`) $\to$ Cart reflects quantity `3` with line total $3 \times \text{Unit Price}$.
  3. Enters boundary value (`0` or negative `-2`) $\to$ System must reject input or prevent addition to cart.
- **Success Criteria:** Negative or zero quantities cannot be placed into the cart or order summary. *(Note: Exploratory testing revealed this is currently a **reproducible defect** on the live target; see `manual-testing/bug-reports/BUG-001-negative-order-total-checkout.md`).*

---

### Scenario TS_CHK_01: End-to-End Order Placement
- **Primary Actor:** Authenticated shopper.
- **Preconditions:** User is logged in; cart contains 1 or more items.
- **Flow:**
  1. User navigates to `/view_cart` and clicks `Proceed To Checkout`.
  2. User reviews Delivery Address, Billing Address, and Order Review Table.
  3. User enters order comments and clicks `Place Order`.
  4. User enters Name on Card, Card Number, CVC, Expiration Month, and Expiration Year.
  5. Clicks `Pay and Confirm Order`.
  6. System confirms payment and navigates to `/payment_done` with success message: `ORDER PLACED!`.
  7. User can download invoice and return to home page.
- **Success Criteria:** Accurate address transfer, exact financial calculations, and clear order confirmation receipt.
