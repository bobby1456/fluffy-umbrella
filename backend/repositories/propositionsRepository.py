from sqlmodel import Session, select, join
from repositories.model.proposition import Proposition
from repositories.model.user import User


class PropositionsRepository:

    _session: Session = None

    def __init__(self, session: Session):
        self._session = session

    def create_proposition(self, Proposition: Proposition):
        self._session.add(Proposition)
        self._session.commit()
        self._session.refresh(Proposition)
        return Proposition

    def get_proposition(self, proposition_id):
        return self._session.get(Proposition, proposition_id)
    
    def get_propositions_by_room(self, room_id):
        statement = select(Proposition).join(User).where(User.room_id == room_id)
        return self._session.exec(statement).all()