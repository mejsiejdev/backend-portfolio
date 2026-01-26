import uuid
import os
from fastapi import UploadFile
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from auth import get_api_key
from .models import Project
from .schemas import ProjectRead, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=list[ProjectRead])
def read_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects

@router.post("/", response_model=ProjectCreate)
def create_project(project: ProjectCreate, session: Session = Depends(get_session), _: str = Depends(get_api_key)):
    db_project = Project.model_validate(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.post("/upload")
async def upload_image(
    file: UploadFile,
    _: str = Depends(get_api_key)
):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {allowed_types}"
        )
    
    ext = file.filename.split(".")[-1] if file.filename else "jpg"
    file_name = f"{uuid.uuid4()}.{ext}"
    os.makedirs("static\images", exist_ok=True)
    file_path = os.path.join("static", "images", file_name)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {"path": f"/static/images/{file_name}"}
    
@router.put("/{id}", response_model=ProjectUpdate)
def update_project(id: int, project: ProjectUpdate, session: Session = Depends(get_session), _: str = Depends(get_api_key)):
    db_project = session.get(Project, id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project
    
@router.delete("/{id}", response_model=ProjectRead)
def delete_project(id: int, session: Session = Depends(get_session), _: str = Depends(get_api_key)):
    db_project = session.get(Project, id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(db_project)
    session.commit()
    return db_project