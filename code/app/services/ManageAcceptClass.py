import services.Database as DB
from datetime import date

class ManageAcceptClass:
    @staticmethod
    def calculateFinalAmount(total, has_sub):
        """
        Returns the final amount to add to the owner's balance,
        applying commission if no subscription.
        """
        commission = 0.0 if has_sub else 0.10  # 10% commission if no subscription
        return total * (1 - commission)

    @staticmethod
    def checkSub(lease):
        """
        Adds the lease amount to the owner's balance, minus commission if no active subscription.
        Returns (True, None) on success, (False, error_message) on failure.
        """
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return False, "Database connection failed."
        try:
            cur = conn.cursor(dictionary=True)
            owner_username = lease['name_of_user']
            total = lease['number_of_days'] * lease['price_per_day']

            # Inline subscription check
            cur.execute(
                "SELECT * FROM pays_subscription WHERE user_name=%s AND end_date >= %s",
                (owner_username, date.today())
            )
            has_sub = cur.fetchone() is not None

            amount_to_add = ManageAcceptClass.calculateFinalAmount(total, has_sub)
            cur.execute(
                "UPDATE user SET balance = balance + %s WHERE username = %s",
                (amount_to_add, owner_username)
            )
            conn.commit()
            cur.close()
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()