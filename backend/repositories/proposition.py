from sqlite3 import Connection

class PropositionsRepository:

    _conn: Connection = None

    def __init__(self, conn: Connection):
        self._conn = conn


    def create_proposition(self, user_id, film_name):
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO proposition (user_id, film_name) VALUES (?, ?)",
            (user_id, film_name)
        )
        self._conn.commit()
        return cursor.lastrowid

    def get_proposition(self, proposition_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM proposition WHERE id = ?", (proposition_id,))
        return cursor.fetchone()
    
    def get_propositions_by_room(self, room_id):
        cursor = self._conn.cursor()
        cursor.execute("Select * from proposition join user on proposition.user_id = user.id where user.room_id = ?", (room_id,))
        return cursor.fetchall()

    def update_proposition(self, proposition_id, film_name=None):
        cursor = self._conn.cursor()
        if film_name:
            cursor.execute(
                "UPDATE proposition SET film_name = ? WHERE id = ?",
                (film_name, proposition_id)
            )
            self._conn.commit()

    def delete_proposition(self, proposition_id):
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM proposition WHERE id = ?", (proposition_id,))
        self._conn.commit()
