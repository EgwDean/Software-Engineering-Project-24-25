import services.Database as DB

class ManageDeclineClass:
    @staticmethod
    def returnLeseeAmount(lease):
        """
        Refunds the lease amount to the lessee's balance.
        Returns (True, None) on success, (False, error_message) on failure.
        """
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return False, "Database connection failed."
        try:
            cur = conn.cursor()
            total = lease['number_of_days'] * lease['price_per_day']
            cur.execute(
                "UPDATE user SET balance = balance + %s WHERE username = %s",
                (total, lease['user_who_rents'])
            )
            conn.commit()
            cur.close()
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()