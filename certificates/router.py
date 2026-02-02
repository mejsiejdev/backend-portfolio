from fastapi import APIRouter, Depends, HTTPException

from database import supabase
from auth import get_api_key
from .schemas import CertificateRead, CertificateCreate
from core.cache import cached, invalidate_cache

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/", response_model=list[CertificateRead])
@cached(prefix="certificates")
async def read_certificates():
    response = (
        supabase.table("certificates").select("*").order("date", desc=True).execute()
    )
    return response.data


@router.post("/", tags=["certificates"], response_model=list[CertificateRead])
async def create_certificate(
    certificate: CertificateCreate,
    _: str = Depends(get_api_key),
):
    response = (
        supabase.table("certificates")
        .insert(certificate.model_dump(mode="json"))
        .execute()
    )
    await invalidate_cache("certificates:*")
    return response.data


@router.delete("/{id}", tags=["certificates"])
async def delete_certificate(id: int, _: str = Depends(get_api_key)):
    response = supabase.table("certificates").delete().eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Certificate not found")
    await invalidate_cache("certificates:*")
    return {"message": f"Certificate {id} deleted"}
