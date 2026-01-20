from sqlmodel import SQLModel


class CertificateBase(SQLModel):
    name: str
    issuer: str
    date: str
    tags: list[str] = []
    link: str


class CertificateCreate(CertificateBase):
    pass


class CertificateRead(CertificateBase):
    id: int
