class TestDataProvider:
    @staticmethod
    def get_registered_details(load_test_data):
        # Extract the registered details from the test data
        return {
            "first_name": load_test_data["mandatory_fields"]["first_name"],
            "last_name": load_test_data["mandatory_fields"]["last_name"],
            "email": load_test_data["mandatory_fields"]["email"]
        }

    @staticmethod
    def get_filled_details(load_test_data):
        # Extract the details from the all fields
        return {
            "first_name": load_test_data["mandatory_fields"]["first_name"],
            "last_name": load_test_data["mandatory_fields"]["last_name"],
            "email": load_test_data["mandatory_fields"]["email"],
            "country": load_test_data["checkout_fields"]["mandatory_billing_address_section"]["country_dropdown"],
            "state": load_test_data["checkout_fields"]["mandatory_billing_address_section"]["state_dropdown"],
            "city": load_test_data["checkout_fields"]["mandatory_billing_address_section"]["city"],
            "address1": load_test_data["checkout_fields"]["mandatory_billing_address_section"]["address1"],
            "zip_code": load_test_data["checkout_fields"]["mandatory_billing_address_section"]["zip_code"],
        }

"""""product_name": load_test_data["product_details"]["product_name"],
        "quantity": load_test_data["product_details"]["quantity"]"""