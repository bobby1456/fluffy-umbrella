from sqlmodel import Session, select
from repositories.model.movie import Movie, MovieCreate, MoviePublic

class MoviesRepository:
    _session: Session = None

    def __init__(self, session: Session):
        self._session = session

    def create_movie(self, movie: MovieCreate) -> Movie:
        db_movie = Movie.model_validate(movie)
        self._session.add(db_movie)
        self._session.commit()
        self._session.refresh(db_movie)
        return db_movie

    def get_movie(self, movie_id: int) -> Movie | None:
        return self._session.get(Movie, movie_id)

    def get_movie_by_imdbid(self, imdbid: str) -> list[MoviePublic]:
        statement = select(Movie).where(Movie.imdbid == imdbid)
        return self._session.exec(statement).all()
