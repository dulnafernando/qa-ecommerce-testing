from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.products_page import ProductsPage

PRODUCT_NAME = "Blue Top"


def test_add_single_product_to_cart(page: Page):
    """Test adding a single product to cart and verifying its presence and quantity."""
    products_page = ProductsPage(page)
    products_page.goto()
    products_page.add_product_to_cart_by_name(PRODUCT_NAME)
    products_page.continue_shopping()

    cart_page = CartPage(page)
    cart_page.goto()

    assert cart_page.is_product_in_cart(PRODUCT_NAME), f"Expected '{PRODUCT_NAME}' to be in the cart"
    assert cart_page.get_product_quantity(PRODUCT_NAME) == "1", "Expected initial cart quantity to be 1"


def test_remove_product_from_cart(page: Page):
    """Test removing a product from the cart and verifying it is deleted."""
    products_page = ProductsPage(page)
    products_page.goto()
    products_page.add_product_to_cart_by_name(PRODUCT_NAME)
    products_page.continue_shopping()

    cart_page = CartPage(page)
    cart_page.goto()
    assert cart_page.is_product_in_cart(PRODUCT_NAME), f"Expected '{PRODUCT_NAME}' to be in the cart before removal"

    cart_page.remove_product(PRODUCT_NAME)
    assert not cart_page.is_product_in_cart(PRODUCT_NAME), f"Expected '{PRODUCT_NAME}' to be removed from the cart"
