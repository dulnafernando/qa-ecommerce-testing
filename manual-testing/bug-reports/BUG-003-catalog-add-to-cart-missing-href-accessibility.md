# Bug Report: BUG-003

## Defect Summary
**Title:** Catalog "Add to Cart" Anchor Elements Lack `href` Attribute, Breaking Keyboard Navigation & Screen Readers  
**Bug ID:** `BUG-003`  
**Module:** Catalog / Front-End Accessibility (WAI-ARIA)  
**Reported By:** Dulna Fernando (QA Automation Lead)  
**Date Logged:** 2026-09-15  
**Environment:** Production (`https://automationexercise.com/products`)  
**Severity:** **Medium** (Accessibility standard non-compliance & testability blocker)  
**Priority:** **P3 — Medium**  
**Associated Test Case:** `TC_PROD_006`  

---

## 1. Description
On the Product Catalog page (`/products`), the "Add to cart" interactive elements on product cards are implemented as anchor tags without an `href` attribute:
```html
<a data-product-id="1" class="btn btn-default add-to-cart">
    <i class="fa fa-shopping-cart"></i>Add to cart
</a>
```

Under W3C HTML5 and WAI-ARIA specifications, an `<a>` element without an `href` attribute represents a **placeholder hyperlink**, not an interactive link. Consequently:
1. It does not possess an implicit ARIA role of `link` (`role="link"`).
2. It is excluded from standard browser keyboard `Tab` sequential navigation.
3. Assistive screen readers (NVDA, JAWS, VoiceOver) do not announce it as an interactive action to visually impaired users.
4. Automation engines using standard semantic selectors (e.g. Playwright `get_by_role("link", name="Add to cart")`) locate 0 elements, requiring CSS class workarounds.

---

## 2. Steps to Reproduce
1. Navigate to `https://automationexercise.com/products`.
2. Right-click the "Add to cart" button on any product card and select "Inspect Element".
3. Observe the DOM element:
   - Tag: `<a>`
   - Class: `btn btn-default add-to-cart`
   - Attribute: `href` is completely absent.
4. Attempt to navigate through product cards using only keyboard (`Tab` / `Shift+Tab`).
5. Notice the button cannot be focused or activated via keyboard `Enter` or `Space`.

---

## 3. Expected vs. Actual Results

### Expected:
Interactive button components should use semantic `<button>` elements with `type="button"`, or include `href="javascript:void(0)"` / `role="button"` with `tabindex="0"`:
```html
<button type="button" class="btn btn-default add-to-cart" data-product-id="1">
    <i class="fa fa-shopping-cart"></i>Add to cart
</button>
```

### Actual:
An unlinked `<a>` tag is used without ARIA roles or keyboard focus attributes.

---

## 4. Suggested Fix
Replace anchor tag with semantic button tag in product card templates:
```html
<button type="button" class="btn btn-default add-to-cart" data-product-id="1">
    <i class="fa fa-shopping-cart"></i>Add to cart
</button>
```
