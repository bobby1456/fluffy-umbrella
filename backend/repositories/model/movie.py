from sqlmodel import Field, SQLModel

class MovieBase(SQLModel):
    title: str
    year: int
    imdbid: str
    type: str 
    poster: str

class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class MoviePublic(MovieBase):
    id: int

class MovieCreate(MovieBase):
    pass