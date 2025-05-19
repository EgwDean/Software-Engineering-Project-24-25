import services.Database as DB

class FilterStatistics:
    @staticmethod
    def fetch_statistics(brand="", model="", date="", vehicle_type="", status=""):
        conn = DB.Database.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()

            # get the filtered statistics
            
            try:
                query = """
                    SELECT brand, model, vehicle_type, status, COUNT(*) as total_listings
                    FROM vehicle_listing
                    WHERE 1=1
                """
                values = []

                if brand:
                    query += " AND brand LIKE %s"
                    values.append(f"%{brand}%")
                if model:
                    query += " AND model LIKE %s"
                    values.append(f"%{model}%")
                if date:
                    query += " AND DATE(to_date) > %s"
                    values.append(date)
                if vehicle_type:
                    query += " AND vehicle_type LIKE %s"
                    values.append(f"%{vehicle_type}%")
                if status:
                    query += " AND status = %s"
                    values.append(status)

                query += """
                    GROUP BY brand, model, vehicle_type, status
                """
                cursor.execute(query, values)
                return cursor.fetchall()
            finally:
                cursor.close()
                conn.close()
        return []
