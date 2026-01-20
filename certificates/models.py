from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class Certificate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    issuer: str
    date: str
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    link: str

