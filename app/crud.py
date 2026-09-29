'''[ Incoming Request ]  ---> [ Input Schema ]   ---> [ CRUD Function ] ---> [ Database ]
 (Admin / User)             (Validation)           (Executes SQL)         (Storage)
                                                                             |
[ Outgoing Response ] <--- [ Output Schema ]  <--- [ CRUD Function ] <-------+
 (JSON Output)              (Formatting)           (Fetches Data)'''

'''
 The validated pydantic data from the user and the session generated from fastAPI are both passed into the crud function and are contextualized before getting to the database
'''

from typing import Optional

from sqlalchemy.orm import Session

from app.models import Flag
from app.schemas import FlagCreate, FlagUpdate

import hashlib

def create_flag(db: Session, flag: FlagCreate) -> Flag:
    db_flag = Flag(
        key=flag.key,
        description=flag.description,
        enabled=flag.enabled,
        rollout_percentage=flag.rollout_percentage,
    )
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    return db_flag


def get_flag_by_key(db: Session, key: str) -> Optional[Flag]:
    return db.query(Flag).filter(Flag.key == key).first()


def list_flags(db: Session) -> list[Flag]:
    return db.query(Flag).all()


def update_flag(db: Session, key: str, updates: FlagUpdate) -> Optional[Flag]:
    db_flag = get_flag_by_key(db, key)
    if db_flag is None:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_flag, field, value)

    db.commit()
    db.refresh(db_flag)
    return db_flag


def delete_flag(db: Session, key: str) -> bool:
    db_flag = get_flag_by_key(db, key)
    if db_flag is None:
        return False

    db.delete(db_flag)
    db.commit()
    return True




def bucket_user(user_id: str, flag_key: str) -> int:
    """
    Deterministically map a (user_id, flag_key) pair to a stable number
    0-99. The same user + same flag always produces the same bucket, so
    a user's experience of a flag never flips between requests — only
    changing rollout_percentage moves the boundary they're compared
    against.

	Every user automatically gets a ticket number assigned to them for each feature flag (calculated using their user_id + flag_key).

    Pure function: no database, no I/O. This is what lets it be tested
    directly without touching the app or a running server at all.
    """
    combined = f"{user_id}:{flag_key}"
    digest = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return int(digest, 16) % 100
