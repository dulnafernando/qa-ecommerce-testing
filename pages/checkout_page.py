import re
from playwright.sync_api import Page


class CheckoutPage:
    """Encapsulates interactions with the Order Review & Checkout page."""

    URL = "https://automationexercise.com/checkout"

    def __init__(self, page: Page):
        self.page = page
        self.delivery_address_box = page.locator("#address_delivery")
        self.invoice_address_box = page.locator("#address_invoice")
        self.comment_input = page.locator('textarea[name="message"]')
        self.place_order_button = page.locator('a[href="/payment"]')

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=60000)

    def get_delivery_address_text(self) -> str:
        """Returns the full text of the delivery address card."""
        return self.delivery_address_box.inner_text()

    def get_billing_address_text(self) -> str:
        """Returns the full text of the billing address card."""
        return self.invoice_address_box.inner_text()

    def _get_product_row(self, product_name: str):
        """Finds a product line item row in the order review table."""
        return self.page.locator("#cart_info tbody tr").filter(has_text=product_name)

    @staticmethod
    def _parse_currency(text: str) -> float:
        """Helper to extract numerical float value from a currency string like 'Rs. 500'."""
        match = re.search(r"(\d+(?:\.\d+)?)", text.replace(",", ""))
        if not match:
            raise ValueError(f"Could not parse numeric amount from '{text}'")
        return float(match.group(1))

    def get_product_price(self, product_name: str) -> float:
        """Retrieves and parses the unit price for a given product."""
        row = self._get_product_row(product_name)
        price_text = row.locator(".cart_price p").inner_text()
        return self._parse_currency(price_text)

    def get_product_quantity(self, product_name: str) -> int:
        """Retrieves and parses the quantity for a given product."""
        row = self._get_product_row(product_name)
        qty_text = row.locator(".cart_quantity button").inner_text()
        return int(qty_text.strip())

    def get_product_total(self, product_name: str) -> float:
        """Retrieves and parses the calculated line total for a given product."""
        row = self._get_product_row(product_name)
        total_text = row.locator(".cart_total .cart_total_price").inner_text()
        return self._parse_currency(total_text)

    def get_total_amount(self) -> float:
        """Retrieves and parses the final order total amount from the summary row."""
        # The summary total row has label 'Total Amount' and class .cart_total_price
        total_row = self.page.locator("#cart_info tbody tr").filter(has_text="Total Amount")
        total_text = total_row.locator(".cart_total_price").inner_text()
        return self._parse_currency(total_text)

    def enter_comment(self, comment: str):
        """Enters an order note/comment into the message textarea."""
        self.comment_input.fill(comment)

    def click_place_order(self):
        """Clicks the Place Order button and waits for the payment page to load."""
        self.place_order_button.click()
        self.page.wait_for_url("**/payment", timeout=15000)
