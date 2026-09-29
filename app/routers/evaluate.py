"""
Master Toggle: Is the flag globally turned on in the database?

User Bucket: What is this specific user's bucket ID (0 to 99)?

Threshold Check: Is bucket < rollout_percentage?

Result: Sends back a simple { "enabled": true } or { "enabled": false }.

Different shape from flags.py this woould return a dashboard record of a user and a flag they want to access  — this is a
read-only, high-frequency path, not an admin action.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import EvaluationResponse

router = APIRouter(tags=["evaluate"])


@router.get("/evaluate/{key}", response_model=EvaluationResponse)
def evaluate_flag(key: str, user_id: str, db: Session = Depends(get_db)):
    flag = crud.get_flag_by_key(db, key)
    if flag is None:
        raise HTTPException(status_code=404, detail=f"Flag '{key}' not found")

    if not flag.enabled:
        return EvaluationResponse(flag_key=key, user_id=user_id, enabled=False)

    bucket = crud.bucket_user(user_id, key)
    enabled = bucket < flag.rollout_percentage

    return EvaluationResponse(flag_key=key, user_id=user_id, enabled=enabled)