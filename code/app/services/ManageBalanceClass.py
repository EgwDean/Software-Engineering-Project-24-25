import services.Database as DB

class ManageBalanceClass:
    @staticmethod
    def get_balance(username):
        db = DB.Database()
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT balance FROM user WHERE username = %s", (username,))
            result = cursor.fetchone()
            return result['balance'] if result and result['balance'] is not None else 0
        finally:
            cursor.close()
            conn.close()