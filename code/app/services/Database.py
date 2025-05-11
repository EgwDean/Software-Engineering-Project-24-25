from pathlib import Path
import mysql.connector

class Database:
    host = 'localhost'
    user = 'root'
    database = 'car_rental'
    password_file = Path(__file__).parent.parent.parent / 'db_password.txt'
    connection = None

    @classmethod
    def connect(cls):
        try:
            password = cls.password_file.read_text(encoding='utf-8').strip()

            print("Creating connection...")
            cls.connection = mysql.connector.connect(
                host=cls.host,
                user=cls.user,
                password=password,
                database=cls.database
            )

            if cls.connection.is_connected():
                print("Successfully connected to the database.")
                return cls.connection
            else:
                print("Failed to connect to the database.")

        except FileNotFoundError:
            print(f"Password file not found at {cls.password_file}")
        except mysql.connector.Error as e:
            print(f"Error while connecting to MySQL: {e}")
        
        return None

    @classmethod
    def close(cls):
        if cls.connection and cls.connection.is_connected():
            cls.connection.close()
            print("MySQL connection closed.")
