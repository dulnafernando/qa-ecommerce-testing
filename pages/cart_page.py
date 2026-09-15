from playwright.sync_api import Page


class CartPage:
    """Encapsulates interactions with the Shopping Cart page."""

    URL = "https://automationexercise.com/view_cart"

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=60000)

    def _get_product_row(self, product_name: str):
        """Returns the locator for a specific product row in the cart table."""
        return self.page.locator("#cart_info_table tbody tr").filter(has_text=product_name)

    def is_product_in_cart(self, product_name: str) -> bool:
        """Checks if a product is currently listed in the cart table."""
        return self._get_product_row(product_name).is_visible()

    def get_product_quantity(self, product_name: str) -> str:
        """Retrieves the quantity value for the given product."""
        row = self._get_product_row(product_name)
        return row.locator(".cart_quantity button").inner_text()

    def remove_product(self, product_name: str):
        """Removes a product from the cart and waits for row detachment.

        The site removes cart items asynchronously via AJAX. Waiting for
        state='detached' ensures Playwright synchronizes with the DOM update
        and prevents race conditions in test assertions.
        """
        row = self._get_product_row(product_name)
        row.locator(".cart_delete a").click()
        row.wait_for(state="detached")

    def proceed_to_checkout(self):
        """Clicks the Proceed To Checkout button."""
        self.page.locator(".check_out").click()

    def clear_cart(self):
        """Removes every item currently in the cart."""
        if not self.page.url.endswith("/view_cart"):
            self.goto()
        delete_buttons = self.page.locator(".cart_delete a")
        while delete_buttons.count() > 0:
            delete_buttons.first.click()
            self.page.wait_for_timeout(500)  # brief pause for the row to actually remove

