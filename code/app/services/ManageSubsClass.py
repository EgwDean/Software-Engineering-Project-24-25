import services.Database as DB
from datetime import date

class ManageSubsClass:
    @staticmethod
    def has_active_subscription(username):
        db = DB.Database()
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM pays_subscription WHERE user_name=%s AND end_date >= %s",
            (username, date.today())
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    @staticmethod
    def get_active_subscription_details(username):
        db = DB.Database()
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT s.plan, s.price, s.commission, p.start_date, p.end_date "
            "FROM pays_subscription p JOIN subscription s ON p.sub_plan = s.plan "
            "WHERE p.user_name = %s AND p.end_date >= %s",
            (username, date.today())
        )
        sub = cursor.fetchone()
        cursor.close()
        conn.close()
        return sub