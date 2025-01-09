from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from .checkout_page import CheckoutPage

class ShippingMethodSection(BasePage):
    GROUND_METHOD_RADIO_BUTTON = (By.ID, "shippingoption_0")
    NEXT_DAY_METHOD_RADIO_BUTTON = (By.ID, "shippingoption_1")
    SECOND_DAY_METHOD_RADIO_BUTTON = (By.ID, "sshippingoption_2")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.shipping-method-next-step-button")

    def select_shipping_method(self, method="ground"):
        if method == "ground":
            self.click(self.GROUND_METHOD_RADIO_BUTTON)
        elif method == "next_day":
            self.click(self.NEXT_DAY_METHOD_RADIO_BUTTON)
        elif method == "second_day":
            self.click(self.SECOND_DAY_METHOD_RADIO_BUTTON)
        else:
            raise ValueError(f"Invalid shipping method: {method}")

        self.click(self.CONTINUE_BUTTON)