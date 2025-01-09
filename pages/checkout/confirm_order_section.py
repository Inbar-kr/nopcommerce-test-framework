from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmOrderSection(BasePage):
    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")

    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.payment-info-next-step-button")

    def confirm_order(self):
        self.click(self.BACK_SHIPPING_LINK)
        self.click(self.CONTINUE_BUTTON)