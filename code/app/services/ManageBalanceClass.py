import services.Database as DB
from datetime import date

class ManageBalanceClass:

    @staticmethod
    def checkBalance(user, selected_package):
        """
        Checks if user has enough balance for the selected package.
        If yes, deducts balance and creates subscription.
        Returns (True, None) on success, (False, error_message) on failure.
        """
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return False, "Database connection failed."
        cursor = conn.cursor()
        try:
            # Check balance
            cursor.execute("SELECT balance FROM user WHERE username = %s", (user.username,))
            result = cursor.fetchone()
            if not result or result[0] is None:
                return False, "Could not retrieve balance."
            user_balance = result[0]
            plan_price = selected_package['price']
            if user_balance < plan_price:
                return False, "Inadequate balance."
            # Deduct balance
            cursor.execute("UPDATE user SET balance = balance - %s WHERE username = %s", (plan_price, user.username))
            # Create subscription (1 month from today)
            today = date.today()
            month = today.month + 1
            year = today.year
            if month > 12:
                month = 1
                year += 1
            from calendar import monthrange
            try:
                end = date(year, month, today.day)
            except ValueError:
                end = date(year, month, monthrange(year, month)[1])
            cursor.execute(
                "INSERT INTO pays_subscription (user_name, sub_plan, start_date, end_date) VALUES (%s, %s, %s, %s)",
                (user.username, selected_package['plan'], today, end)
            )
            conn.commit()
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()