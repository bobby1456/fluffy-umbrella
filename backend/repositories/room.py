from sqlite3 import Connection

class RoomsRepository:

    _conn:Connection = None

    def __init__(self, conn):
        self._conn = conn

    def create_room(self, name):
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO room (name) VALUES (?)",
            (name,)
        )
        self._conn.commit()
        cursor = self._conn.cursor()
        cursor.execute("SELECT id FROM room WHERE name = ?", (name,))
        print(f"Room created with ID: {cursor.fetchone()}")
        return cursor.lastrowid

    def get_room(self, room_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM room WHERE id = ?", (room_id,))
        return cursor.fetchone()

    def get_room_by_name(self, name):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM room WHERE name = ?", (name,))
        return cursor.fetchone()
        
    def get_users_in_room(self, room_id: int):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM user WHERE room_id = ?", (room_id,))
        return cursor.fetchall()

    def update_room(self, room_id, name=None):
        cursor = self._conn.cursor()
        fields = []
        values = []
        if name:
            fields.append("name = ?")
            values.append(name)
        values.append(room_id)
        cursor.execute(f"UPDATE room SET {', '.join(fields)} WHERE id = ?", values)
        self._conn.commit()

    def delete_room(self, room_id):
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM room WHERE id = ?", (room_id,))
        self._conn.commit()
