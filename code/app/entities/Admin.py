import services.Database as DB

class Admin:
    def __init__(self, username):
        self.username = username
        self.password = None

        # Fetch admin data from the database
        self.fetch_admin_data()

    def fetch_admin_data(self):
        """Fetch admin data from the database."""
        try:
            # Connect to the database
            db = DB.Database()
            connection = db.connect()

            if connection is None:
                print("Failed to connect to the database.")
                return

            # Query the admin table
            cursor = connection.cursor()
            query = "SELECT password FROM admin WHERE username = %s"
            cursor.execute(query, (self.username,))
            result = cursor.fetchone()

            if result:
                self.password = result[0]
                print(f"Admin data fetched for {self.username}: {result}")
            else:
                print(f"No admin found with username: {self.username}")

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except Exception as e:
            print(f"An error occurred while fetching admin data: {e}")