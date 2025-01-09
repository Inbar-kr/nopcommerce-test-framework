class TestDataProvider:
    @staticmethod
    def get_registered_details(load_test_data):
        # Extract the registered details from the test data
        return {
            "first_name": load_test_data["mandatory_fields"]["first_name"],
            "last_name": load_test_data["mandatory_fields"]["last_name"],
            "email": load_test_data["mandatory_fields"]["email"]
        }

