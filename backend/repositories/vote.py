from sqlite3 import Connection

class VotesRepository:
    _conn: Connection = None

    def __init__(self, conn: Connection):
        self._conn = conn

    def create_vote(self, proposition_id, user_id, vote_type):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO vote (proposition_id, user_id, vote_type) VALUES (?, ?, ?)",
                (proposition_id, user_id, vote_type)
            )
            self._conn.commit()
            return cursor.lastrowid

    def get_vote(self, vote_id):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM vote WHERE id = ?", (vote_id,))
            return cursor.fetchone()

    def update_vote(self, vote_id, vote_type):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "UPDATE vote SET vote_type = ? WHERE id = ?",
                (vote_type, vote_id)
            )
            self._conn.commit()

    def delete_vote(self, vote_id):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute("DELETE FROM vote WHERE id = ?", (vote_id,))
            self._conn.commit()