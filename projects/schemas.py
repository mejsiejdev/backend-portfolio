from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str
    tags: list[str] = []
    demo: str
    code: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    image: str
    image_dark: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    demo: str | None = None
    code: str | None = None
