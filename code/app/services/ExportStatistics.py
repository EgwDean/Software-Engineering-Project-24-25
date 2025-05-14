import csv

class ExportStatistics:
    @staticmethod
    def save_to_csv(results, file_path="statistics.csv"):
        try:
            # Αν τα αποτελέσματα είναι κενά, επιστρέφουμε άμεση ειδοποίηση
            if not results:
                raise ValueError("No data to export.")

            # Άνοιγμα αρχείου για εγγραφή
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Γράφουμε την επικεφαλίδα (headers)
                writer.writerow(["Brand", "Model", "Vehicle Type", "Status", "Total Listings"])
                
                # Γράφουμε τα δεδομένα
                for row in results:
                    writer.writerow(row)

            print(f"Statistics exported successfully to {file_path}")

        except Exception as e:
            print(f"Error exporting statistics: {e}")
