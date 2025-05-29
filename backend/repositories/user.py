from sqlite3 import Connection

class UsersRepository:
    _conn:Connection = None

    def __init__(self, conn):
        self._conn = conn
    
    def create_user(self, username, room_id):
        print(f"Creating user: {username} in room: {room_id}")
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO user (username, room_id) VALUES (?, ?)",
            (username, room_id)
        )
        self._conn.commit()
        return cursor.lastrowid

    def get_user(self, user_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def update_user(self, user_id, username=None, email=None, password_hash=None):
        cursor = self._conn.cursor()
        fields = []
        values = []
        if username:
            fields.append("username = ?")
            values.append(username)
        if email:
            fields.append("email = ?")
            values.append(email)
        if password_hash:
            fields.append("password_hash = ?")
            values.append(password_hash)
        values.append(user_id)
        cursor.execute(f"UPDATE user SET {', '.join(fields)} WHERE id = ?", values)
        self._conn.commit()

    def delete_user(self, user_id):
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        self._conn.commit()
