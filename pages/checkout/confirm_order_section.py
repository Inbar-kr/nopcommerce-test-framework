from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmOrderSection(BasePage):
    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONFIRM_BUTTON = (By.CLASS_NAME, "button-1.confirm-order-next-step-button")

    # Billing Info
    BILLING_NAME = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'name')]")
    BILLING_EMAIL = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'email')]")
    BILLING_PHONE = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'phone')]")
    BILLING_FAX = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'fax')]")
    BILLING_COUNTRY = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'country')]")
    BILLING_STATE = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'stateprovince')]")
    BILLING_CITY = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'city')]")
    BILLING_COUNTY = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'county')]")
    BILLING_ADDRESS1 = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'address1')]")
    BILLING_ADDRESS2 = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'address2')]")
    BILLING_ZIP_CODE = (By.XPATH, "//div[@class='billing-info']//li[contains(@class, 'zippostalcode')]")

    # payment and shipping method info
    payment_method = (By.XPATH, "//li[contains(@class, 'payment-method')]//span[@class='value']")
    shipping_method = (By.XPATH, "//li[contains(@class, 'shipping-method')]//span[@class='value']")

    PRODUCT_NAME = (By.CLASS_NAME, "product-name")
    PRODUCT_QUANTITY = (By.CLASS_NAME, "product-quantity")

    ORDER_COMPLETED_MESSAGE = (By.CSS_SELECTOR, ".section.order-completed")
    COMPLETED_CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.order-completed-continue-button")

    def confirm_order(self):
        self.click(self.CONFIRM_BUTTON)

    def prev_page(self):
        self.click(self.BACK_SHIPPING_LINK)

    def get_order_summary_details(self):
        product_name = self.get_element_text(self.PRODUCT_NAME)
        product_quantity = self.get_element_text(self.PRODUCT_QUANTITY)

        return {
            "product_name": product_name,
            "quantity": product_quantity
        }

    def get_confirm_order_details(self):
        try:
            full_name = self.get_text_value(self.BILLING_NAME).strip()

            if not full_name:
                first_name, last_name = "", ""
            else:
                name_parts = full_name.split(" ", 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""

            return {
                "first_name": first_name,
                "last_name": last_name,
                "email": self.get_text_value(self.BILLING_EMAIL).replace("Email:", "").strip(),
                "country": self.get_text_value(self.BILLING_COUNTRY).strip(),
                "state": self.get_text_value(self.BILLING_STATE).strip(),
                "city": self.get_text_value(self.BILLING_CITY).strip(),
                "address1": self.get_text_value(self.BILLING_ADDRESS1).strip(),
                "zip_code": self.get_text_value(self.BILLING_ZIP_CODE).strip(),
                "phone_number": self.get_text_value(self.BILLING_PHONE).replace("Phone:", "").strip(),
            }
        except Exception as e:
            self.logger.error(f"Error extracting confirm order details: {str(e)}")
            raise

    def complete_order(self):
        order_message = self.get_element_text(self.ORDER_COMPLETED_MESSAGE)
        assert "Your order has been successfully processed" in order_message, \
            f"Order completion message not found. Actual: {order_message}"

        self.click(self.COMPLETED_CONTINUE_BUTTON)
