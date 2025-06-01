from sqlmodel import Session, select
from repositories.model.vote import Vote

class VotesRepository:
    _session: Session = None

    def __init__(self, session: Session):
        self._session = session

    def create_vote(self, vote: Vote):
        self._session.add(vote)
        self._session.commit()
        self._session.refresh(vote)
        return vote