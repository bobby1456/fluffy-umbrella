from sqlmodel import Session, select
from repositories.model.vote import Vote, VoteCreate

class VotesRepository:
    _session: Session = None

    def __init__(self, session: Session):
        self._session = session

    def create_vote(self, vote: VoteCreate):
        db_vote = vote.model_validate(vote)
        self._session.add(db_vote)
        self._session.commit()
        self._session.refresh(db_vote)
        return db_vote
    
    def get_vote(self, vote_id: int):
        return self._session.get(Vote, vote_id)
    
    def get_votes_by_proposition(self, proposition_id: int):
        statement = select(Vote).where(Vote.proposition_id == proposition_id)
        return self._session.exec(statement).all()