# Bug Report: BUG-004

## Defect Summary
**Title:** Cart Item Deletion Operates Asynchronously Without Confirmation or Undo Action  
**Bug ID:** `BUG-004`  
**Module:** Shopping Cart / User Experience  
**Reported By:** Dulna Fernando (QA Automation Lead)  
**Date Logged:** 2026-09-15  
**Environment:** Production (`https://automationexercise.com/view_cart`)  
**Severity:** **Low** (Usability friction / accidental data removal)  
**Priority:** **P3 — Medium**  
**Associated Test Case:** `TC_CHK_003`  

---

## 1. Description
On the Shopping Cart view (`/view_cart`), clicking the delete icon (`.cart_quantity_delete`) triggers an asynchronous AJAX request that immediately removes the product row from the cart and session.

There is no modal confirmation dialog (e.g. *"Are you sure you want to remove this item?"*) and no temporary "Undo" toast/notification banner. If an end-user accidentally misclicks the delete icon on mobile or desktop, their chosen item is permanently discarded, requiring them to locate the product in the catalog and add it again from scratch.

---

## 2. Steps to Reproduce
1. Navigate to `/products` and add any product to cart.
2. Navigate to `/view_cart`.
3. Click the "X" button (`.cart_quantity_delete`) on the item row.
4. Observe application behavior.

---

## 3. Expected vs. Actual Results

### Expected:
Modern e-commerce standard UX provides either:
1. A brief confirmation prompt before executing the deletion, or
2. A toast notification allowing the user to click `"Undo"` within 5 seconds to restore the item without losing session state.

### Actual:
Item is instantly deleted via AJAX with zero recovery mechanism.

---

## 4. Suggested Fix
Add an inline snackbar/toast notification with an undo callback:
```javascript
function deleteItem(productId) {
    // Hide row temporarily and show toast
    showToast("Item removed from cart. [Undo]", function onUndo() {
        restoreItem(productId);
    });
}
```
