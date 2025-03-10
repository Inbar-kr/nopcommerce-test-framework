from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ShippingMethodSection(BasePage):
    GROUND_METHOD_RADIO_BUTTON = (By.ID, "shippingoption_0")
    NEXT_DAY_METHOD_RADIO_BUTTON = (By.ID, "shippingoption_1")
    SECOND_DAY_METHOD_RADIO_BUTTON = (By.ID, "sshippingoption_2")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.shipping-method-next-step-button")

    def select_shipping_method(self, method="ground"):
        shipping_methods = {
            "ground": self.GROUND_METHOD_RADIO_BUTTON,
            "next_day": self.NEXT_DAY_METHOD_RADIO_BUTTON,
            "second_day": self.SECOND_DAY_METHOD_RADIO_BUTTON
        }

        if method not in shipping_methods:
            raise ValueError(f"Invalid shipping method: {method}")

        self.click(shipping_methods[method])
        self.click(self.CONTINUE_BUTTON)
