from sqlmodel import SQLModel
from datetime import date


class CertificateBase(SQLModel):
    name: str
    issuer: str
    date: date
    tags: list[str] = []
    link: str


class CertificateCreate(CertificateBase):
    pass


class CertificateRead(CertificateBase):
    id: int
