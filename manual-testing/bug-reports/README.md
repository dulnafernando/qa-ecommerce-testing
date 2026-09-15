# Defect Management & Bug Reporting Repository

This directory contains real, reproducible defect reports logged against the target application (`https://automationexercise.com`). 

> **Important QA Integrity Rule:**  
> In strict accordance with professional QA standards, **zero bugs in this repository are simulated or fabricated**. Every defect documented here was uncovered during manual exploratory testing, verified with automated reproduction scripts, and remains actively reproducible on the live environment.

---

## 1. The Critical Interview Distinction: Severity vs. Priority

A classic question in technical QA interviews is: **"What is the difference between Severity and Priority, and can you give examples of High Severity/Low Priority and Low Severity/High Priority?"**

### A. Severity (Technical Impact)
- **Defined by:** QA / Engineering.
- **Question it answers:** *"How badly does this bug break the technical functionality or integrity of the system?"*
- **Criteria:** Does it cause data loss, a system crash, financial corruption, security breaches, or a complete blocker of critical paths?
- **Levels:**
  - **Critical**: System crash, data corruption, financial leak, negative checkout totals.
  - **Major**: Core workflow blocked with no workaround.
  - **Medium**: Non-critical feature fails, or workaround exists.
  - **Low**: Minor visual defect, cosmetic misalignment, typo.

### B. Priority (Business Urgency)
- **Defined by:** Product Manager / Business Stakeholder / Lead QA.
- **Question it answers:** *"How urgently must this defect be fixed from a business and customer perspective?"*
- **Criteria:** User exposure, brand damage, revenue loss, release deadlines.
- **Levels:**
  - **P1 (Immediate)**: Blocker; stop the release or hotfix immediately.
  - **P2 (High)**: Major issue; fix in the active sprint.
  - **P3 (Medium)**: Normal bug; schedule for the next planned release.
  - **P4 (Low)**: Minor defect; fix when resources allow.

---

## 2. Real-World Intersection Matrix with Concrete Examples

```
                ▲ HIGH SEVERITY
                │
   High Sev /   │   High Sev /
   Low Pri      │   High Pri (P1)
   [Example 2]  │   [Example 1: BUG-001]
                │
◄───────────────┼───────────────►
 LOW PRIORITY   │   HIGH PRIORITY
                │
   Low Sev /    │   Low Sev /
   Low Pri      │   High Pri
   [Example 4]  │   [Example 3]
                │
                ▼ LOW SEVERITY
```

### Real Examples:
1. **High Severity & High Priority (Critical / P1)**:
   - *Example:* **BUG-001** (Negative order totals at checkout). Allowing customers to check out with negative quantities (`Rs. -100`) directly corrupts financial data and threatens financial loss.
2. **High Severity & Low Priority (Critical / P4)**:
   - *Example:* A catastrophic crash occurs only when an admin generates an annual audit PDF on Windows 7 running Internet Explorer 9. The system crashes completely (High Severity), but the user segment is 0.001% of traffic (Low Priority).
3. **Low Severity & High Priority (Low / P1)**:
   - *Example:* The company's corporate logo on the login page is misspelled or displaying an offensive placeholder image. Technically, all functionality works perfectly (Low Severity), but the public PR and brand damage is severe (Immediate P1 fix).
4. **Low Severity & Low Priority (Low / P4)**:
   - *Example:* **BUG-004** (Cart item deletion lacks an undo prompt). A minor usability inconvenience that does not prevent any user journey.

---

## 3. Active Bug Reports Summary

| Bug ID | Defect Title | Module | Severity | Priority | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| [`BUG-001`](./BUG-001-negative-order-total-checkout.md) | Negative and Zero Product Quantities Allowed at Checkout Resulting in Negative Order Total | Checkout / Cart | **Critical** | **P1 (Immediate)** | Open |
| [`BUG-002`](./BUG-002-api-returns-200-on-client-and-method-errors.md) | REST API Returns HTTP 200 OK Transport Status on 4xx Client and Method Errors | REST API | **Major** | **P2 (High)** | Open |
| [`BUG-003`](./BUG-003-catalog-add-to-cart-missing-href-accessibility.md) | Catalog "Add to Cart" Links Lack `href` Attribute, Breaking Keyboard Navigation & Screen Readers | Catalog / UI | **Medium** | **P3 (Medium)** | Open |
| [`BUG-004`](./BUG-004-cart-removal-missing-confirmation-and-undo.md) | Cart Item Deletion Operates Asynchronously Without Confirmation or Undo Action | Cart / UX | **Low** | **P3 (Medium)** | Open |
