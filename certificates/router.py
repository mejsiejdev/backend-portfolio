from fastapi import APIRouter, Depends, HTTPException

from database import supabase
from auth import get_api_key
from .schemas import CertificateRead, CertificateCreate

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/", response_model=list[CertificateRead])
def read_certificates():
    response = (
        supabase.table("certificates").select("*").order("date", desc=True).execute()
    )
    return response.data


@router.post("/", tags=["certificates"], response_model=list[CertificateRead])
def create_certificate(
    certificate: CertificateCreate,
    _: str = Depends(get_api_key),
):
    response = (
        supabase.table("certificates")
        .insert(certificate.model_dump(mode="json"))
        .execute()
    )
    return response.data


@router.delete("/{id}", tags=["certificates"])
def delete_certificate(id: int, _: str = Depends(get_api_key)):
    response = supabase.table("certificates").delete().eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {"message": f"Certificate {id} deleted"}
