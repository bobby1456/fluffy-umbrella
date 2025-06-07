from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from repositories.model.room import Room, RoomCreate

class RoomsRepository:

    _session: Session = None

    def __init__(self, session):
        self._session = session

    def create_room(self, room: RoomCreate):
        db_room = Room.model_validate(room)
        self._session.add(db_room)
        self._session.commit()
        self._session.refresh(db_room)
        return db_room

    def find_room(self, room_name: str):
        statement = select(Room).where(Room.name == room_name)
        return self._session.exec(statement).first()

    def get_room(self, room_id):
        return self._session.exec(select(Room).where(Room.id == room_id).options(selectinload(Room.users))).first()

    def get_room_by_name(self, name:str):
        statement = select(Room).where(Room.name == name)
        return self._session.exec(statement).first()
    