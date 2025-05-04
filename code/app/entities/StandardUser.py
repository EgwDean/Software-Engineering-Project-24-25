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

        # Fetch user data from the database
        self.fetch_user_data()

    def fetch_user_data(self):
        """Fetch user data from the database."""
        try:
            # Connect to the database
            db = DB.Database()
            connection = db.connect()

            if connection is None:
                print("Failed to connect to the database.")
                return

            # Query the user table
            cursor = connection.cursor()
            query = "SELECT password, phone, email, balance, bank_id, message FROM user WHERE username = %s"
            cursor.execute(query, (self.username,))
            result = cursor.fetchone()

            if result:
                self.password, self.phone, self.email, self.balance, self.bank_id, self.message = result
                print(f"User data fetched for {self.username}: {result}")
            else:
                print(f"No user found with username: {self.username}")

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except Exception as e:
            print(f"An error occurred while fetching user data: {e}")