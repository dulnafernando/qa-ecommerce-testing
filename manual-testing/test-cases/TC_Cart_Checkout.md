# Test Cases: Cart Management & Checkout Flow

This suite covers shopping cart operations, asynchronous item removal, mathematical verification of line items vs. composite totals, address validation, and payment processing.

---

## Summary Matrix

| Test Case ID | Test Case Title | Type | Priority | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_CART_001** | Add Multiple Distinct Products to Cart | Functional | P1 | Critical | **PASS** |
| **TC_CART_002** | Asynchronous Cart Item Removal | Functional / AJAX | P2 | Major | **PASS** |
| **TC_CART_003** | Cart Mathematical Calculation Verification ($\text{Price} \times \text{Qty}$) | Financial / Logic | P1 | Critical | **PASS** |
| **TC_CHK_001** | End-to-End Valid Checkout with Card Payment | E2E Happy Path | P1 | Critical | **PASS** |
| **TC_CHK_002** | Payment Submission with Missing Mandatory Fields | Validation | P1 | High | **PASS** |
| **TC_CHK_003** | Cart Removal Lacks Undo Confirmation Warning | Usability | P3 | Low | **FAIL (Defect BUG-004)** |

---

## Detailed Test Cases

### TC_CART_001: Add Multiple Distinct Products to Cart
- **Module:** Cart
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Automated & Manual
- **Preconditions:** Fresh browser session; cart is empty.
- **Test Steps:**
  1. Navigate to `/products`.
  2. Click "Add to cart" on product 1 (`Blue Top`, Rs. 500).
  3. In modal dialog, click "Continue Shopping".
  4. Click "Add to cart" on product 2 (`Men Tshirt`, Rs. 400).
  5. In modal dialog, click "View Cart".
- **Expected Result:**
  - Cart table `#cart_info_table` renders exactly 2 product rows.
  - Row 1 displays `Blue Top`, Price `Rs. 500`, Quantity `1`, Total `Rs. 500`.
  - Row 2 displays `Men Tshirt`, Price `Rs. 400`, Quantity `1`, Total `Rs. 400`.
- **Actual Result:** Both rows render accurately with matching product names, quantities, and line totals.
- **Status:** **PASS**

---

### TC_CART_002: Asynchronous Cart Item Removal
- **Module:** Cart
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** Cart contains 2 items (`Blue Top` and `Men Tshirt`).
- **Test Steps:**
  1. Navigate to `/view_cart`.
  2. Identify product row with ID `product-1`.
  3. Click the delete icon `.cart_quantity_delete` on that row.
  4. Wait for DOM detachment / AJAX network completion.
- **Expected Result:**
  - Deleted item row is detached from the DOM without requiring a full page refresh.
  - Cart now contains only 1 remaining product row (`Men Tshirt`).
  - Remaining row retains accurate pricing and description.
- **Actual Result:** Row detaches dynamically; 1 item remains in table.
- **Status:** **PASS**

---

### TC_CART_003: Cart Mathematical Calculation Verification
- **Module:** Cart & Financial Logic
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Automated
- **Preconditions:** Cart contains multiple items with varied quantities (e.g., 2 units of Item A at Rs. 500, 3 units of Item B at Rs. 400).
- **Test Steps:**
  1. For each row in `#cart_info_table tbody tr`:
     - Parse `Unit Price` string into numeric float (strip `"Rs. "`).
     - Parse `Quantity` string into integer.
     - Parse `Total Price` string into numeric float.
     - Compute expected line total: $\text{Price} \times \text{Quantity}$.
     - Assert line total matches expected product.
  2. Sum all line totals: $\sum \text{Line Totals}$.
  3. Compare against checkout composite order total.
- **Expected Result:**
  - Mathematical identity holds: $\text{Price} \times \text{Quantity} == \text{Line Total}$ for every row.
  - Sum of line totals equals final invoice charge.
- **Actual Result:** Calculations verified accurately via automated test `test_order_review_calculations_and_totals`.
- **Status:** **PASS**

---

### TC_CHK_001: End-to-End Valid Checkout with Card Payment
- **Module:** Checkout & Payment
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Automated & Manual
- **Preconditions:** User is authenticated (`dulna.test@example.com`); cart contains at least 1 item.
- **Test Steps:**
  1. From `/view_cart`, click `Proceed To Checkout`.
  2. On `/checkout`, verify Delivery Address and Billing Address contain user details.
  3. Verify Order Summary matches cart contents.
  4. Enter order note: `"Please deliver between 9 AM and 5 PM"`.
  5. Click `Place Order` button (navigates to `/payment`).
  6. Fill payment details:
     - Name on Card: `Dulna Fernando`
     - Card Number: `4111 2222 3333 4444`
     - CVC: `123`
     - Expiration Month: `12`
     - Expiration Year: `2028`
  7. Click `Pay and Confirm Order` (`#submit`).
- **Expected Result:**
  - Form submits successfully.
  - User is navigated to `/payment_done`.
  - Page confirms: `"ORDER PLACED!"` and `"Congratulations! Your order has been confirmed!"`.
- **Actual Result:** Order placed successfully; confirmation banner displayed.
- **Status:** **PASS**

---

### TC_CHK_002: Payment Submission with Missing Mandatory Fields
- **Module:** Payment
- **Priority:** High (P1)
- **Severity:** High
- **Execution Type:** Automated & Manual
- **Preconditions:** Navigated to `/payment` with active order session.
- **Test Steps:**
  1. Leave all payment fields blank.
  2. Click `Pay and Confirm Order`.
- **Expected Result:**
  - Browser intercepts submission via HTML5 validation (`required` attribute on card name, number, cvc).
  - Form validity check `el.checkValidity()` returns `False`.
  - Transaction is not dispatched to payment processor.
- **Actual Result:** Native validation flags missing mandatory fields.
- **Status:** **PASS**

---

### TC_CHK_003: Cart Removal Lacks Undo Confirmation Warning
- **Module:** Cart / Usability
- **Priority:** Low (P3)
- **Severity:** Low
- **Execution Type:** Manual
- **Preconditions:** Cart contains 1 item.
- **Test Steps:**
  1. On `/view_cart`, accidentally or intentionally click the "X" (delete) icon.
- **Expected Result:**
  - Best-practice e-commerce UX displays a quick confirmation prompt ("Are you sure you want to remove this item?") or provides a toast notification with an "Undo" action.
- **Actual Result:**
  - Item is immediately deleted via AJAX with zero confirmation or recovery option.
- **Status:** **FAIL (Logged as BUG-004)**
