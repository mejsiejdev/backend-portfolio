from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: str
    image: str
    image_dark: str | None = None
    tags: list[str] = []
    demo: str
    code: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int

class ProjectUpdate(ProjectBase):
    name: str | None = None
    description: str | None = None
    image: str | None = None
    image_dark: str | None = None
    tags: list[str] | None = None
    demo: str | None = None
    code: str | None = None