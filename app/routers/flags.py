"""
Admin endpoints: create, list, get, update, delete flags. No business
logic lives here — each handler calls into crud.py and translates the
result into an HTTP response.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import FlagCreate, FlagResponse, FlagUpdate

router = APIRouter(prefix="/flags", tags=["flags"])


@router.post("", response_model=FlagResponse, status_code=201)
def create_flag(flag: FlagCreate, db: Session = Depends(get_db)):
    existing = crud.get_flag_by_key(db, flag.key)
    if existing is not None:
        raise HTTPException(status_code=409, detail=f"Flag '{flag.key}' already exists")
    return crud.create_flag(db, flag)


@router.get("", response_model=list[FlagResponse])
def list_flags(db: Session = Depends(get_db)):
    return crud.list_flags(db)


@router.get("/{key}", response_model=FlagResponse)
def get_flag(key: str, db: Session = Depends(get_db)):
    flag = crud.get_flag_by_key(db, key)
    if flag is None:
        raise HTTPException(status_code=404, detail=f"Flag '{key}' not found")
    return flag


@router.patch("/{key}", response_model=FlagResponse)
def update_flag(key: str, updates: FlagUpdate, db: Session = Depends(get_db)):
    flag = crud.update_flag(db, key, updates)
    if flag is None:
        raise HTTPException(status_code=404, detail=f"Flag '{key}' not found")
    return flag


@router.delete("/{key}", status_code=204)
def delete_flag(key: str, db: Session = Depends(get_db)):
    deleted = crud.delete_flag(db, key)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Flag '{key}' not found")