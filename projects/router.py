import uuid
import json
from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException

from database import supabase, IMAGES_BUCKET
from auth import get_api_key
from .schemas import ProjectRead
from core.cache import cached, invalidate_cache

router = APIRouter(prefix="/projects", tags=["projects"])

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]


def get_public_url(path: str) -> str:
    return supabase.storage.from_(IMAGES_BUCKET).get_public_url(path)


def delete_image_from_storage(url: str) -> None:
    if not url:
        return
    parts = url.split(f"{IMAGES_BUCKET}/")
    path = parts[1] if len(parts) > 1 else None
    if path:
        try:
            supabase.storage.from_(IMAGES_BUCKET).remove([path])
        except Exception:
            pass


def parse_tags(tags: str) -> list[str]:
    if not tags or tags == "[]":
        return []
    try:
        return json.loads(tags)
    except json.JSONDecodeError:
        return [tag.strip() for tag in tags.split(",") if tag.strip()]


async def upload_image_file(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_IMAGE_TYPES}"
        )
    ext = file.filename.split(".")[-1] if file.filename else "jpg"
    file_name = f"{uuid.uuid4()}.{ext}"
    content = await file.read()

    try:
        supabase.storage.from_(IMAGES_BUCKET).upload(
            file_name, content, {"content-type": file.content_type}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    return get_public_url(file_name)


@router.get("/", response_model=list[ProjectRead])
@cached(prefix="projects")
async def read_projects():
    response = (
        supabase.table("projects").select("*").order("created_at", desc=True).execute()
    )
    return response.data


@router.post("/", response_model=ProjectRead)
async def create_project(
    name: str = Form(...),
    description: str = Form(...),
    demo: str = Form(...),
    tags: str = Form("[]"),
    code: str | None = Form(None),
    image: UploadFile = File(...),
    image_dark: UploadFile | None = File(None),
    _: str = Depends(get_api_key),
):
    image_url = await upload_image_file(image)
    image_dark_url = await upload_image_file(image_dark) if image_dark else None

    project_data = {
        "name": name,
        "description": description,
        "demo": demo,
        "tags": parse_tags(tags),
        "code": code,
        "image": image_url,
        "image_dark": image_dark_url,
    }
    response = supabase.table("projects").insert(project_data).execute()
    await invalidate_cache("projects:*")
    return response.data[0]


@router.put("/{id}", response_model=ProjectRead)
async def update_project(
    id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    demo: str | None = Form(None),
    tags: str | None = Form(None),
    code: str | None = Form(None),
    image: UploadFile | None = File(None),
    image_dark: UploadFile | None = File(None),
    _: str = Depends(get_api_key),
):
    existing = supabase.table("projects").select("*").eq("id", id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Project not found")

    old_project = existing.data[0]
    update_data = {}

    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if demo is not None:
        update_data["demo"] = demo
    if tags is not None:
        update_data["tags"] = parse_tags(tags)
    if code is not None:
        update_data["code"] = code

    if image:
        delete_image_from_storage(old_project.get("image"))
        update_data["image"] = await upload_image_file(image)
    if image_dark:
        delete_image_from_storage(old_project.get("image_dark"))
        update_data["image_dark"] = await upload_image_file(image_dark)

    if not update_data:
        return old_project

    response = supabase.table("projects").update(update_data).eq("id", id).execute()
    await invalidate_cache("projects:*")
    return response.data[0]


@router.delete("/{id}", response_model=ProjectRead)
async def delete_project(id: int, _: str = Depends(get_api_key)):
    existing = supabase.table("projects").select("*").eq("id", id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Project not found")

    project = existing.data[0]
    delete_image_from_storage(project.get("image"))
    delete_image_from_storage(project.get("image_dark"))

    supabase.table("projects").delete().eq("id", id).execute()
    await invalidate_cache("projects:*")
    return project
