from sqlmodel import Session, select
from repositories.model.user import User, UserCreate

class UsersRepository:
    _session:Session = None

    def __init__(self, session):
        self._session = session
    
    def create_user(self, user:UserCreate):
        db_user = User.model_validate(user)
        self._session.add(db_user)
        self._session.commit()
        self._session.refresh(db_user)
        return db_user

    def get_user(self, user_id):
        return self._session.get(User, user_id)
    
    def get_users_in_room(self, room_id: int):
        statement = select(User).where(User.room_id == room_id)
        return self._session.exec(statement).all()