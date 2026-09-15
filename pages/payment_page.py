from playwright.sync_api import Page


class PaymentPage:
    """Encapsulates interactions with the Payment and Order Confirmation pages."""

    URL = "https://automationexercise.com/payment"

    def __init__(self, page: Page):
        self.page = page
        self.name_on_card = page.locator('[data-qa="name-on-card"]')
        self.card_number = page.locator('[data-qa="card-number"]')
        self.cvc = page.locator('[data-qa="cvc"]')
        self.expiry_month = page.locator('[data-qa="expiry-month"]')
        self.expiry_year = page.locator('[data-qa="expiry-year"]')
        self.pay_button = page.locator('[data-qa="pay-button"]')
        self.order_placed_heading = page.locator('[data-qa="order-placed"]')
        self.order_success_text = page.locator("text=Congratulations! Your order has been confirmed!")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=60000)

    def enter_payment_details(
        self,
        name: str = "",
        card_number: str = "",
        cvc: str = "",
        month: str = "",
        year: str = "",
    ):
        """Fills out the credit card payment details."""
        if name:
            self.name_on_card.fill(name)
        if card_number:
            self.card_number.fill(card_number)
        if cvc:
            self.cvc.fill(cvc)
        if month:
            self.expiry_month.fill(month)
        if year:
            self.expiry_year.fill(year)

    def click_pay_and_confirm(self):
        """Submits the payment form."""
        self.pay_button.click()

    def is_order_placed(self) -> bool:
        """Verifies if the order placed confirmation header is visible."""
        return self.order_placed_heading.is_visible()

    def is_field_invalid(self, field_name: str) -> bool:
        """Checks HTML5 validity of a payment input (returns True if invalid)."""
        field = self.page.locator(f'[data-qa="{field_name}"]')
        return field.evaluate("el => !el.checkValidity()")

    def get_field_validation_message(self, field_name: str) -> str:
        """Retrieves the browser's native HTML5 validation message."""
        field = self.page.locator(f'[data-qa="{field_name}"]')
        return field.evaluate("el => el.validationMessage")
