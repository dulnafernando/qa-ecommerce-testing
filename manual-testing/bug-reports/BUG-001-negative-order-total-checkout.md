# Bug Report: BUG-001

## Defect Summary
**Title:** Negative and Zero Product Quantities Allowed at Checkout Resulting in Negative Order Total  
**Bug ID:** `BUG-001`  
**Module:** Shopping Cart / Product Details / Checkout  
**Reported By:** Dulna Fernando (QA Automation Lead)  
**Date Logged:** 2026-09-15  
**Environment:** Production (`https://automationexercise.com`), Chrome 120+, Firefox 120+, WebKit  
**Severity:** **Critical** (Financial integrity compromise / business logic failure)  
**Priority:** **P1 — Immediate**  
**Associated Test Case:** `TC_PROD_005`, `TC_CHK_001`  

---

## 1. Description
On the Product Details page (`/product_details/<id>`), the item quantity input field `#quantity` accepts zero (`0`) and negative numeric integers (e.g., `-1`, `-5`). 

When an end-user submits a negative quantity, the system places the negative item into the shopping cart, calculates a negative line total (e.g., $\text{Unit Price Rs. 500} \times -1 = \text{Rs. -500}$), and allows the user to proceed to checkout. If combined with a lower-priced legitimate item, the total order amount calculates to a negative balance (e.g., $\text{Rs. 400} + (\text{Rs. -500}) = \text{Rs. -100}$). The checkout page accepts this negative amount and allows proceeding to payment.

---

## 2. Steps to Reproduce
1. Navigate to product details page: `https://automationexercise.com/product_details/1`.
2. In the quantity input field (`#quantity`), delete the default value `1` and type `-1`.
3. Click the `Add to cart` button.
4. In the pop-up modal dialog, click `Continue Shopping`.
5. Navigate to another product details page: `https://automationexercise.com/product_details/2`.
6. Add `1` quantity of `Men Tshirt` (Price: Rs. 400) to the cart.
7. Navigate to the shopping cart: `https://automationexercise.com/view_cart`.
8. Observe the cart table:
   - Row 1: Men Tshirt | Price: Rs. 400 | Qty: 1 | Total: Rs. 400
   - Row 2: Blue Top | Price: Rs. 500 | Qty: -1 | Total: Rs. -500
9. Click `Proceed To Checkout`.
10. Inspect the order review total on `/checkout`.

---

## 3. Expected vs. Actual Results

### Expected Result:
1. **Client-Side Validation**: The `#quantity` input should enforce HTML5 boundary attributes (`min="1"`, `step="1"`), preventing input or submission of non-positive values.
2. **Server-Side Validation**: The backend cart API must validate that `quantity >= 1`. If invalid input is received, return HTTP 400 Bad Request with an error message: `"Quantity must be a positive integer."`.
3. **Checkout Rejection**: The checkout engine must reject any order where item quantities are $\le 0$ or where the composite order total is $\le 0$.

### Actual Result:
1. `#quantity` has `type="number"`, but completely lacks the `min="1"` attribute.
2. The modal confirms: `"Your product has been added to cart."`.
3. The cart line total is negative: `Rs. -500`.
4. The final order amount on the checkout page calculates to:
   ```text
   Men Tshirt (Rs. 400) + Blue Top (Rs. -500) = Total Amount: Rs. -100
   ```
5. The checkout system allows placing the order with a negative total.

---

## 4. Root Cause Analysis (RCA)
- **Front-End**: Missing input constraints on `<input type="number" name="quantity" id="quantity" value="1">`. It lacks `min="1"`, `oninput="validity.valid||(value='');"`, or form submission checks.
- **Back-End**: Missing server-side domain model validation in the session cart service. The backend accepts whatever integer is passed in the request body without asserting `quantity > 0`.

---

## 5. Automated Reproduction Script
This defect was programmatically verified and documented via Playwright:
```python
page.goto("https://automationexercise.com/product_details/1")
page.locator("#quantity").fill("-1")
page.locator("button:has-text('Add to cart')").click()
page.goto("https://automationexercise.com/view_cart")
assert page.locator(".cart_total_price").inner_text() == "Rs. -500"  # Reproduces defect
```

---

## 6. Suggested Fix
1. Add `min="1"` and input sanitization to `#quantity`:
   ```html
   <input type="number" name="quantity" id="quantity" value="1" min="1" onkeydown="return event.keyCode !== 69 && event.keyCode !== 189" />
   ```
2. Implement strict backend validation on cart update and checkout payloads:
   ```python
   if item_quantity <= 0:
       return Response({"error": "Quantity must be greater than zero"}, status=400)
   ```
