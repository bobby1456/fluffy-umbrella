from sqlmodel import Session, select, join
from repositories.model.proposition import Proposition, PropositionCreate
from repositories.model.user import User


class PropositionsRepository:

    _session: Session = None

    def __init__(self, session: Session):
        self._session = session

    def create_proposition(self, proposition: PropositionCreate):
        db_proposition = Proposition.model_validate(proposition)
        self._session.add(db_proposition)
        self._session.commit()
        self._session.refresh(db_proposition)
        return db_proposition

    def get_proposition(self, proposition_id):
        return self._session.get(Proposition, proposition_id)
    
    def get_propositions_by_room(self, room_id):
        statement = select(Proposition).join(User).where(User.room_id == room_id)
        return self._session.exec(statement).all()
    
    def get_propositions_by_user(self, user_id):
        statement = select(Proposition).where(Proposition.user_id == user_id)
        return self._session.exec(statement).all()