from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    image: str
    image_dark: str | None = None
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    demo: str
    code: str | None = None