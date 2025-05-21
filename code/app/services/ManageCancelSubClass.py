import services.Database as DB
from datetime import date

class ManageCancelSubClass:
    @staticmethod
    def cancel_subscription(username):
        """
        Deletes the active subscription (with end_date >= today) for the given user from pays_subscription.
        Returns True if a subscription was deleted, False otherwise.
        """
        db = DB.Database()
        conn = db.connect()
        cursor = conn.cursor()
        try:
            # Delete only the active subscription(s)
            cursor.execute(
                "DELETE FROM pays_subscription WHERE user_name = %s AND end_date >= %s",
                (username, date.today())
            )
            conn.commit()
            deleted = cursor.rowcount > 0
        except Exception as e:
            print("Error cancelling subscription:", e)
            deleted = False
        finally:
            cursor.close()
            conn.close()
        return deleted