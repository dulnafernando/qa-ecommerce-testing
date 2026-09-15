# Cross-Browser Testing Guide

## 1. Overview: Cross-Browser Testing vs. Simple Repetition

A key distinction frequently discussed in QA engineering interviews is the difference between **repeating tests** and **testing across rendering engines**.

Running a test three times on Google Chrome simply tests the same browser engine three times. True cross-browser testing verifies application behavior across **distinct rendering and JavaScript execution engines**:

| Browser Engine | Browser Families | JavaScript Engine | Key Engine Characteristics |
|---|---|---|---|
| **Blink** | Google Chrome, Microsoft Edge, Brave, Opera, Vivaldi | V8 | Dominant market share; lenient CSS box-sizing and scroll behavior; standard DOM event loop. |
| **Gecko** | Mozilla Firefox | SpiderMonkey | Separate CSS layout model (sub-pixel grid/flexbox rounding); distinct native form controls (date/time pickers). |
| **WebKit** | Apple Safari (macOS & iOS) | JavaScriptCore (JSC) | Strict Intelligent Tracking Prevention (ITP/cookie policies); distinct touch/click event dispatching; WebKit-specific CSS constraints. |

---

## 2. Why Cross-Browser Testing Matters in E-Commerce

In e-commerce applications like [Automation Exercise](https://automationexercise.com), layout shifts and event timing differences can impact critical revenue paths:
1. **Modal Backdrops & Overlays:** The cart modal (`#cartModal`) uses CSS transitions. WebKit and Gecko handle backdrop blur and modal stacking contexts differently than Blink.
2. **Form Validation:** Modern forms rely on native HTML5 validation (`required`, `checkValidity()`). Different browsers present validation tooltips differently and handle form submission blocking through separate internal event hooks.
3. **AJAX Deletion Timing:** When removing items from the cart, DOM detachment timing varies across JavaScript engines (V8 vs SpiderMonkey vs JSC). Our `row.wait_for(state="detached")` ensures tests remain rock-solid across all three.

---

## 3. How Playwright Implements Cross-Browser Testing

Unlike Selenium (which historically required separate WebDriver binaries like `chromedriver.exe`, `geckodriver.exe`, and Safari driver), Playwright bundles reproducible, patched builds of:
- **Chromium** (open-source foundation of Chrome/Edge)
- **Firefox** (open-source Mozilla engine)
- **WebKit** (open-source Apple engine built for Linux/Windows/macOS)

Playwright controls the browser via direct DevTools protocol connections rather than WebDriver HTTP hops, resulting in faster and more reliable execution.

---

## 4. Execution Commands

### A. Default Local Execution (Chromium only — fastest feedback)
```powershell
pytest
```

### B. Single Browser Engine Execution
```powershell
# Run only against Firefox (Gecko)
pytest --browser firefox

# Run only against WebKit (Safari engine)
pytest --browser webkit

# Run only against Chromium (Blink)
pytest --browser chromium
```

### C. Full Multi-Browser Matrix Execution
```powershell
# Run smoke and cart tests across all 3 engines
pytest tests/ui/test_smoke.py tests/ui/test_cart.py --browser chromium --browser firefox --browser webkit
```

### D. Headed Mode (for visual debugging)
```powershell
pytest --browser firefox --headed
```

---

## 5. Reporting & Artifact Isolation

When running cross-browser:
- **HTML Report (`reports/report.html`):** Tests are automatically tagged by engine: `test_smoke[chromium]`, `test_smoke[firefox]`, `test_smoke[webkit]`.
- **Failure Screenshots (`screenshots/`):** Captured filenames preserve the engine tag (e.g. `test_login_firefox_valid_login_.png`), preventing cross-engine file collisions.
