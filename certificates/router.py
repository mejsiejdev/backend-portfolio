from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from auth import get_api_key
from .models import Certificate
from .schemas import CertificateRead, CertificateCreate

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/", response_model=list[CertificateRead])
def read_certificates(session: Session = Depends(get_session)):
    certificates = session.exec(select(Certificate)).all()
    return certificates


@router.post("/", tags=["certificates"], response_model=CertificateRead)
def create_certificate(
    certificate: CertificateCreate,
    session: Session = Depends(get_session),
    _: str = Depends(get_api_key),
):
    db_certificate = Certificate.model_validate(certificate)
    session.add(db_certificate)
    session.commit()
    session.refresh(db_certificate)
    return db_certificate


@router.delete("/{id}", tags=["certificates"])
def delete_certificate(
    id: int, session: Session = Depends(get_session), _: str = Depends(get_api_key)
):
    certificate = session.get(Certificate, id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    session.delete(certificate)
    session.commit()
    return {"message": f"Certificate {id} deleted"}
