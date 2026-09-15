# Test Cases: Products & Catalog

This suite covers product discovery, keyword searching, category filtering, product detail presentation, and quantity boundary validation.

---

## Summary Matrix

| Test Case ID | Test Case Title | Type | Priority | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_PROD_001** | Full Product Catalog Display & Pagination/Card Layout | Functional | P1 | Major | **PASS** |
| **TC_PROD_002** | Keyword Search with Matching Product Name | Functional | P1 | Major | **PASS** |
| **TC_PROD_003** | Keyword Search with Non-Existent Term | Functional | P2 | Medium | **PASS** |
| **TC_PROD_004** | Product Details Page Metadata Verification | Functional | P1 | Major | **PASS** |
| **TC_PROD_005** | Quantity Input Boundary Value Analysis (Zero & Negative) | Boundary | P1 | Critical | **FAIL (Defect BUG-001)** |
| **TC_PROD_006** | Catalog Add to Cart Button Keyboard Accessibility | Usability / A11y | P3 | Medium | **FAIL (Defect BUG-003)** |

---

## Detailed Test Cases

### TC_PROD_001: Full Product Catalog Display & Card Layout
- **Module:** Catalog
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** Server catalog contains products.
- **Test Steps:**
  1. Navigate to `https://automationexercise.com/products`.
  2. Verify page title is `"Automation Exercise - All Products"`.
  3. Verify presence of header title `"ALL PRODUCTS"`.
  4. Inspect first product card for presence of:
     - Product Image (`.productinfo img`)
     - Price (`.productinfo h2`)
     - Product Name (`.productinfo p`)
     - Add to Cart button (`.productinfo a.add-to-cart`)
- **Expected Result:**
  - Catalog renders a minimum of 30 products in a responsive grid layout.
  - Every card contains valid pricing, title, and interactive add-to-cart trigger.
- **Actual Result:** All product cards render with expected imagery and textual details.
- **Status:** **PASS**

---

### TC_PROD_002: Keyword Search with Matching Product Name
- **Module:** Catalog & Search
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** Catalog contains items matching `"top"`.
- **Test Steps:**
  1. Navigate to `https://automationexercise.com/products`.
  2. Locate search input `#search_product`.
  3. Enter keyword `"top"`.
  4. Click search button `#submit_search`.
- **Expected Result:**
  - Page navigates to `/products?search=top`.
  - Header displays `"SEARCHED PRODUCTS"`.
  - All returned product cards have titles or descriptions containing the term `"top"`.
- **Actual Result:** Returned cards display matching tops/t-shirts with zero unrelated products.
- **Status:** **PASS**

---

### TC_PROD_003: Keyword Search with Non-Existent Term
- **Module:** Catalog & Search
- **Priority:** Medium (P2)
- **Severity:** Medium
- **Execution Type:** Manual
- **Preconditions:** On `/products`.
- **Test Steps:**
  1. Enter non-existent keyword: `"xyznonexistentitem12345"`.
  2. Click `#submit_search`.
- **Expected Result:**
  - System indicates zero results found cleanly (empty grid or friendly "No products found" message).
  - No 500 internal server error or unhandled script exception.
- **Actual Result:** Page displays "SEARCHED PRODUCTS" title with 0 cards rendered.
- **Status:** **PASS**

---

### TC_PROD_004: Product Details Page Metadata Verification
- **Module:** Product Details
- **Priority:** High (P1)
- **Severity:** Major
- **Execution Type:** Automated & Manual
- **Preconditions:** Product ID 1 exists.
- **Test Steps:**
  1. Click `View Product` on first product card (navigates to `/product_details/1`).
  2. Verify presence of:
     - Product name (`Blue Top`)
     - Category (`Women > Tops`)
     - Price (`Rs. 500`)
     - Availability (`In Stock`)
     - Condition (`New`)
     - Brand (`Polo`)
- **Expected Result:**
  - All attributes display readable, non-null values.
- **Actual Result:** Metadata rendered completely and formatted consistently.
- **Status:** **PASS**

---

### TC_PROD_005: Quantity Input Boundary Value Analysis (Zero & Negative)
- **Module:** Product Details / Cart Integrity
- **Priority:** High (P1)
- **Severity:** Critical
- **Execution Type:** Manual & Exploratory
- **Preconditions:** On `/product_details/1`.
- **Test Steps:**
  1. Clear quantity input field `#quantity`.
  2. Enter negative value `-2` (or `0`).
  3. Click `Add to cart` button.
  4. Observe modal confirmation dialog.
  5. Click `View Cart` in modal.
- **Expected Result:**
  - Input field enforces `min="1"`.
  - Submission is blocked with a validation message (e.g., "Value must be greater than or equal to 1").
  - Negative or zero quantities cannot be placed into the shopping cart.
- **Actual Result:** 
  - The modal pops up: `"Your product has been added to cart."`.
  - The cart displays: `Qty: -2`, `Total: Rs. -1000`.
  - Proceeding to checkout creates a negative order total of `Rs. -100`.
- **Status:** **FAIL (Logged as BUG-001)**

---

### TC_PROD_006: Catalog Add to Cart Button Keyboard Accessibility
- **Module:** Catalog / Accessibility (a11y)
- **Priority:** Low (P3)
- **Severity:** Medium
- **Execution Type:** Manual & DOM Inspection
- **Preconditions:** On `/products`.
- **Test Steps:**
  1. Inspect the DOM element for `.productinfo .add-to-cart`.
  2. Attempt to navigate using keyboard `Tab` key.
- **Expected Result:**
  - Element has `href` attribute if it is an `<a>` tag, or is implemented as `<button type="button">`.
  - Element receives focus during Tab traversal.
- **Actual Result:**
  - Element is `<a data-product-id="1" class="btn btn-default add-to-cart">` without an `href` attribute.
  - Per HTML5 / WAI-ARIA standards, an `<a>` without `href` is not a link and is not focusable by default.
- **Status:** **FAIL (Logged as BUG-003)**
