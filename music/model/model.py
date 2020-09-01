
class Model():
    def _db_conn(self):
        return 'connected to db'

    def _exec(self, sql, values):
        """Executing SQL queries
        sql:
            SQL query string
        values: tuple
            values to insert for a sql string
        """
        return f"Changes commited {values}"
