import services.Database as DB

class StandardUser:
    def __init__(self, username):
        self.username = username
        self.password = None
        self.phone = None
        self.email = None
        self.balance = None
        self.bank_id = None
        self.message = None
        self.country = None
        self.city = None
        self.street = None

        # Fetch user data from the database
        self.fetch_user_data()

    def fetch_user_data(self):
        """Fetch user and address data from the database."""
        try:
            # Connect to the database
            db = DB.Database()
            connection = db.connect()

            if connection is None:
                print("Failed to connect to the database.")
                return

            # Query the user table
            cursor = connection.cursor()
            user_query = "SELECT password, phone, email, balance, bank_id, message FROM user WHERE username = %s"
            cursor.execute(user_query, (self.username,))
            user_result = cursor.fetchone()

            if user_result:
                self.password, self.phone, self.email, self.balance, self.bank_id, self.message = user_result
                print(f"User data fetched for {self.username}: {user_result}")
            else:
                print(f"No user found with username: {self.username}")
                cursor.close()
                connection.close()
                return

            # Query the address table
            address_query = "SELECT country, city, street FROM address WHERE username_address = %s"
            cursor.execute(address_query, (self.username,))
            address_result = cursor.fetchone()

            if address_result:
                self.country, self.city, self.street = address_result
                print(f"Address data fetched for {self.username}: {address_result}")
            else:
                print(f"No address found for username: {self.username}")

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except Exception as e:
            print(f"An error occurred while fetching user data: {e}")