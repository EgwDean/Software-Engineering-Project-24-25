import services.Database as DB

class ReportHandler:
    def __init__(self, report_id):
        self.report_id = report_id


    #refund the user
    def refund(self):
        conn = DB.Database.connect()
        if not conn or not conn.is_connected():
            print("Database connection failed.")
            return

        cursor = conn.cursor()
        try:
            query = """
                SELECT name_reporter, name_of_user, user_who_rents, price_per_day * number_of_days AS total
                FROM reports 
                INNER JOIN vehicle_listing ON id_list_report = id
                INNER JOIN rents ON id = id_of_listing
                WHERE id = %s
            """
            cursor.execute(query, (self.report_id,))
            result = cursor.fetchone()

            if not result:
                print(f"No report found with id {self.report_id}")
                return

            name_reporter, owner_username, renter_username, total = result

            if total is None:
                print("Total amount is None, cannot proceed with refund.")
                return

            if name_reporter == renter_username:
                from_user = owner_username
                to_user = renter_username
            elif name_reporter == owner_username:
                from_user = renter_username
                to_user = owner_username
            else:
                print("Invalid report: Reporter is neither renter nor owner.")
                return

            cursor.execute("SELECT balance FROM user WHERE username = %s", (from_user,))
            from_balance = cursor.fetchone()
            if not from_balance:
                print(f"User {from_user} not found.")
                return
            from_balance = from_balance[0]

            cursor.execute("SELECT balance FROM user WHERE username = %s", (to_user,))
            to_balance = cursor.fetchone()
            if not to_balance:
                print(f"User {to_user} not found.")
                return
            to_balance = to_balance[0]

            if from_balance < total:
                print(f"{from_user} does not have enough balance to proceed with the refund.")
                return

            new_from_balance = from_balance - total
            new_to_balance = to_balance + total

            cursor.execute("UPDATE user SET balance = %s WHERE username = %s", (new_from_balance, from_user))
            cursor.execute("UPDATE user SET balance = %s WHERE username = %s", (new_to_balance, to_user))

            conn.commit()
            print(f"Refunded {total} from {from_user} to {to_user} for report {self.report_id}")

        except Exception as e:
            print(f"Error during refund: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    #suspend the user
    def suspendAccount(self):
        conn = DB.Database.connect()
        if not conn or not conn.is_connected():
            raise Exception("Database connection failed.")

        cursor = conn.cursor()
        try:
            # get the name of the user who made the report and the other user
            query = """
                SELECT name_reporter, name_of_user, user_who_rents
                FROM reports 
                INNER JOIN vehicle_listing ON id_list_report = id
                INNER JOIN rents ON id = id_of_listing
                WHERE id_list_report = %s
            """
            cursor.execute(query, (self.report_id,))
            result = cursor.fetchone()
            if not result:
                raise Exception(f"No report found with id {self.report_id}")

            name_reporter, owner_username, renter_username = result

            # select the user to suspend
            if name_reporter == renter_username:
                user_to_suspend = owner_username
            elif name_reporter == owner_username:
                user_to_suspend = renter_username
            else:
                raise Exception("Invalid report: Reporter is neither renter nor owner.")

            # update the user status to 'suspended'
            cursor.execute("""
                UPDATE user
                SET status = 'suspended'
                WHERE username = %s
            """, (user_to_suspend,))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # ignore the report
    def ignore(self):
        conn = DB.Database.connect()
        if not conn or not conn.is_connected():
            raise Exception("Failed to connect to database.")

        cursor = conn.cursor()
        try:
            update_query = """
                UPDATE reports
                SET status = 'ignored'
                WHERE id_list_report = %s
            """
            cursor.execute(update_query, (self.report_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # complete the report
    def completeReport(self):
        conn = DB.Database.connect()
        if not conn or not conn.is_connected():
            raise Exception("Failed to connect to database.")

        cursor = conn.cursor()
        try:
            update_query = """
                UPDATE reports
                SET status = 'resolved'
                WHERE id_list_report = %s
            """
            cursor.execute(update_query, (self.report_id,))
            conn.commit()
            print(f"Report {self.report_id} marked as complete.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
