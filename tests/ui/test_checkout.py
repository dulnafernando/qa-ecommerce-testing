import json
from pathlib import Path
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage

DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "login_data.json"

with open(DATA_FILE, encoding="utf-8") as f:
    login_cases = json.load(f)

VALID_USER = next(case for case in login_cases if case["case"] == "valid_login")
PRODUCT_NAME = "Blue Top"


def _login_and_add_product(page: Page, product_name: str = PRODUCT_NAME):
    """Helper to log in with a valid account and add a product to the cart."""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(VALID_USER["email"], VALID_USER["password"])
    assert login_page.is_logged_in(), "Precondition failed: Login must succeed before checkout."

    # Clear shared account-level cart to guarantee isolated test starting state
    cart_page = CartPage(page)
    cart_page.clear_cart()

    products_page = ProductsPage(page)
    products_page.goto()
    products_page.add_product_to_cart_by_name(product_name)
    products_page.continue_shopping()


def test_cart_totals_carry_through_to_checkout(page: Page):
    """Verify delivery details and mathematical consistency of price, quantity, and totals in checkout."""
    _login_and_add_product(page, PRODUCT_NAME)

    cart_page = CartPage(page)
    cart_page.goto()
    assert cart_page.is_product_in_cart(PRODUCT_NAME), f"Expected '{PRODUCT_NAME}' to be in the cart."
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(page)

    # 1. Verify address details are populated from the registered account
    delivery_text = checkout_page.get_delivery_address_text()
    assert len(delivery_text) > 0, "Delivery address should not be empty."
    assert "your delivery address" in delivery_text.lower()

    # 2. Verify calculated values: (unit_price * quantity == line_total)
    price = checkout_page.get_product_price(PRODUCT_NAME)
    quantity = checkout_page.get_product_quantity(PRODUCT_NAME)
    line_total = checkout_page.get_product_total(PRODUCT_NAME)

    assert price > 0, f"Expected positive unit price, got {price}"
    assert quantity > 0, f"Expected positive quantity, got {quantity}"
    assert price * quantity == line_total, (
        f"Calculated line total mismatch: {price} * {quantity} != {line_total}"
    )

    # 3. Verify order total matches line item sum
    order_total = checkout_page.get_total_amount()
    assert line_total == order_total, (
        f"Order total mismatch: expected {line_total}, got {order_total}"
    )


def test_checkout_with_missing_payment_fields(page: Page):
    """Negative test: Submitting payment with missing required fields must be blocked by HTML5 form validation."""
    _login_and_add_product(page, PRODUCT_NAME)

    cart_page = CartPage(page)
    cart_page.goto()
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(page)
    checkout_page.click_place_order()

    payment_page = PaymentPage(page)
    # Attempt to submit with all fields empty
    payment_page.click_pay_and_confirm()

    # Verify form validation blocks navigation and marks required fields invalid
    assert "payment" in page.url, f"Expected to remain on payment page, but URL is {page.url}"
    assert payment_page.is_field_invalid("name-on-card"), "Expected 'name-on-card' to fail HTML5 validity check."
    assert not payment_page.is_order_placed(), "Order should not be placed when payment fields are empty."


def test_valid_checkout_end_to_end(page: Page):
    """End-to-end happy path: Log in, add product, proceed to checkout, add order comment, pay, and confirm order."""
    _login_and_add_product(page, PRODUCT_NAME)

    cart_page = CartPage(page)
    cart_page.goto()
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(page)
    checkout_page.enter_comment("Automated test order - please deliver with care.")
    checkout_page.click_place_order()

    payment_page = PaymentPage(page)
    payment_page.enter_payment_details(
        name="Test User",
        card_number="4111111111111111",
        cvc="311",
        month="12",
        year="2028",
    )
    payment_page.click_pay_and_confirm()

    # Wait for order confirmation
    page.wait_for_url("**/payment_done/**", timeout=15000)
    assert payment_page.is_order_placed(), "Expected 'ORDER PLACED!' confirmation heading to be visible."
    assert payment_page.order_success_text.is_visible(), "Expected order confirmation message to be visible."
