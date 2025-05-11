import services.Database as DB

class VehicleListing:
    def __init__(self, listing_id):
        self.id = listing_id
        self.name_of_user = None
        self.price_per_day = None
        self.vehicle_type = None
        self.brand = None
        self.model = None
        self.year = None
        self.total_km = None
        self.fuel_type = None
        self.description = None
        self.from_date = None
        self.to_date = None
        self.status = None

        # Fetch vehicle listing data from the database
        self.fetch_listing_data()

    def fetch_listing_data(self):
        """Fetch vehicle listing data from the database."""
        try:
            # Connect to the database
            db = DB.Database()
            connection = db.connect()

            if connection is None:
                print("Failed to connect to the database.")
                return

            # Query the vehicle_listing table
            cursor = connection.cursor()
            query = """
                SELECT name_of_user, price_per_day, vehicle_type, brand, model, year, 
                       total_km, fuel_type, description, from_date, to_date, status
                FROM vehicle_listing
                WHERE id = %s
            """
            cursor.execute(query, (self.id,))
            result = cursor.fetchone()

            if result:
                (
                    self.name_of_user,
                    self.price_per_day,
                    self.vehicle_type,
                    self.brand,
                    self.model,
                    self.year,
                    self.total_km,
                    self.fuel_type,
                    self.description,
                    self.from_date,
                    self.to_date,
                    self.status,
                ) = result
                print(f"Vehicle listing data fetched for ID {self.id}: {result}")
            else:
                print(f"No vehicle listing found with ID: {self.id}")

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except Exception as e:
            print(f"An error occurred while fetching vehicle listing data: {e}")