import csv

class ExportStatistics:
    @staticmethod
    def save_to_csv(results, file_path="statistics.csv"):
        try:
            # notify if results is empty
            if not results:
                raise ValueError("No data to export.")

            # open the file in write mode
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # write the header
                writer.writerow(["Brand", "Model", "Vehicle Type", "Status", "Total Listings"])
                
                # write the data
                for row in results:
                    writer.writerow(row)

            print(f"Statistics exported successfully to {file_path}")

        except Exception as e:
            print(f"Error exporting statistics: {e}")
