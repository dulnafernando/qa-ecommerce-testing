from playwright.sync_api import Page


class ProductsPage:
    """Encapsulates interactions with the All Products page."""

    URL = "https://automationexercise.com/products"

    def __init__(self, page: Page):
        self.page = page
        self.cart_modal = page.locator("#cartModal")
        self.continue_shopping_button = page.get_by_role("button", name="Continue Shopping")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=60000)

    def add_product_to_cart_by_name(self, product_name: str):
        """Finds a product card by its visible name and adds it to the cart.

        Note: The site renders two 'Add to cart' elements per card:
        1. Inside .productinfo (the static, always-visible card)
        2. Inside .product-overlay (only visible on hover)
        Also, the elements are <a> tags without href attributes, meaning Playwright
        does not consider them accessible links (role='link').
        Targeting '.productinfo .add-to-cart' reliably clicks the static button.
        """
        product_card = self.page.locator(".product-image-wrapper").filter(has_text=product_name)
        product_card.locator(".productinfo .add-to-cart").click()
        self.cart_modal.wait_for(state="visible")

    def continue_shopping(self):
        """Dismisses the 'added to cart' modal to keep browsing."""
        self.continue_shopping_button.click()
        self.cart_modal.wait_for(state="hidden")
