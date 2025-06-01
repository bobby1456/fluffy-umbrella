from sqlmodel import Session, select
from repositories.model.room import Room

class RoomsRepository:

    _session: Session = None

    def __init__(self, session):
        self._session = session

    def create_room(self, room: Room):
        self._session.add(room)
        self._session.commit()
        self._session.refresh(room)
        return room

    def get_room(self, room_id):
        return self._session.get(Room, room_id)

    def get_room_by_name(self, name:str):
        statement = select(Room).where(Room.name == name)
        return self._session.exec(statement).first()
    